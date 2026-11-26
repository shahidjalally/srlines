"""Shared public SRLINES identity and structured data."""
import json

DOMAIN = "https://srlines.net"
LEGAL_NAME = "SRLINES SOFTWARE HOUSE (SMC-PRIVATE) LIMITED"
EMAIL = "contact@srlines.net"
UAN = "+92 311 110 1966"
PHONE = "+923111101966"
WHATSAPP = "https://wa.me/" + PHONE.lstrip("+")
LOCATION = "Umer Town, Sadiqabad, District Rahim Yar Khan, Punjab, Pakistan 64350"
PBX = "/products/srlines-pbx.html"
FLAGSHIP = "SRLINES AI Calling Agent & AI-Enabled PBX"
DESCRIPTION = "SRLINES provides AI calling agents, AI-enabled business telephony and wCRM integration for businesses in Pakistan."
SOCIALS = [
    "https://www.linkedin.com/company/srlines-software-house-smc-pvt-limited",
    "https://www.facebook.com/srlinessoftwarehouse",
    "https://www.instagram.com/srlinessoftwarehouse",
]


def ref(fragment):
    return {"@id": DOMAIN + fragment}


def node(kind, fragment, **fields):
    return {"@type": kind, **ref(fragment), **fields}


def company_graph():
    address = {
        "@type": "PostalAddress", "streetAddress": "Umer Town",
        "addressLocality": "Sadiqabad", "addressRegion": "Punjab",
        "postalCode": "64350", "addressCountry": "PK",
    }
    return [
        node(["Organization", "ProfessionalService"], "/#organization",
             name="SRLINES", legalName=LEGAL_NAME, alternateName="SRLINES Software House",
             url=DOMAIN + "/", logo=DOMAIN + "/logo.png", image=DOMAIN + "/logo.png",
             description=DESCRIPTION, telephone=PHONE, email=EMAIL, address=address,
             contactPoint=ref("/#contact"), sameAs=SOCIALS, areaServed="Pakistan",
             identifier=[
                 {"@type": "PropertyValue", "propertyID": label, "value": value}
                 for label, value in [("UCIN", "0226235"), ("PSEB IT Company", "Z-25-22334/26"),
                                      ("PSEB Call Center/BPO", "C05/PSEB/2026/8766")]
             ],
             knowsAbout=["AI Calling Agents", "AI-enabled PBX", "SIP telephony", "CRM integration"],
             hasOfferCatalog=ref("/#catalog")),
        node("ContactPoint", "/#contact", contactType="sales", telephone=PHONE, email=EMAIL),
        node("WebSite", "/#website", name="SRLINES", alternateName="SRLINES Software House",
             url=DOMAIN + "/", publisher=ref("/#organization"), inLanguage="en"),
        node("OfferCatalog", "/#catalog", name="SRLINES products and implementation services",
             itemListElement=[ref(path + suffix) for path, suffix in [
                 (PBX, "#software"), (PBX, "#service"), ("/products/wcrm.html", "#software"),
                 ("/products/shopify-mobile-app.html", "#software"),
                 ("/services/n8n-workflows.html", "#service"),
                 ("/services/digital-advertising.html", "#service"),
                 ("/services/web-application-development.html", "#service"),
             ]]),
    ]


def page_schema(path, title, description, crumb=None, *, entities=(), faqs=(), about=None, media=()):
    kind = {"/about.html": "AboutPage", "/contact.html": "ContactPage"}.get(path, "WebPage")
    page = node(kind, path + "#webpage", name=title, url=DOMAIN + path,
                description=description, isPartOf=ref("/#website"),
                publisher=ref("/#organization"), inLanguage="en",
                about=about or ref(PBX + "#software" if path == "/" else "/#organization"))
    graph = company_graph() + [page, *entities, *media]
    if media:
        page["video"] = [{"@id": asset["@id"]} for asset in media]
    if entities:
        page["mainEntity"] = {"@id": entities[0]["@id"]}
    if crumb:
        page["breadcrumb"] = ref(path + "#breadcrumb")
        graph.append(node("BreadcrumbList", path + "#breadcrumb", itemListElement=[
            {"@type": "ListItem", "position": i, "name": label, "item": DOMAIN + link}
            for i, (label, link) in enumerate([("Home", "/"), (crumb, path)], 1)
        ]))
    if faqs:
        questions = [{"@type": "Question", "name": q,
                      "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs]
        page["hasPart"] = ref(path + "#faq")
        graph.append(node("FAQPage", path + "#faq", isPartOf=ref(path + "#webpage"),
                          mainEntity=questions))
    return schema_json(graph)


def schema_json(graph):
    return json.dumps({"@context": "https://schema.org", "@graph": graph},
                      ensure_ascii=False, separators=(",", ":")).replace("<", "\\u003c")


def software(path, name, description, **fields):
    return node("SoftwareApplication", path + "#software", name=name, description=description,
                url=DOMAIN + path, publisher=ref("/#organization"), creator=ref("/#organization"),
                applicationCategory="BusinessApplication", **fields)


def service(path, name, description, **fields):
    return node("Service", path + "#service", name=name, description=description,
                url=DOMAIN + path, provider=ref("/#organization"), areaServed="Pakistan",
                serviceType=name, **fields)
