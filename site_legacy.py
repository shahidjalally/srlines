"""Reconcile the hand-maintained pages and generate canonical crawl files."""
from html import escape, unescape
import json
import re

from site_identity import DOMAIN, FLAGSHIP, PBX, UAN, page_schema, schema_json
from voice_content import AGENT, HOSPITAL, LANDINGS, PRICING, RECEPTION, RESTAURANT


JSON_LD = re.compile(r'<script type="application/ld\+json">\s*(.*?)\s*</script>', re.S)
CANONICAL = re.compile(r'<link rel="canonical" href="([^"]+)">')
DESCRIPTION = re.compile(r'<meta name="description" content="([^"]*)">')


def update_legacy(html, path):
    title = unescape(re.search(r"<title>(.*?)</title>", html, re.S)[1]).strip()
    description = unescape(DESCRIPTION.search(html)[1])
    crumb = title.removesuffix(" | SRLINES")
    graph = json.loads(page_schema(path, title, description, crumb))["@graph"]
    page = next(entity for entity in graph if entity.get("@id") == DOMAIN + path + "#webpage")
    for block in JSON_LD.findall(html):
        data = json.loads(block)
        for entity in data.get("@graph", [data]):
            properties = {key: value for key, value in entity.items() if key != "@context"}
            kind = properties.get("@type")
            identity = properties.get("@id")
            if identity in {DOMAIN + fragment for fragment in ("/#organization", "/#website", "/#contact", "/#catalog")}:
                continue
            if kind == "WebPage":
                for key in ("mainEntity", "mentions", "primaryImageOfPage", "potentialAction"):
                    if key in properties:
                        page[key] = properties[key]
                continue
            if kind in ("ProfilePage", "CollectionPage"):
                page["@type"] = kind
                page.update({key: value for key, value in properties.items()
                             if key in ("about", "mainEntity", "hasPart")})
                continue
            # Preserve page-specific markup. Legacy breadcrumbs without a matching
            # visible breadcrumb and commercial offers without current evidence
            # are unsuitable for the shared graph.
            if kind == "BreadcrumbList":
                continue
            if kind == "FAQPage" and identity:
                page["hasPart"] = {"@id": identity}
                properties["isPartOf"] = {"@id": page["@id"]}
            properties.pop("offers", None)
            graph.append(properties)
            if kind in ("Service", "Article", "BlogPosting") and identity:
                page["mainEntity"] = {"@id": identity}
    schema = '<script type="application/ld+json">' + schema_json(graph) + '</script>'
    html = JSON_LD.sub(lambda _: schema, html, count=1)
    if "application/ld+json" not in html:
        html = html.replace("</head>", schema + "\n</head>", 1)
    for old, new in (
        ('href="/#markets"', 'href="/#industries"'),
        ('href="../privacy-policy.html"', 'href="/privacy.html"'),
        ('href="../../privacy-policy.html"', 'href="/privacy.html"'),
        ('href="../terms-of-service.html"', 'href="/terms.html"'),
        ('href="../../terms-of-service.html"', 'href="/terms.html"'),
    ):
        html = html.replace(old, new)
    # On partner pages the brand name is in the masthead, above the page's H1.
    html = html.replace("<h1>SRLINES</h1>", '<div class="partner-brand-name">SRLINES</div>')
    html = html.replace('<p class="partner-brand-name">SRLINES</p>', '<div class="partner-brand-name">SRLINES</div>')
    html = html.replace(".logo-text h1", ".logo-text .partner-brand-name")
    if 'data-legacy-breadcrumb' not in html:
        breadcrumb = ('<nav data-legacy-breadcrumb aria-label="Breadcrumb">'
                      f'<a href="/">Home</a> / <span aria-current="page">{escape(crumb)}</span></nav>')
        # Keep the breadcrumb in the existing layout and out of a masthead.
        main = re.search(r"<main\b[^>]*>", html)
        if main:
            html = html[:main.end()] + breadcrumb + html[main.end():]
        else:
            html = re.sub(r"(<h1\b[^>]*>)", lambda match: breadcrumb + match[0], html, count=1)
    if 'data-voice-link' not in html:
        target, label = {
            "/industries/healthcare.html": (HOSPITAL, "AI calling for hospitals and clinics"),
            "/industries/hospitality.html": (RESTAURANT, "AI calling for restaurants"),
        }.get(path, (PBX, FLAGSHIP))
        link = f'<p data-voice-link><a href="{target}">{escape(label)}</a></p>'
        if "</main>" in html:
            html = html.replace("</main>", link + "</main>", 1)
        else:
            html = html.replace("</body>", link + "</body>", 1)
    return html


def sitemap(paths):
    urls = "\n".join(f"  <url><loc>{DOMAIN}{path}</loc></url>" for path in sorted(set(paths)))
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
            + urls + "\n</urlset>\n")


def complete_public_site(root, write):
    public = []
    for file in sorted(root.rglob("*.html")):
        relative = file.relative_to(root)
        if any(piece.startswith(".") for piece in relative.parts) or relative.parts[0] in {
            "docs", "tests", "content", "contact-form-widget"
        }:
            continue
        html = file.read_text(encoding="utf-8")
        canonical = CANONICAL.search(html)
        if not canonical or not canonical[1].startswith(DOMAIN + "/") or 'content="noindex"' in html:
            continue
        path = canonical[1].removeprefix(DOMAIN)
        if relative.as_posix() not in (path.lstrip("/"), path.lstrip("/") + "index.html"):
            raise ValueError(f"Non-local canonical: {relative} → {path}")
        public.append(path)
        if '<body data-path=' not in html:
            write(relative, update_legacy(html, path))
    write("sitemap.xml", sitemap(public))
    write("ai-sitemap.xml", sitemap(["/", PBX, *LANDINGS]))
    write("product-sitemap.xml", sitemap(path for path in public if path in LANDINGS or
                                        path.startswith("/products/")))
    entities = ["/", "/about.html", "/contact.html", "/credentials.html", PBX]
    for name in ("entity-sitemap.xml", "llm-sitemap.xml"):
        write(name, sitemap(entities))
    write("robots.txt", f"""# Search and training crawlers have separate purposes.
# Keep the existing site-wide access policy pending owner review of training access.
User-agent: *
Allow: /

Sitemap: {DOMAIN}/sitemap.xml
""")
    discovery = f"""# SRLINES

> {FLAGSHIP} is a wCRM-integrated business communication platform in Pakistan.

- [Flagship platform and demo]({DOMAIN}{PBX})
- [AI Calling Agent]({DOMAIN}{AGENT})
- [AI Receptionist]({DOMAIN}{RECEPTION})
- [AI PBX pricing and quotation]({DOMAIN}{PRICING})
- [wCRM]({DOMAIN}/products/wcrm.html)
- [Company and credentials]({DOMAIN}/about.html)
- [Contact SRLINES]({DOMAIN}/contact.html) · {UAN}
- [Canonical sitemap]({DOMAIN}/sitemap.xml)
"""
    for name in ("llms.txt", "llm.txt", ".llms.txt"):
        write(name, discovery)
