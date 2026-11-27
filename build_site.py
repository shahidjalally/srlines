#!/usr/bin/env python3
"""Build the primary SRLINES static pages without a runtime dependency."""
from pathlib import Path
from html import escape
from site_identity import (
    DESCRIPTION, DOMAIN, EMAIL, FLAGSHIP, LEGAL_NAME, LOCATION, PBX, PHONE, SOCIALS,
    UAN, WHATSAPP, node, page_schema, ref, service, software,
)
from voice_content import (
    AGENT, CONSULT, HOSPITAL, LANDINGS, PBX_EXTRA_MINUTE_USD,
    PBX_FAQS, PBX_OPENAI_RATE_PKR, PBX_OPENAI_RATE_USD, PBX_PACKAGE_FEATURES, PBX_PACKAGE_TERMS, PBX_PLANS, PBX_PRICING_FAQS,
    PBX_SECTIONS, PBX_SETUP_PKR, PBX_ZONG_MINUTES, PBX_ZONG_PKR, PBX_ZONG_RATE_PKR,
    PRICING, QUOTE, RECEPTION, RESTAURANT, SCHOOL,
    VIDEO, VIDEO_EMBED, VIDEO_IMAGE, VIDEO_TITLE, VIDEO_UPLOAD_DATE,
)
from site_legacy import complete_public_site

ROOT = Path(__file__).parent
OPENAI_ADS_PIXEL = (
    '<script>!function(w,d,s,u){if(w.oaiq)return;'
    'var q=function(){q.q.push(arguments)};q.q=[];w.oaiq=q;'
    'var j=d.createElement(s);j.async=1;j.src=u;'
    'var f=d.getElementsByTagName(s)[0];f.parentNode.insertBefore(j,f);'
    '}(window,document,"script","https://bzrcdn.openai.com/sdk/oaiq.min.js");'
    'oaiq("init",{pixelId:"Gdnu5euNH4BuKr7TaBQfL3",debug:true});</script>'
)

NAV = {
    "Company": [("About SRLINES", "/about.html"), ("Team & Organogram", "/team.html"), ("Credentials & Partnerships", "/credentials.html"), ("Contact", "/contact.html")],
    "Services": [("Services overview", "/services/index.html"), ("Website development", "/services/website-development.html"), ("Web applications", "/services/web-application-development.html"), ("Mobile applications", "/services/mobile-application-development.html"), ("Digital advertising", "/services/digital-advertising.html"), ("NTN consultancy", "/services/ntn-consultancy.html"), ("Meta verification", "/services/meta-verification.html"), ("n8n deployment", "/services/n8n-installation.html"), ("n8n automation", "/services/n8n-workflows.html")],
    "Products": [("Products overview", "/products/index.html"), ("wCRM", "/products/wcrm.html"), ("Shopify Integrated Mobile App", "/products/shopify-mobile-app.html"), ("AI Calling Agent", AGENT), ("AI Receptionist", RECEPTION), ("AI PBX Pricing", PRICING), ("Mobile app", "/products/wcrm-mobile.html"), ("Shopify app", "/products/wcrm-shopify.html"), ("n8n node", "/products/wcrm-n8n.html"), ("WooCommerce plugin", "/products/wcrm-woocommerce.html"), ("Bitrix24 app", "/products/wcrm-bitrix24.html")],
    "Portfolio": [("Client projects", "/portfolio/index.html"), ("SignSyncer", "/portfolio/signsyncer.html"), ("FormSyncer", "/portfolio/formsyncer.html"), ("Whatsell", "/portfolio/whatsell.html")],
    "Industries": [("Restaurants", RESTAURANT), ("Hospitals & clinics", HOSPITAL), ("Schools & colleges", SCHOOL), ("Real estate", "/industries/real-estate.html"), ("Ecommerce", "/industries/ecommerce.html"), ("Internet service providers", "/industries/isp.html"), ("Professional services", "/industries/professional-services.html"), ("Healthcare", "/industries/healthcare.html"), ("Hospitality", "/industries/hospitality.html"), ("Recruitment", "/industries/recruitment.html")],
}

services = [
 ("website-development", "Website Design & Development", "Websites that make a clear business case", "Business owners and organisations that need an accessible, credible and maintainable public presence.", ["Discovery and content architecture", "Responsive interface design", "Standards-based front-end development", "SEO foundations, analytics readiness and launch support"], "Your brand assets, approved copy, domain access and a named reviewer.", [("Will you use our existing brand?", "Yes. We audit and apply the assets and guidelines you provide."), ("Is hosting included?", "Hosting and ongoing support are scoped in the quotation rather than assumed.")]),
 ("web-application-development", "Web Application Development", "Purpose-built software for real operating work", "Teams replacing spreadsheets, connecting systems or delivering a secure browser-based service.", ["Requirements and workflow mapping", "Interface and application architecture", "API and third-party integration", "Testing, deployment documentation and handover"], "Process owners, sample data, integration documentation and access to test environments.", [("Can you integrate an existing system?", "We assess available APIs, data ownership and vendor constraints during discovery."), ("Who owns the deliverables?", "Ownership, licences and access are made explicit in the project agreement.")]),
 ("mobile-application-development", "Mobile Application Development", "Mobile experiences planned around real users", "Businesses that need a companion app, field workflow or customer-facing mobile product.", ["Product discovery and user flows", "Mobile UI design", "API-connected application development", "Testing and store-release preparation"], "Target platforms, user scenarios, brand assets, API details and store-account access where publishing is included.", [("Do you guarantee store approval?", "No. We prepare submissions and address technical feedback, while stores control approval."), ("Can a mobile app connect to our web system?", "Yes, where a suitable API and permissions are available.")]),
 ("digital-advertising", "Digital Advertising Management", "Accountable campaign operations across Meta, Google and TikTok", "Brands that need structured campaign setup, creative coordination, measurement and ongoing optimisation.", ["Account and tracking audit", "Campaign structure and audience planning", "Creative briefing and launch management", "Reporting and optimisation recommendations"], "Platform access through approved roles, offer details, creative assets, budget confirmation and compliant landing pages.", [("Is advertising spend included?", "No. Media spend and our management scope are identified separately in the quotation."), ("Can you guarantee results?", "No. Performance depends on the offer, market, budget, creative and platform delivery.")]),
 ("ntn-consultancy", "NTN Consultancy", "Practical assistance preparing for National Tax Number registration", "Individuals and businesses in Pakistan seeking help understanding and preparing an NTN application.", ["Requirements checklist", "Document-readiness review", "Application preparation guidance", "Support responding to routine process questions"], "Accurate identity, business, address and registration information plus documents required by the applicable FBR process.", [("Are you a government authority?", "No. SRLINES provides consultancy; FBR controls registration and decisions."), ("Is an NTN guaranteed?", "No. We assist with preparation and guidance but cannot guarantee acceptance or timing.")]),
 ("meta-verification", "Meta Business Portfolio Verification Consultancy", "Prepare a consistent, supportable verification submission", "Businesses that need guidance aligning their legal, web and Meta portfolio information.", ["Business-information consistency review", "Document and domain-readiness checklist", "Portfolio settings guidance", "Submission preparation and follow-up guidance"], "Authorised portfolio access, current legal documents, a business domain and accurate public contact information.", [("Can SRLINES approve verification?", "No. Meta alone controls eligibility, review and approval."), ("Do you have privileged access?", "No. We provide preparation and platform guidance without claiming privileged decision-making access.")]),
 ("n8n-installation", "n8n Installation, Configuration & Deployment", "A documented automation environment your team can operate", "Organisations that want a self-managed or appropriately hosted n8n deployment.", ["Deployment architecture review", "Installation and baseline configuration", "Credentials, webhook and backup planning", "Operational documentation and handover"], "Infrastructure access, domain and DNS control, security requirements, email configuration and an accountable technical contact.", [("Does this include workflow development?", "Baseline workflows can be scoped; complex automations are handled as a separate workstream."), ("Can you deploy anywhere?", "We first confirm that the selected provider supports the required runtime, networking and persistence.")]),
 ("n8n-workflows", "Custom n8n Workflows & Business Automation", "Connect repetitive work into observable workflows", "Teams moving data manually between sales, support, commerce and operational systems.", ["Workflow and exception mapping", "Connector and API assessment", "Workflow implementation and testing", "Monitoring guidance, documentation and handover"], "Process examples, authorised API credentials, sample records, business rules and an owner for acceptance testing.", [("Can every platform be automated?", "Only where supported access, APIs and acceptable terms allow it."), ("How do you handle failures?", "We define validation, retries, alerts and human escalation appropriate to the workflow.")]),
]

