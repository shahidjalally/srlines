# SRLINES AI calling website implementation

## Scope and changes

SRLINES AI Calling Agent and AI-Enabled PBX now leads the homepage, product roster, desktop and mobile navigation, and shared footer. The homepage explains how voice workflows work, displays the product diagram and official demo, introduces use cases and links to the secondary catalog. Legacy portfolio and product routes remain available. Older wCRM testimonials and delivery metrics were removed from the homepage lead-in as part of the product repositioning.

The existing PBX canonical remains `/products/srlines-pbx.html`. It covers conversational AI and IVR, Urdu and English, inbound and outbound calling, human transfer, SIP and UAN, CRM, recording, deployment, privacy and quotation-based pricing. Six new pages address AI calling, AI reception, restaurants, hospitals and clinics, schools and colleges, and commercial pricing. Industry workflows distinguish a request for staff from a confirmed booking or order.

The 12 [Hugo-ready articles](../content/blog/README.md) cover technical, commercial and industry questions with contextual links. They are unpublished. The main site's sitemap contains public canonicals only.

## Sitewide identity, SEO and conversion

- Corrected call, display, structured-data and WhatsApp references to the owner-confirmed UAN. Preserved independent third-party numbers. Public identity and contact values live in `site_identity.py`.
- Added the shared Organization, ContactPoint, WebSite, OfferCatalog and page graphs. Connected product, service, visible FAQ, breadcrumb and video nodes to stable IDs. Retained special partner and editorial markup where supported. Removed unsupported offers from legacy markup.
- Expanded the main sitemap from 32 to 74 URLs. Rebuilt four supplemental maps as canonical subsets and excluded the 404, stale paths and fragment-only entries. Existing broad robots access continues. Production crawler review is a separate step.
- Added metadata and Open Graph images for voice routes, fixed broken legacy industry and partner links and linked legacy guides through wCRM. Added canonical product discovery summaries to `llms.txt` and the two existing discovery aliases.
- Used the existing contact form for consultation and quote entry points and retained its submission integration, payload, lead analytics and WhatsApp tracking. The product CTA preselects the existing SRLINES PBX interest value.
- Reused the real PBX diagram with a 141 KB WebP derivative of the 1.87 MB source. Added sized images and a lazy, aspect-ratio video embed with a direct fallback. Improved mobile drawer keyboard focus and fixed tablet overflow in the delivery grid.

## Files and validation

Added the six commercial HTML routes, the WebP product visual, the three Python identity/content/legacy modules, one discovery file, 12 editorial drafts and their handoff, and six project documents. Modified the generator, existing site HTML, redesign CSS and JavaScript, four supplemental sitemaps and the primary sitemap, robots file, discovery aliases, ignore rules and validation script. GitHub Pages branch, custom domain, product portals and contact backend settings are retained.

The build, `python tests/validate_site.py`, `node --check assets/redesign.js` and `git diff --check` passed. The validator covers canonical resolution and coverage, duplicate titles, descriptions, H1s, coherent JSON-LD, local links and assets, crawler visibility and UAN. Two consecutive builds produced identical public files. Chromium checks passed on 11 representative pages at 320, 390, 768, 1024 and 1440 pixels and covered keyboard drawer behaviour, consultation preselection, invalid-form handling and simulated lead and WhatsApp events. Browser tests use local HTML and block external submission and analytics. OCR checked 42 tracked raster and PDF assets and found no detectable obsolete UAN. Video frames and OCR false negatives remain possible.

## Owner and production follow-up

- Pricing is quotation-based. Confirm approved rates, allowances, concurrency and taxes if publishing packages later.
- Confirm Calendly is current before replacing the on-site consultation route. Verify the demo's official metadata, public playback and embed permissions.
- Supply the exact supported Asterisk/OpenAI deployment arrangements, carrier or Zong service terms, and approved tenant, access and retention details for any narrower public claims.
- Check live form receipt, production field performance and Cloudflare crawler access after the Pages deployment. Submit indexing requests and update external profiles using authorized accounts.
- Follow [the launch and rollback checklist](POST-DEPLOYMENT-CHECKLIST.md). The pull request is the review and merge boundary. Merging triggers branch-based Pages publishing.
