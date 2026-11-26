"""Site-specific checks for JSON-LD semantics and Google rich-result fields."""
from datetime import datetime
from decimal import Decimal, InvalidOperation
import re
from urllib.parse import urlsplit


def objects(value):
    """Yield every JSON-LD object, including nested offers and entities."""
    if isinstance(value, dict):
        yield value
        for child in value.values():
            yield from objects(child)
    elif isinstance(value, list):
        for child in value:
            yield from objects(child)


def list_of(value):
    return value if isinstance(value, list) else [value] if value is not None else []


def normalize(value):
    return " ".join(value.split()).casefold()


def web_url(value):
    if not isinstance(value, str):
        return False
    url = urlsplit(value)
    return url.scheme == "https" and bool(url.netloc)


def iso_date(value):
    if not isinstance(value, str) or not re.match(r"^\d{4}-\d{2}-\d{2}(?:T|$)", value):
        return False
    try:
        datetime.fromisoformat(value)
    except ValueError:
        return False
    return True


def valid_offer_price(offer):
    if not isinstance(offer, dict) or offer.get("@type") != "Offer":
        return False
    try:
        value = Decimal(str(offer.get("price")))
    except InvalidOperation:
        return False
    currency = offer.get("priceCurrency")
    return value.is_finite() and value >= 0 and (
        value == 0 or isinstance(currency, str) and bool(re.fullmatch(r"[A-Z]{3}", currency))
    )


def schema_issues(graph, page, url):
    """Check entity shapes and compare relevant properties against the rendered HTML."""
    visible = normalize(" ".join(page.visible_text))
    for node in objects(graph):
        kinds = list_of(node.get("@type"))
        label = node.get("@id") or node.get("name") or "/".join(kinds)
        if "VideoObject" in kinds:
            if not node.get("name") or not iso_date(node.get("uploadDate")):
                yield f"{label} requires a name and ISO 8601 uploadDate"
            images = list_of(node.get("thumbnailUrl"))
            if not images or not all(web_url(image) for image in images):
                yield f"{label} requires an absolute thumbnail URL"
            if not node.get("embedUrl") or node["embedUrl"] not in page.embeds:
                yield f"{label} does not match an embedded player"
            duration = node.get("duration")
            if duration and not re.fullmatch(r"PT(?=\d)(?:\d+H)?(?:\d+M)?(?:\d+S)?", duration):
                yield f"{label} has an invalid duration"
        if {"SoftwareApplication", "MobileApplication", "WebApplication", "VideoGame"} & set(kinds):
            if not node.get("name") or not any(map(valid_offer_price, list_of(node.get("offers")))):
                yield f"{label} requires a name and a priced Offer"
            rating = node.get("aggregateRating") or {}
            review = node.get("review") or {}
            if not (rating.get("ratingValue") and (rating.get("ratingCount") or rating.get("reviewCount"))
                    or review.get("author") and (review.get("reviewRating") or {}).get("ratingValue")):
                yield f"{label} requires an actual review or aggregate rating"
        if "LocalBusiness" in kinds:
            address = node.get("address") or {}
            if not node.get("name") or address.get("@type") != "PostalAddress" or not all(
                address.get(field) for field in ("streetAddress", "addressLocality", "addressCountry")
            ):
                yield f"{label} requires a name and a physical address"
        if "BreadcrumbList" in kinds:
            entries = list_of(node.get("itemListElement"))
            if len(entries) < 2 or any(
                item.get("@type") != "ListItem" or item.get("position") != index
                or not item.get("name") or not web_url(item.get("item"))
                for index, item in enumerate(entries, 1)
            ):
                yield f"{label} has invalid breadcrumb items"
            elif entries[-1]["item"] != url or normalize(entries[-1]["name"]) not in visible:
                yield f"{label} does not match the visible page breadcrumb"
        if "FAQPage" in kinds:
            questions = list_of(node.get("mainEntity"))
            if not questions:
                yield f"{label} must contain questions"
            for question in questions:
                answer = question.get("acceptedAnswer") or {}
                q = question.get("name", "")
                a = answer.get("text", "")
                if (question.get("@type") != "Question" or answer.get("@type") != "Answer"
                        or not q or not a or normalize(q) not in visible or normalize(a) not in visible):
                    yield f"{label} does not match visible FAQ text: {q}"
        if "ProfilePage" in kinds:
            subject = node.get("mainEntity") or {}
            if subject.get("@type") not in ("Person", "Organization") or not subject.get("name"):
                yield f"{label} requires a named Person or Organization"