products = [
 ("wcrm", "wCRM — Meta Assets Native CRM", "The SRLINES customer-conversation workspace", "Core CRM", "Shared inboxes, sales pipelines, campaigns and automation for teams working through official Meta assets.", "https://crm.srlines.net/", "Explore wCRM"),
 ("wcrm-mobile", "wCRM Mobile App", "Take the wCRM ecosystem with you", "Mobile application", "The official companion application for the wCRM ecosystem, available on Google Play.", "https://play.google.com/store/apps/details?id=net.srlines.wcrm", "Get it on Google Play"),
 ("wcrm-shopify", "wCRM Transactional Notifier — Shopify App", "Connect Shopify events with customer notifications", "Marketplace app", "The published Shopify app in the wCRM ecosystem for transactional notification workflows.", "https://apps.shopify.com/wcrm", "View on Shopify App Store"),
 ("wcrm-n8n", "wCRM n8n Node", "Build wCRM into visual automations", "Published integration", "The published n8n integration connects wCRM actions with broader business workflows.", "https://n8n.io/integrations/wcrm", "View n8n Integration"),
 ("wcrm-woocommerce", "wCRM WooCommerce Plugin", "Connect WooCommerce notification workflows", "Plugin", "A downloadable WooCommerce plugin within the wCRM integration ecosystem.", "https://srlines.net/woocommerce-whatsapp-notifications.zip", "Download Plugin"),
 ("wcrm-bitrix24", "wCRM Bitrix24 App", "Link Bitrix24 workflows with the wCRM ecosystem", "Integration app", "An integration app for organisations coordinating Bitrix24 and wCRM-related communication workflows.", "https://bitrix24.srlines.net/", "Explore Bitrix24 App"),
]

portfolio = [
 ("signsyncer", "SignSyncer", "Signature workflow software", "SRLINES delivered this client software project around signature workflows. Project scope and the precise signature type can be confirmed during a relevant enquiry.", "web"),
 ("formsyncer", "FormSyncer", "Form-driven data workflow implementation", "SRLINES delivered this client application project to support form-based data workflows.", "automation"),
 ("whatsell", "Whatsell", "Conversation-led commerce implementation", "SRLINES delivered this client project around commerce conversations and workflow.", "commerce"),
]

def hrefs(items):
    return ''.join(f'<a href="{u}">{escape(t)}</a>' for t,u in items)

def header():
    groups=''.join(f'<div class="nav-group"><button type="button" aria-expanded="false">{n}<span aria-hidden="true">⌄</span></button><div class="nav-panel">{hrefs(v)}</div></div>' for n,v in NAV.items())
    mobile=''.join(f'<details><summary>{n}</summary>{hrefs(v)}</details>' for n,v in NAV.items())
    return f'''<a class="skip" href="#main">Skip to content</a><header class="site-header"><a class="brand" href="/" aria-label="SRLINES home"><img src="/logo.png" alt="SRLINES" width="180" height="60"></a><nav class="desktop-nav" aria-label="Primary"><a class="primary-product" href="{PBX}">AI Calling &amp; PBX</a>{groups}</nav><a class="button quote" href="/contact.html">Request a Quote</a><button class="menu-toggle" type="button" aria-expanded="false" aria-controls="mobile-menu"><span aria-hidden="true">☰</span><span>Menu</span></button></header><div class="drawer-backdrop" hidden></div><aside class="mobile-drawer" id="mobile-menu" aria-label="Mobile navigation" aria-hidden="true" inert><div class="drawer-head"><b>Explore SRLINES</b><button class="drawer-close" type="button" aria-label="Close menu">×</button></div><nav><a href="/">Home</a><a class="primary-product" href="{PBX}">{escape(FLAGSHIP)}</a>{mobile}<a class="button" href="/contact.html">Request a Quote</a><a href="tel:{PHONE}">Call {UAN}</a><a href="mailto:{EMAIL}">{EMAIL}</a></nav></aside>'''

def footer():
    return f'''<footer><div><a class="brand brand-light" href="/"><img src="/logo.png" alt="SRLINES" width="180" height="60"></a><p>{DESCRIPTION}</p></div><div><strong>Products and services</strong><a href="{PBX}">{escape(FLAGSHIP)}</a><a href="/products/wcrm.html">wCRM</a><a href="{PRICING}">AI PBX pricing</a><a href="/products/shopify-mobile-app.html">Shopify Integrated Mobile App</a><a href="/services/index.html">Services</a><a href="/products/index.html">Products</a><a href="/portfolio/index.html">Client projects</a><a href="/credentials.html">Credentials</a></div><div><strong>Contact</strong><a href="mailto:{EMAIL}">{EMAIL}</a><a href="tel:{PHONE}">{UAN}</a><a href="{WHATSAPP}" target="_blank" rel="noopener noreferrer">Chat on WhatsApp</a><span>{LOCATION}</span></div><div><strong>Verify</strong><a href="/meet-our-partners/">Meet our partners</a><a href="/meta-partner-authority-pakistan.html">Meta credentials</a><a href="https://eservices.secp.gov.pk/eServices/ControllerServlet?request_id=VERIFY_ONLINE_INCORP_CERT&amp;id=0226235" target="_blank" rel="noopener noreferrer">SECP incorporation verification</a><a href="https://play.google.com/store/apps/details?id=net.srlines.wcrm" target="_blank" rel="noopener noreferrer">wCRM Android app on Google Play</a><a href="/privacy.html">Privacy</a><a href="/terms.html">Terms</a></div><small>© 2026 {LEGAL_NAME} · UCIN 0226235 · PSEB IT Company: Z-25-22334/26 · Call Center/BPO: C05/PSEB/2026/8766</small></footer>'''

def shell(path, title, desc, body, crumb="", *, entities=(), faqs=(), about=None, voice=False, media=()):
    canonical=DOMAIN+("/" if path=="index.html" else "/"+path)
    bc=f'<nav class="breadcrumbs" aria-label="Breadcrumb"><a href="/">Home</a><span aria-hidden="true">/</span><span aria-current="page">{escape(crumb or title)}</span></nav>' if path!="index.html" else ""
    structured_data = ""
    if path != "404.html":
        schema = page_schema(canonical.removeprefix(DOMAIN), title, desc,
                             (crumb or title) if bc else None, entities=entities,
                             faqs=faqs, about=about, media=media)
        structured_data = f'<script type="application/ld+json">{schema}</script>'
    og_image = "/assets/srlines-pbx.webp" if voice else "/Grow%20Sales%20with%20WhatsApp%20CRM%20%26%20Live%20Chat.png"
    og_width, og_height = (960, 960) if voice else (1280, 720)
    robots = '<meta name="robots" content="noindex">' if path == "404.html" else ""
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8">{OPENAI_ADS_PIXEL}{robots}<script src="/assets/whatsapp-conversion.js" defer></script><meta name="viewport" content="width=device-width,initial-scale=1"><title>{escape(title)} | SRLINES</title><meta name="description" content="{escape(desc,quote=True)}"><link rel="canonical" href="{canonical}"><meta property="og:type" content="website"><meta property="og:title" content="{escape(title,quote=True)} | SRLINES"><meta property="og:description" content="{escape(desc,quote=True)}"><meta property="og:url" content="{canonical}"><meta property="og:image" content="{DOMAIN}{og_image}"><meta property="og:image:width" content="{og_width}"><meta property="og:image:height" content="{og_height}"><link rel="icon" href="/favicon.ico"><link rel="stylesheet" href="/assets/redesign.css">{structured_data}</head><body data-path="/{path}">{header()}<main id="main">{bc}{body}<aside class="flagship-strip" aria-label="Explore flagship solutions"><span>Built for connected business</span><a href="/products/srlines-pbx.html">AI Calling Agent &amp; AI-Enabled PBX →</a><a href="/products/shopify-mobile-app.html">Shopify-integrated mobile app →</a></aside></main>{footer()}<script src="/assets/redesign.js" defer></script></body></html>'''

def hero(kicker,title,text,actions=''):
    return f'<section class="page-hero"><div><span class="eyebrow">{kicker}</span><h1>{title}</h1><p>{text}</p>{actions}</div><div class="hero-art" aria-hidden="true"><i></i><i></i><i></i><b>SR</b></div></section>'

def cards(items, cls="cards"):
    return f'<div class="{cls}">'+''.join(f'<article><span>{escape(a)}</span><h3>{escape(b)}</h3><p>{escape(c)}</p>{d if len(x)>3 else ""}</article>' for x in items for a,b,c,*rest in [x] for d in [rest[0] if rest else ''])+'</div>'

def faq(items, title="Before we begin"):
    return '<section class="section faq"><div class="section-title"><span class="eyebrow">Questions</span><h2>'+escape(title)+'</h2></div>'+''.join(f'<details><summary>{escape(q)}</summary><p>{escape(a)}</p></details>' for q,a in items)+'</section>'

def write(path, html):
    p=ROOT/path; p.parent.mkdir(parents=True,exist_ok=True); p.write_text(html,encoding='utf-8')

def voice_actions(*, demo=PBX + "#demo", explore=False):
    links = [("Watch Live Demo", demo), ("Book a Consultation", CONSULT),
             ("Request a Quotation", QUOTE)]
    if explore:
        links.append(("Explore AI Calling Agent", AGENT))
    links.append(("Call Our UAN", "tel:" + PHONE))
    return '<div class="actions voice-actions">' + "".join(
        f'<a class="button{" secondary" if i else ""}" href="{escape(url, quote=True)}">{label}</a>'
        for i, (label, url) in enumerate(links)
    ) + '</div>'


def voice_visual():
    return ('<figure class="hero-product voice-visual">'
            '<img src="/assets/srlines-pbx.webp" alt="Diagram showing SRLINES PBX with SIP connectivity, IVR, staff extensions and CRM" width="960" height="960" fetchpriority="high">'
            '<figcaption>SRLINES business telephone system and CRM workflow.</figcaption></figure>')


def voice_hero(label, title, description, actions, visual=None):
    return (f'<section class="page-hero voice-hero"><div><span class="eyebrow">{escape(label)}</span>'
            f'<h1>{escape(title)}</h1><p>{escape(description)}</p>{actions}</div>'
            f'{visual or voice_visual()}</section>')


def demo_section():
    return (
        '<section class="section split tinted" id="demo"><div><h2>Watch the SRLINES calling demo</h2>'
        '<p>See a walkthrough of the AI calling and PBX platform. For a tailored demo, bring a sample enquiry and the route it should take to your staff.</p>'
        f'<p><a href="{VIDEO}" target="_blank" rel="noopener noreferrer">Watch the SRLINES demo on YouTube</a></p></div>'
        f'<iframe class="voice-video" src="{VIDEO_EMBED}" title="{escape(VIDEO_TITLE, quote=True)}" width="560" height="315" loading="lazy" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe></section>'
    )


def demo_media():
    # The visible player remains available while required upload metadata is pending.
    if not VIDEO_UPLOAD_DATE:
        return ()
    return (node("VideoObject", PBX + "#demo-video", name=VIDEO_TITLE,
                 description="Official walkthrough of the SRLINES business calling platform.",
                 thumbnailUrl=VIDEO_IMAGE, uploadDate=VIDEO_UPLOAD_DATE,
                 embedUrl=VIDEO_EMBED, url=VIDEO, publisher=ref("/#organization"),
                 about=ref(PBX + "#software")),)


def voice_sections(sections):
    return '<section class="section"><div class="voice-sections">' + "".join(
        f'<article><h2>{escape(title)}</h2><p>{escape(text)}</p></article>'
        for title, text in sections
    ) + '</div></section>'


def voice_resources(current=None):
    links = [(FLAGSHIP, PBX), ("AI Calling Agent Pakistan", AGENT),
             ("AI Receptionist Pakistan", RECEPTION), ("Restaurants", RESTAURANT),
             ("Hospitals and clinics", HOSPITAL), ("Schools and colleges", SCHOOL),
             ("AI PBX pricing", PRICING), ("wCRM integration", "/products/wcrm.html")]
    return '<section class="section tinted voice-resources" id="industries"><h2>Explore business calling</h2><ul>' + "".join(
        f'<li><a href="{url}">{escape(label)}</a></li>' for label, url in links if url != current
    ) + '</ul></section>'


def flagship_section():
    return f'''<section class="section flagship-section"><div class="section-title"><h2>SRLINES products</h2></div>
    <div class="cards"><article><h3>{escape(FLAGSHIP)}</h3><p>Conversational voice workflows, SIP telephony, routing and wCRM integration.</p><a href="{PBX}">Explore the flagship platform</a></article>
    <article><h3>wCRM</h3><p>Manage omnichannel conversations, sales pipelines and automation.</p><a href="/products/wcrm.html">Explore wCRM</a></article>
    <article><h3>Shopify-integrated mobile app</h3><p>Launch a branded Android shopping app connected to your store.</p><a href="/products/shopify-mobile-app.html">Explore mobile commerce</a></article></div></section>'''


def build_pbx_pricing():
    title = "AI Calling Agent & PBX Pricing in Pakistan"
    description = ("Compare SRLINES AI PBX plans in Pakistan with PKR totals, a shared inbound and outbound AI allowance "
                   "and separate Zong, OpenAI and SRLINES costs.")
    quote_url = escape(QUOTE, quote=True)
    body = f'''<section class="page-hero pbx-pricing-hero"><div>
        <h1>AI Calling Agent and PBX Pricing in Pakistan</h1>
        <p>Prepaid plans for a managed AI receptionist that answers routine calls,
        captures enquiries and routes exceptions to your team.</p>
        <div class="actions voice-actions"><a class="button" href="#plans">Compare plans</a>
        <a class="button secondary" href="{quote_url}">Request a quote</a></div>
    </div></section>'''
    packages = []
    for name, minutes, openai_cost, srlines_rate in PBX_PLANS:
        srlines_cost = minutes * srlines_rate
        total = PBX_ZONG_PKR + openai_cost + srlines_cost
        packages.append((name, minutes, openai_cost, srlines_rate, srlines_cost, total))
    rows = "".join(
        f'<tr id="{name.lower()}"><th scope="row">{name}</th>'
        f'<td>{minutes:,}<small>{minutes // 60} h {minutes % 60:02d} min</small></td>'
        f'<td>{PBX_ZONG_PKR:,}</td><td>{openai_cost:,}</td><td>{srlines_rate:.2f}</td>'
        f'<td>{srlines_cost:,}</td><td><strong>{total:,}</strong></td></tr>'
        for name, minutes, openai_cost, srlines_rate, srlines_cost, total in packages
    )
    body += f'''<section class="section pbx-pricing" id="plans"><div class="pbx-plan-content">
        <h2 id="pbx-plans-title">Simple monthly packages</h2>
        <p>All plans are prepaid and renew every 30 days. The table shows the <strong>total AI conversation time</strong> for each plan.
        Inbound and outbound AI calls share this allowance and use the same AI rate within the plan.</p>
        <div class="pbx-plan-scroll" role="region" aria-labelledby="pbx-plans-title" tabindex="0">
            <table class="pbx-plan-table" aria-labelledby="pbx-plans-title" aria-describedby="pbx-rate-notes">
                <thead><tr><th scope="col">Plan</th><th scope="col">AI minutes</th><th scope="col">Zong (PKR)</th>
                <th scope="col">OpenAI (PKR)</th><th scope="col">SRLINES /min</th><th scope="col">SRLINES (PKR)</th>
                <th scope="col">Total (PKR)</th></tr></thead>
                <tbody>{rows}</tbody>
            </table>
        </div>
        <div class="pbx-rate-notes" id="pbx-rate-notes">
            <p>Zong: {PBX_ZONG_MINUTES:,} outbound airtime minutes are included in each plan total
            at PKR {PBX_ZONG_RATE_PKR:.2f}/min (PKR {PBX_ZONG_PKR:,} per 30 days). Inbound airtime is free under the operator arrangement.
            Airtime and AI conversation time are measured separately.</p>
            <p>OpenAI: USD {PBX_OPENAI_RATE_USD:.4f}/min (approx. PKR {PBX_OPENAI_RATE_PKR:.2f}). AI minutes vary by plan.</p>
            <p>Rates may change at short notice due to Zong tariffs, USD/PKR changes and inflation.</p>
        </div>
        <div id="charges">
            <p><strong>One-time implementation and setup:</strong> PKR {PBX_SETUP_PKR:,} per business, payable in advance.
            Covers account setup, basic agent configuration, portal onboarding and initial setup of the included UAN,
            three concurrent sessions, IVR, keypad routing and soft extensions. Custom integrations, additional numbers
            and substantial workflow development are quoted separately.</p>
            <p><strong>Additional AI minutes:</strong> USD {PBX_EXTRA_MINUTE_USD:.2f} per minute in either direction,
            prepaid and subject to availability. SRLINES confirms rates for outbound airtime beyond the bundle and
            any destination-specific charges before activation.</p>
        </div>
    </div></section>'''
    body += '<section class="section tinted pbx-pricing" id="included">'
    body += '<div class="section-title"><h2>What each plan includes</h2></div>'
    body += '<div class="voice-sections">' + "".join(
        f'<article><h3>{escape(heading)}</h3><p>{escape(copy)}</p></article>'
        for heading, copy in PBX_PACKAGE_FEATURES
    ) + '</div></section>'
    body += faq(PBX_PRICING_FAQS, "AI PBX pricing FAQs")
    body += '<section class="section tinted pbx-pricing" id="service-terms">'
    body += '<div class="section-title"><h2>Service terms and safeguards</h2></div>'
    body += '<div class="voice-sections">' + "".join(
        f'<article><h3>{escape(heading)}</h3><p>{escape(copy)}</p></article>'
        for heading, copy in PBX_PACKAGE_TERMS
    ) + '</div></section>'
    body += voice_resources(PRICING)
    body += f'''<section class="cta">
        <h2>Request a quote for your calling setup</h2>
        <p>Share your expected inbound minutes, busiest call times, any outbound needs and the workflows you want to automate.</p>
        <a class="button light" href="{quote_url}">Request a quote</a>
        <a class="button light" href="tel:{PHONE}">Call {UAN}</a>
    </section>'''

    managed_service = ref(PBX + "#service")
    plan_offers = [
        node("Offer", PRICING + "#" + name.lower(), name=name,
             url=DOMAIN + PRICING + "#" + name.lower(),
             description=(f"Includes {minutes:,} AI minutes shared across inbound and outbound calls per prepaid 30-day cycle, "
                          "one UAN and three concurrent call sessions."),
             itemOffered=managed_service, offeredBy=ref("/#organization"),
             price=total, priceCurrency="PKR",
             priceSpecification={
                 "@type": "UnitPriceSpecification", "price": total, "priceCurrency": "PKR",
                 "referenceQuantity": {"@type": "QuantitativeValue", "value": 30, "unitCode": "DAY"},
             })
        for name, minutes, _, _, _, total in packages
    ]
    plan_catalog = node("OfferCatalog", PRICING + "#plans", name="Simple monthly packages",
                        itemListElement=plan_offers)
    write(PRICING.lstrip("/"), shell(PRICING.lstrip("/"), title, description, body, "AI PBX Pricing",
                                     voice=True, entities=(plan_catalog,), about=managed_service))


def build_voice():
    pbx_title = "AI Calling Agent & AI PBX in Pakistan"
    pbx_desc = "Explore SRLINES conversational AI, business SIP, UAN, IVR, call recording, human handover and wCRM integration. Watch the demo or request a quote."
    pbx = voice_hero("Flagship voice platform", "AI Calling Agent and AI-Enabled PBX System in Pakistan",
                     "Combine conversational AI, business telephony and wCRM in a phone system configured around your number, callers and staff.", voice_actions(demo="#demo"))
    pbx += demo_section() + voice_sections(PBX_SECTIONS) + voice_resources(PBX)
    pbx += faq(PBX_FAQS, "AI Calling Agent and PBX FAQs")
    write(PBX.lstrip("/"), shell(PBX.lstrip("/"), pbx_title, pbx_desc, pbx, "AI Calling & PBX",
                                 voice=True, faqs=PBX_FAQS, entities=(
        service(PBX, FLAGSHIP, pbx_desc),
        software(PBX, FLAGSHIP, pbx_desc, genre="Business telephony software",
                 image=DOMAIN + "/assets/srlines-pbx.webp"),
    ), about=ref(PBX + "#software"), media=demo_media()))

    for path, (title, description, heading, intro, sections, faqs) in LANDINGS.items():
        visual = ('<div class="voice-flow"><h2>Call workflow</h2><ol>'
                  + "".join(f'<li>{escape(step)}</li>' for step in FLOW_STEPS[path]) + '</ol></div>')
        body = voice_hero("Business calling", heading, intro, voice_actions(), visual)
        body += voice_sections(sections) + faq(faqs, heading + " FAQs") + voice_resources(path)
        body += f'<section class="cta"><h2>Plan your calling workflow</h2><p>Share your number, call volume and the enquiries you want to handle.</p><a class="button light" href="{escape(QUOTE, quote=True)}">Request a Quotation</a></section>'
        entities = (service(path, heading, description,
                            audience={"@type": "BusinessAudience", "name": AUDIENCES[path]}),)
        write(path.lstrip("/"), shell(path.lstrip("/"), title, description, body, title,
                                     voice=True, entities=entities, faqs=faqs,
                                     about=ref(PBX + "#software")))


    build_pbx_pricing()


FLOW_STEPS = {
    AGENT: ("Caller explains the request", "AI uses approved business instructions", "Staff handle exceptions"),
    RECEPTION: ("Answer and identify the enquiry", "Use the correct hours and routing rules", "Transfer or arrange a callback"),
    RESTAURANT: ("Identify the branch", "Answer menu or takeaway questions", "Send orders and reservation requests to staff"),
    HOSPITAL: ("Identify the department", "Share approved clinic information", "Route appointment requests to staff"),
    SCHOOL: ("Ask about campus and grade", "Share published admissions information", "Connect the caller to the office"),
}
AUDIENCES = {
    AGENT: "Businesses in Pakistan", RECEPTION: "Customer-facing businesses",
    RESTAURANT: "Restaurants", HOSPITAL: "Hospitals and clinics", SCHOOL: "Schools and colleges",
}


def wcrm_resources():
    guides = [
        ("WhatsApp Cloud API provider in Pakistan", "/best-whatsapp-api-provider-pakistan.html"),
        ("WhatsApp API plans", "/whatsapp-api-pricing-pakistan.html"),
        ("Compare WhatsApp API prices", "/whatsapp-api-price-comparison-pakistan.html"),
        ("Cloud API vs WhatsApp Business app", "/whatsapp-cloud-api-vs-whatsapp-business-app.html"),
        ("Shopify and WhatsApp integration", "/shopify-whatsapp-integration-pakistan.html"),
        ("WhatsApp chatbot for COD stores", "/whatsapp-chatbot-for-cod-stores-pakistan.html"),
        ("Bitrix24 WhatsApp app", "/bitrix24-whatsapp-app.html"),
        ("Kanban sales pipeline", "/kanban-sales-pipeline.html"),
        ("Multi-assets CRM", "/multi-assets-crm.html"),
        ("Social media management", "/social-meida-management.html"),
        ("OneZeroArt integration announcement", "/official-mou-onezeroart-whatsapp-integration.html"),
    ]
    cities = ("Islamabad", "Karachi", "Lahore", "Multan", "Rawalpindi")
    city_guides = [
        f'<details><summary>{label}</summary><ul>' + "".join(
            f'<li><a href="/whatsapp-api-{slug}-{city.lower()}.html">{label} in {city}</a></li>'
            for city in cities
        ) + '</ul></details>'
        for slug, label in (("ctwa-ads", "Click-to-WhatsApp ads"), ("ecommerce", "Ecommerce messaging"),
                            ("real-estate", "Real estate enquiries"))
    ]
    return ('<section class="section voice-resources"><h2>wCRM and WhatsApp resources</h2><ul>'
            + "".join(f'<li><a href="{url}">{label}</a></li>' for label, url in guides)
            + '</ul>' + "".join(city_guides) + '</section>')


def build_commerce():
    app=hero('Branded mobile commerce','Your brand. Your app. Your complete commerce ecosystem.','Launch a mobile shopping experience with your own name, logo, products and identity—connected to Shopify and a web-based admin panel.','<div class="actions"><a class="button" href="https://play.google.com/store/apps/details?id=net.srlines.ecommerce" target="_blank" rel="noopener noreferrer">Try the Android app</a><a class="button secondary" href="https://ecommerce.srlines.net/" target="_blank" rel="noopener noreferrer">Explore the admin panel</a></div>')
    app += f'<section class="section product-infographic"><img src="/Ecommerce_App_Promotional_Banner_1200x600.png" alt="SRLINES branded ecommerce mobile application" width="1200" height="600" loading="lazy"></section><section class="section">'+cards([('Mobile shopping','A store in your customer’s pocket','Give customers a dedicated Android shopping experience under your own brand.'),('Store operations','Products & order management','Manage your catalogue and orders through the web-based backend.'),('Shopify connectivity','Connected store workflows','Connect the mobile app, backend and Shopify store with synchronized product and order workflows.'),('White-label option','Your identity, throughout','Choose a branded admin panel for a complete white-label commerce ecosystem.')])+f'</section><section class="section split tinted"><div><span class="eyebrow">Live demonstration</span><h2>Experience the complete setup.</h2><p>Explore mobile shopping, product and order management, the admin backend, Shopify connectivity and app-to-backend synchronization.</p><p>Demo store identifier: <strong>demo</strong></p><a class="text-link" href="/contact.html?service=shopify-mobile-app-demo">Request demo access →</a></div><div><h2>Built around your business.</h2><p>Your brand name, logo, product catalogue and visual identity. Add your own branding to the administration panel for a consistent experience across your commerce operations.</p><p>Contact our team for pricing, deployment details and next steps.</p></div></section><section class="cta"><h2>Your next storefront is in their hands.</h2><p>Tell us about your store and the experience you want to create.</p><a class="button light" href="{WHATSAPP}?text=INTERESTED%20in%20the%20Shopify%20Integrated%20Mobile%20App" target="_blank" rel="noopener noreferrer">I’m interested</a></section>'
    write('products/shopify-mobile-app.html',shell('products/shopify-mobile-app.html','Shopify Integrated Mobile App','Launch your branded Android ecommerce app, Shopify connectivity and web admin panel, with optional white-label administration.',app, entities=(software('/products/shopify-mobile-app.html', 'Shopify Integrated Mobile App', 'Branded Android shopping app connected to Shopify.', genre='Android commerce software', image=DOMAIN + '/Ecommerce_App_Promotional_Banner_1200x600.png'),)))

def build():
    home = voice_hero("SRLINES business communication",
                      "AI Calling Agents and AI-Enabled PBX for Pakistani Businesses",
                      "Answer and make business calls in Urdu or English with an AI receptionist. Connect local SIP telephony, transfer callers to staff and bring call workflows into wCRM.",
                      voice_actions(demo="#demo", explore=True))
    home += voice_sections([
        ("How AI calling works", "A caller explains what they need in their own words. An AI calling agent uses approved business information to answer routine questions or routes the call to staff. The PBX handles the telephone connections, extensions and routing."),
        ("Give every enquiry a route", "Plan for peak hours, after-hours requests and missed enquiries. Use IVR, recording and reporting where appropriate, and decide what call activity should reach wCRM for follow-up."),
        ("From a demo to your business number", "Bring a sample call and your current carrier. We map the workflow, confirm SIP and number compatibility, then test call quality, escalation and capacity before launch."),
    ]) + demo_section() + voice_resources()
    home_faqs = [PBX_FAQS[i] for i in (0, 2, 4, 6)]
    home += faq(home_faqs, "Business calling FAQs")
    home+=flagship_section()
    home+='''<section class="trust-grid" aria-label="Verifiable company and product references"><a href="https://eservices.secp.gov.pk/eServices/ControllerServlet?request_id=VERIFY_ONLINE_INCORP_CERT&amp;id=0226235" target="_blank" rel="noopener noreferrer"><span>Company registration</span><strong>SECP incorporation verification</strong><small>UCIN 0226235 · SRLINES SOFTWARE HOUSE (SMC-PRIVATE) LIMITED</small></a><a href="https://play.google.com/store/apps/details?id=net.srlines.wcrm" target="_blank" rel="noopener noreferrer"><span>Published application</span><strong>wCRM Android app on Google Play</strong><small>Explore the official wCRM Android application</small></a><a href="/Meta%20Tech%20Provider%20Certificate.pdf" target="_blank" rel="noopener noreferrer"><span>Meta credential evidence</span><strong>Technology Provider certificate</strong><small>Explore our technology provider documentation</small></a></section>
    <section class="section"><div class="section-title"><span class="eyebrow">Built around business outcomes</span><h2>Connect customer journeys, internal systems and the people doing the work.</h2></div>'''+cards([('Web & mobile','Custom applications','Plan and build customer-facing and operational software around documented requirements.','<a href="/services/index.html">Explore software services →</a>'),('CRM & WhatsApp','Connected conversations','Onboard the official WhatsApp Cloud API and connect conversations with wCRM, Bitrix24 or a suitable existing workflow.','<a href="/products/wcrm-bitrix24.html">Explore CRM integrations →</a>'),('Automation','Less repetitive work','Use n8n, APIs and carefully scoped AI-assisted steps with validation and human handover.','<a href="/services/n8n-workflows.html">Explore automation →</a>')])+'''</section>
    <section class="section dark"><div class="split"><div><span class="eyebrow">Omnichannel CRM</span><h2>wCRM brings customer conversations and sales work together.</h2><p>A customer communication and sales platform built around official Meta integrations, with a shared inbox, pipelines, campaigns, team collaboration and connected automation.</p><div class="actions"><a class="button light" href="/contact.html?service=wcrm-demo">Request a wCRM demo</a><a class="text-link light-link" href="/products/wcrm.html">Explore wCRM →</a></div></div><figure class="product-shot"><img src="/wCRM-Inbox-New-Look.png" alt="wCRM shared inbox interface" width="1365" height="768" loading="lazy"><figcaption>Shared inbox interface shown with demonstration data.</figcaption></figure></div></section>
    <section class="section"><div class="section-title"><span class="eyebrow">Specialist integrations</span><h2>Make the systems you already use work together.</h2></div>'''+cards([('Official API','WhatsApp Cloud API','Onboarding, templates, webhooks and CRM integration. Meta controls approval and platform access.'),('CRM workflow','Bitrix24 + WhatsApp','Connect supported deal, lead and customer communication steps after discovery.'),('Business portfolio','Meta setup assistance','Prepare portfolio information and verification submissions without promising Meta approval.'),('Workflow platform','n8n integrations','Connect supported applications and APIs with testing, monitoring and exception handling.'),('Responsible automation','AI + human handover','Scope AI-assisted classification or response steps with defined review and escalation.')])+'''</section>
    <section class="section delivery"><div class="section-title"><span class="eyebrow">International delivery from Pakistan</span><h2>A documented route from brief to handover.</h2><p>Communication cadence, milestones, confidentiality, account ownership, source-code/IP arrangements and post-launch support are agreed in the proposal or contract for each engagement.</p></div><ol><li><b>01</b><h3>Discovery</h3><p>Goals, users, systems, risks and requirements.</p></li><li><b>02</b><h3>Scope</h3><p>Deliverables, milestones, responsibilities and review points.</p></li><li><b>03</b><h3>Build</h3><p>Design, development or integration in reviewable stages.</p></li><li><b>04</b><h3>Test</h3><p>Acceptance checks, feedback and release preparation.</p></li><li><b>05</b><h3>Handover</h3><p>Deployment, documentation and agreed support.</p></li></ol></section>
    <section class="section faq"><div class="section-title"><span class="eyebrow">Questions from international buyers</span><h2>Before we start.</h2></div><details><summary>Where is SRLINES based?</summary><p>SRLINES is based in Sadiqabad, Punjab, Pakistan and works with organisations in Pakistan and internationally.</p></details><details><summary>Who owns platform accounts and project deliverables?</summary><p>Account ownership, access, source code, intellectual property and licences are recorded in the proposal or contract. For WhatsApp projects, we plan around customer-controlled Meta assets where the platform permits.</p></details><details><summary>Can you guarantee Meta verification or an AI outcome?</summary><p>No. We can assist with setup, integration and submission preparation, but Meta controls its decisions and automation outcomes depend on data, systems and agreed review controls.</p></details><details><summary>How do remote projects stay visible?</summary><p>The agreed proposal identifies milestones, review points, communication channels, responsibilities and acceptance criteria.</p></details></section>
    <section class="cta"><span class="eyebrow">Have a software or integration brief?</span><h2>Turn it into a practical delivery plan.</h2><p>Tell us the business problem, current systems and target outcome. We will reply with relevant questions and the next step.</p><a class="button light" href="/contact.html">Discuss your project</a></section>'''
    home += '<section class="section"><h2>Explore automation guides</h2><p><a href="https://blog.srlines.net/" target="_blank" rel="noopener noreferrer">Read the SRLINES blog</a> for customer communication, WhatsApp and business automation guides.</p></section>'
    write('index.html', shell('index.html', 'AI Calling Agent & AI-Enabled PBX Pakistan',
          'Automate business calls with SRLINES AI Calling Agents and AI-enabled PBX in Pakistan. Explore AI reception, IVR, recording, UAN and wCRM integration.',
          home, voice=True, faqs=home_faqs, media=demo_media()))

    about=hero('Ideas to Impact','Technology with purpose. Delivery with precision.','SRLINES SOFTWARE HOUSE (SMC-PRIVATE) LIMITED works with business owners, agencies and operational teams in Pakistan and international markets.')+'''<section class="section split"><div><h2>What we do</h2><p>We translate business processes into websites, applications, connected workflows and measured digital operations. Our flagship platform is <a href="/products/srlines-pbx.html">SRLINES AI Calling Agent &amp; AI-Enabled PBX</a>, integrated with wCRM. Our other products include branded Shopify mobile commerce. We combine product expertise with bespoke software delivery to help your business operate with confidence.</p></div><div><h2>How we work</h2><ul class="checks"><li>Clarify the problem, users and constraints</li><li>Define scope, access and acceptance criteria</li><li>Build and review in practical stages</li><li>Document launch, ownership and next steps</li></ul></div></section>'''
    about += f'''<section class="section split"><div><h2>Company credentials</h2>
    <p>SRLINES is an SECP-registered Single Member Private Limited Company and is registered with PSEB for IT and Call Center/BPO services. SRLINES uses PTA IP-whitelisted infrastructure for relevant deployments.</p>
    <p>Explore <a href="/credentials.html">registration references and Meta credentials</a>, including SRLINES’ Meta Badged Partner and Meta Verified Technology Provider references.</p></div>
    <div><h2>Headquarters and official profiles</h2><p>{LOCATION}</p><p><a href="tel:{PHONE}">{UAN}</a> · <a href="mailto:{EMAIL}">{EMAIL}</a></p>
    <p>{' · '.join(f'<a href="{url}" target="_blank" rel="noopener noreferrer">{label}</a>' for label, url in zip(("LinkedIn", "Facebook", "Instagram"), SOCIALS))}</p></div></section>'''
    write('about.html',shell('about.html','About SRLINES','Learn how SRLINES approaches software, services, owned products and client delivery.',about))

    team=hero('Leadership & organisation','One vision. Three specialist teams.','Executive direction, technical leadership and dedicated managers keep every engagement connected—from business development to delivery and customer success.')
    team += '<section class="section org-chart" aria-labelledby="org-title"><div class="section-title"><span class="eyebrow">Our organogram</span><h2 id="org-title">Clear leadership. Shared accountability.</h2><p>Our three managers report to the Chief Executive Officer &amp; Head of Technical Operations.</p></div><ol class="org-root"><li><div class="org-leadership">'
    team += '<article class="team-card executive"><img src="/CEO-Photograph.jpg" alt="Shahid Rasool" width="320" height="400"><span class="eyebrow">Executive leadership</span><h3>Shahid Rasool</h3><p class="team-role">Chief Executive Officer &amp; Head of Technical Operations</p><p>Provides company direction and technical oversight across software delivery, connected communications and business operations.</p></article>'
    soban_image = ROOT/'assets/team/muhammad-oban.jpeg'
    soban_portrait = '<img src="/assets/team/muhammad-oban.jpeg" alt="Muhammad Soban" class="soban-portrait" width="768" height="889" decoding="async">' if soban_image.exists() else '<div class="team-monogram" aria-hidden="true">MS</div>'
    team += '<article class="team-card executive">'+soban_portrait+'<span class="eyebrow">Co Founder</span><h3>Muhammad Soban</h3><p class="team-role">Co Founder &amp; eCommerce Specialist</p></article></div><ol class="org-managers">'
    managers=[('Muhammad Saim','BPOM','Business Processes Outsourcing Manager','Coordinates outsourcing operations, business processes and service delivery.','/assets/team/muhammad-saim.png','MS'),('Rubab Javed','BDM','Business Development Manager','Connects business requirements with the right solutions and builds lasting client relationships.','/assets/team/rubab-javed.jpg','RJ'),('Muhammad Sarim','CSM','Customer Success Manager','Supports onboarding, product adoption and ongoing customer relationships.','/assets/team/muhammad-sarim.png','MS')]
    for name,initials,role,description,image,monogram in managers:
        portrait = f'<img src="{image}" alt="{name}" width="400" height="440" loading="lazy">' if (ROOT/image.lstrip('/')).exists() else f'<div class="team-monogram" aria-hidden="true">{monogram}</div>'
        team += f'<li><article class="team-card">{portrait}<span class="eyebrow">{initials}</span><h3>{name}</h3><p class="team-role">{role}</p><p>{description}</p></article></li>'
    team += '</ol></li></ol></section><section class="cta"><h2>Expertise connected around your business.</h2><p>Meet the team behind your next software, communications or commerce project.</p><a class="button light" href="/contact.html">Start a conversation</a></section>'
    write('team.html',shell('team.html','Team & Organogram','Meet Shahid Rasool, Chief Executive Officer & Head of Technical Operations, Muhammad Soban, Co Founder & eCommerce Specialist, and the managers leading outsourcing, business development and customer success.',team))

    cred_items=[('Corporate identity','UCIN 0226235','SRLINES SOFTWARE HOUSE (SMC-PRIVATE) LIMITED.'),('PSEB registration','IT Company: Z-25-22334/26','Pakistan Software Export Board IT Company registration.'),('PSEB registration','Call Center/BPO: C05/PSEB/2026/8766','Pakistan Software Export Board Call Center/BPO registration.'),('Company registration','SECP incorporation','View our incorporation record through the official SECP verification service.'),('Published application','wCRM Android app','Explore the official wCRM Android application on Google Play.'),('Certificate artifact','Meta Technology Provider','The certificate PDF is retained on this website. Buyers should confirm whether the status remains current in the relevant Meta portal.'),('Partner tier artifact','Meta badged partner','The archived tier badge records a previously published partner tier; current status requires owner and platform verification.'),('Programme participation','Meta Partner Performance Accelerator','An archived image records programme participation; this is distinct from a current company partner tier.'),('Technical integration','WhatsApp Cloud API','wCRM connects customer communication workflows through official Meta APIs.')]
    credentials=hero('Company and product references','A registered company. A professional delivery partner.','Our corporate identity, PSEB registrations and published product references support informed business decisions. Explore our records and supporting documents below.')+'''<section class="section"><div class="credential-grid">'''+''.join(f'<article><span>{a}</span><h2>{b}</h2><p>{c}</p></article>' for a,b,c in cred_items)+'''</div><div class="verification-links"><a href="https://eservices.secp.gov.pk/eServices/ControllerServlet?request_id=VERIFY_ONLINE_INCORP_CERT&amp;id=0226235" target="_blank" rel="noopener noreferrer"><strong>SECP incorporation verification</strong><span>Official verification destination supplied for incorporation record 0226235. This shows registration, not endorsement of service quality.</span></a><a href="https://play.google.com/store/apps/details?id=net.srlines.wcrm" target="_blank" rel="noopener noreferrer"><strong>wCRM Android app on Google Play</strong><span>View the published application listing.</span></a><a href="/Meta%20Tech%20Provider%20Certificate.pdf" target="_blank" rel="noopener noreferrer"><strong>Meta Technology Provider certificate (PDF)</strong><span>Archived certificate evidence; confirm current platform status during procurement.</span></a><a href="/Current%20Tier%20Badged.png" target="_blank" rel="noopener noreferrer"><strong>Meta partner tier badge (archived image)</strong><span>Previously published tier evidence; not represented here as a current status.</span></a><a href="/Meta%20Partner%20Performance%20Accelerator.png" target="_blank" rel="noopener noreferrer"><strong>Meta Partner Performance Accelerator</strong><span>Previously published programme-participation artwork.</span></a></div></section>'''
    write('credentials.html',shell('credentials.html','Credentials & Partnerships','Review SRLINES registrations, partner relationships, published listings and technical integrations with clear qualifications.',credentials))

    service_cards=[]
    for slug,title,tag,audience,deliver,needs,faqs in services:
        service_cards.append(('Service',title,tag,f'<a href="/services/{slug}.html">Learn more →</a>'))
        body=hero('Professional service',title,tag,'<div class="actions"><a class="button" href="/contact.html?service='+slug+'">Request a Quote</a></div>')
        body+=f'''<section class="section"><div class="split"><div><span class="eyebrow">Business problem</span><h2>Move from an unclear requirement to an accountable delivery plan.</h2><p>{audience}</p><p>Discovery identifies the current constraint, intended users, dependencies and a useful definition of done before implementation.</p></div><div><span class="eyebrow">Scope &amp; deliverables</span><h2>What the engagement can cover</h2><ul class="checks">{''.join('<li>'+escape(x)+'</li>' for x in deliver)}</ul></div></div></section><section class="section tinted"><div class="section-title"><span class="eyebrow">Delivery process</span><h2>A transparent path from brief to handover.</h2></div>'''+cards([('01','Discover','Confirm goals, users, systems, risks and success criteria.'),('02','Define','Agree deliverables, responsibilities, review points and quotation.'),('03','Deliver','Implement in reviewable stages and test against the agreed scope.'),('04','Handover','Launch or transfer with documentation and clearly scoped support.')])+f'''</section><section class="section split"><div><h2>What you provide</h2><p>{needs}</p></div><div><h2>Relevant SRLINES experience</h2><p>Our wCRM integrations and selected <a href="/portfolio/index.html">client projects</a> demonstrate experience connecting interfaces, data and operational workflows. Relevance is confirmed during discovery rather than assumed.</p></div></section>'''+faq(faqs)+'''<section class="cta"><h2>Discuss your requirements.</h2><p>Share the business problem and available systems. We will respond with questions and a tailored proposal and clear next steps.</p><a class="button light" href="/contact.html">Discuss Your Project</a></section>'''
        write(f'services/{slug}.html',shell(f'services/{slug}.html',title,tag+' Scope, process, client inputs and service-specific FAQs.',body,title, entities=(service(f'/services/{slug}.html', title, tag),), faqs=faqs))
    overview=hero('Professional services','Technology and operational support, scoped around your business.','Choose a specialist service or start with the problem. Each engagement begins with requirements, dependencies and a quotation.')+'<section class="section">'+cards(service_cards)+'</section>'
    write('services/index.html',shell('services/index.html','Services','Explore SRLINES software development, advertising, consultancy, n8n deployment and automation services.',overview,'Services'))

    build_voice()
    build_commerce()
    prod_cards=[]
    for slug,title,tag,kind,desc,url,cta in products:
        prod_cards.append((kind,title,desc,f'<a href="/products/{slug}.html">View details →</a>'))
        body=hero('wCRM ecosystem · '+kind,title,tag,f'<div class="actions"><a class="button" href="{url}" target="_blank" rel="noopener noreferrer">{cta}</a><a class="button secondary" href="/contact.html">Request a Demo</a></div>')
        body+=f'''<section class="section split"><div><span class="eyebrow">Position in the ecosystem</span><h2>A connected part of your customer workflow.</h2><p>{desc}</p><p>This page describes the <strong>{kind.lower()}</strong> within the company-owned wCRM ecosystem.</p></div><div><h2>Plan the right setup</h2><ul class="checks"><li>Confirm the operational use case</li><li>Review required platform accounts and permissions</li><li>Map customer consent and data responsibilities</li><li>Agree onboarding or integration support</li></ul></div></section><section class="cta"><h2>See whether this fits your workflow.</h2><a class="button light" href="{url}" target="_blank" rel="noopener noreferrer">{cta}</a></section>'''
        if slug == "wcrm":
            body += '<section class="section"><h2>Connect voice calls with wCRM</h2><p>Explore how the <a href="/products/srlines-pbx.html">AI Calling Agent and AI-enabled PBX</a> can route calls and link agreed call activity with customer workflows.</p></section>' + wcrm_resources()
        fields = {"genre": "Android business software"} if slug == "wcrm-mobile" else {}
        write(f'products/{slug}.html', shell(f'products/{slug}.html', title, desc, body, title,
              entities=(software(f'/products/{slug}.html', title, desc, **fields),)))
    overview=hero('SRLINES product portfolio','Connected communications. Branded commerce. Smarter operations.','Explore our flagship AI Calling Agent and AI-enabled PBX, the wCRM ecosystem and branded mobile commerce.')+flagship_section()+'<section class="section">'+cards(prod_cards)+'</section>'
    write('products/index.html',shell('products/index.html','Products & wCRM Ecosystem','Compare SRLINES AI Calling Agent and AI-enabled PBX, wCRM, Shopify mobile commerce and business integrations.',overview,'Products'))

    p_cards=[]
    for slug,title,tag,desc,cat in portfolio:
        p_cards.append((cat.title(),title,tag,f'<a href="/portfolio/{slug}.html">Read project profile →</a>'))
        body=hero('Client project · Developed for a client',title,tag,'<div class="actions"><a class="button" href="/contact.html">Discuss a similar project</a><a class="button secondary" href="/portfolio/index.html">All client projects</a></div>')
        body+=f'''<section class="section split"><div><h2>Project context</h2><p>{desc}</p></div><div><h2>Implementation perspective</h2><p>Project information reflects the published delivery profile. Detailed client, feature and outcome information is shared only when authorised and relevant to a prospective engagement.</p></div></section>'''
        write(f'portfolio/{slug}.html',shell(f'portfolio/{slug}.html',title+' — Client Project',tag+' A client project developed by SRLINES.',body,title))
    overview=hero('Portfolio','Selected client projects, clearly separated from SRLINES products.','SignSyncer, FormSyncer and Whatsell were developed for clients. Their brands and businesses are not presented as owned by SRLINES.')+'''<section class="section"><div class="filters" aria-label="Filter client projects"><button class="active" data-filter="all">All</button><button data-filter="web">Web</button><button data-filter="automation">Automation</button><button data-filter="commerce">Commerce</button></div><div class="cards portfolio-grid">'''+''.join(f'<article data-category="{cat}"><span>Client project</span><h3>{title}</h3><p>{tag}</p><a href="/portfolio/{slug}.html">View client project →</a></article>' for slug,title,tag,desc,cat in portfolio)+'''</div></section><section class="section tinted"><div class="section-title"><span class="eyebrow">wCRM customer implementations</span><h2>Case studies recovered from the July 2026 website.</h2><p>These are customer uses of SRLINES' company-owned wCRM product, not additional SRLINES-owned products. Reported results should be reconfirmed during procurement.</p></div><div class="evidence-grid"><article><span>REBC · Real estate</span><h3>Lead and property update automation</h3><p>SRLINES previously published a deployment of segmented broadcast campaigns, enquiry automation and follow-up sequences, reporting 3× faster lead response and 70% less manual workload.</p></article><article><span>BLXCK · Ecommerce</span><h3>Shopify notification workflows</h3><p>SRLINES previously published a Shopify-connected implementation for order notifications, abandoned-cart follow-up and product enquiries, reporting 40% cart recovery.</p></article><article><span>TotalLink · IT & telecom</span><h3>n8n support automation</h3><p>SRLINES previously published ticket, onboarding and resolution-notification workflows using wCRM and n8n, reporting 3× support capacity with the same resources.</p></article></div></section>'''
    write('portfolio/index.html',shell('portfolio/index.html','Client Project Portfolio','Explore SignSyncer, FormSyncer and Whatsell as client projects developed by SRLINES—not company-owned products.',overview,'Portfolio'))

    industries=[('real-estate','Real Estate Solutions','Connect property enquiries, sales follow-up and campaign workflows.','Developers, agencies and property teams can combine responsive web experiences, advertising operations, workflow automation and wCRM conversation management.'),('ecommerce','Ecommerce Solutions','Connect storefront activity with customer communication.','Launch a Shopify-connected mobile shopping app with your own brand, a web-based admin panel and synchronized products and orders. Connect customer conversations through wCRM and your sales or support teams through SRLINES PBX.'),('isp','ISP Solutions','Build clearer customer and operational workflows for ISPs.','Internet service providers can explore customer portals, enquiry management, payment-related integrations and automated service workflows, subject to available systems and permissions.')]
    for slug,title,tag,text in industries:
        body=hero('Industry solutions',title,tag,'<div class="actions"><a class="button" href="/contact.html">Request a Quote</a></div>')+f'''<section class="section split"><div><h2>Where we can help</h2><p>{text}</p></div><div><h2>Possible building blocks</h2><ul class="checks"><li>Website or application delivery</li><li>wCRM customer-conversation workflows</li><li>n8n integration and automation</li><li>Digital advertising and measurement support</li></ul></div></section><section class="cta"><h2>Map a solution around your systems.</h2><a class="button light" href="/contact.html">Discuss Your Project</a></section>'''
        body += '<section class="section"><h2>Handle calls and enquiries</h2><p><a href="/products/srlines-pbx.html">Explore SRLINES AI Calling Agent and AI-Enabled PBX</a> for business telephone routing and CRM-connected workflows.</p></section>'
        write(f'industries/{slug}.html',shell(f'industries/{slug}.html',title,tag,body,title))

    contact=hero('Contact SRLINES','Tell us what needs to work better.','Request an AI Calling Agent and PBX consultation or quotation, explore wCRM and branded commerce, or outline an integration requirement.')+f'''<section class="section contact-layout"><form id="contact-form" action="mailto:{EMAIL}" method="post" enctype="text/plain" novalidate><h2 data-enquiry-heading>Request a quote</h2><p>Tell us the outcome you need and the systems involved. We will review your enquiry and reply with clarifying questions or a suitable next step.</p><label>Name <input name="name" autocomplete="name" required></label><label>Business email <input type="email" name="email" autocomplete="email" required></label><label>Phone <input type="tel" name="phone" autocomplete="tel"></label><label>Area of interest <select name="interest" required><option value="">Choose one</option><option value="SRLINES PBX">AI Calling Agent &amp; PBX</option><option>wCRM</option><option>Software development</option><option>Shopify Integrated Mobile App</option><option>Automation / n8n</option><option>Digital advertising</option><option>NTN consultancy</option><option>Meta verification consultancy</option></select></label><label class="full">Project or requirement <textarea name="message" rows="6" required></textarea></label><label class="trap" aria-hidden="true">Website<input name="wcrm_website" tabindex="-1" autocomplete="off"></label><button class="button" type="submit">Send Request</button><div class="form-status" data-wcrm-result role="status" aria-live="polite"></div></form><aside><h2>Direct contact</h2><p><a href="mailto:{EMAIL}">{EMAIL}</a></p><p><a href="tel:{PHONE}">{UAN}</a></p><p><a href="{WHATSAPP}" target="_blank" rel="noopener noreferrer">Chat on WhatsApp</a></p><p>{LOCATION}</p><p><a href="/privacy.html">Read our privacy policy</a></p><p class="notice">Do not send passwords or secret API keys through this form. Access requirements are agreed after scope and identity are confirmed.</p></aside></section><script src="https://crm.srlines.net/form-widget.js" data-form-id="wf_n7XM70piQmFNx5ZJY7kfckWj" data-form-selector="#contact-form" defer></script>'''
    write('contact.html',shell('contact.html','Contact / Request a Quote','Contact SRLINES for an AI Calling Agent, PBX, software, automation or wCRM quotation.',contact,'Contact'))

    privacy=hero('Legal','Privacy Policy','How SRLINES handles information submitted through this website and related enquiries.')+'''<article class="legal"><h2>Information we receive</h2><p>We may receive identity, contact, business and project information you submit, plus ordinary technical request data produced when a website is accessed.</p><h2>Why it is used</h2><p>Information may be used to respond to enquiries, prepare quotations, provide requested services, protect systems and meet legal obligations.</p><h2>Forms and processors</h2><p>The quotation form uses the existing wCRM form integration hosted at crm.srlines.net. Its availability and submission confirmation determine whether a form request was received. You may instead email us.</p><h2>Sharing and retention</h2><p>Information is shared only where needed for service delivery, legal compliance or a processor acting on our behalf. Retention depends on the enquiry, contract and applicable requirements.</p><h2>Your choices</h2><p>Contact <a href="mailto:contact@srlines.net">contact@srlines.net</a> with a relevant privacy request. Rights and exceptions depend on applicable law.</p><p><strong>Last updated:</strong> 30 September 2026.</p></article>'''
    terms=hero('Legal','Terms of Service','General website and enquiry terms. A signed proposal or service agreement controls project-specific delivery.')+'''<article class="legal"><h2>Website information</h2><p>Website content is general information and may change. Marketplace, platform and government decisions remain controlled by their respective operators.</p><h2>Services and quotations</h2><p>Scope, fees, access, delivery responsibilities, intellectual property, support and acceptance criteria are established in the applicable quotation or agreement. No completion date or price is implied by this website.</p><h2>Consultancy limitations</h2><p>NTN and Meta verification services provide preparation and guidance. SRLINES is not a government authority and cannot guarantee registration, verification, approval or platform decisions.</p><h2>Third-party services</h2><p>External platforms have their own terms, charges and availability. Customers remain responsible for authorised access, lawful data use and compliance relevant to their operations.</p><h2>Contact</h2><p>Questions may be sent to <a href="mailto:contact@srlines.net">contact@srlines.net</a>.</p><p><strong>Last updated:</strong> 30 September 2026.</p></article>'''
    write('privacy.html',shell('privacy.html','Privacy Policy','SRLINES website privacy policy covering enquiries, forms, use, sharing and choices.',privacy,'Privacy'))
    write('terms.html',shell('terms.html','Terms of Service','General SRLINES website, quotation, consultancy and third-party service terms.',terms,'Terms'))

    notfound=hero('404','That page could not be found.','The address may have changed, or the page may no longer be public. Use the links below to continue.','<div class="actions"><a class="button" href="/">Go home</a><a class="button secondary" href="/contact.html">Contact SRLINES</a></div>')
    write('404.html',shell('404.html','Page Not Found','The requested SRLINES page could not be found.',notfound,'404'))

    complete_public_site(ROOT, write)

if __name__ == '__main__': build()
