# SRLINES website audit

## Baseline

The implementation starts from GitHub `main` at `bef9a59`. The checkout was clean. The original validation script passed its 32-page sitemap check. The repository contains source and ready-to-publish HTML, CSS and JavaScript. `build_site.py` generates the shared redesign without a package manager. GitHub Pages publishes checked-in files from the production branch using `CNAME` and `.nojekyll`. There was no repository-managed Actions workflow in this checkout.

| Area | Confirmed finding |
| --- | --- |
| Flagship | The homepage title and heading led with software and integration. The PBX product had a generic heading, a short call-routing summary and a consultation link. wCRM, PBX and branded commerce were all presented as flagships in different places. |
| Coverage | The repository contained 69 HTML files, 68 with indexable public canonicals. The main sitemap listed 32. The 36 supplemental product, partner, sector and WhatsApp pages sat outside the primary sitemap. The four supplemental XML maps included fragments, other hosts and obsolete paths. |
| Head and schema | Shared pages emitted a minimal WebPage object. Hand-maintained pages repeated Organization and WebSite definitions with different descriptions and contact properties. Five partner pages used the SRLINES masthead as an extra H1. |
| Links | Legacy industry links pointed at removed home fragments. Partner privacy and terms links targeted old filenames. Several WhatsApp and integration guides were outside the main navigation. |
| Identity | The shared footer and contact page showed the incorrect UAN. The Shopify app CTA used the same incorrect WhatsApp number. Other numbers appear in partner and third-party contexts. |
| Conversion | The contact form uses the hosted wCRM widget, browser validation and a mailto fallback. OpenAI Ads measures the existing successful lead event and WhatsApp link clicks. No Calendly link was found in the repository. |
| Content | The public blog is a separate Hugo site. Its current home page emphasizes WhatsApp automation. This checkout contains no Hugo configuration or blog source. |
| Experience | The redesign already uses static semantic sections, responsive grids, local system fonts, deferred scripts and reduced-motion styles. The original PBX infographic is 1.87 MB. A Chromium tablet test exposed a fixed-column delivery grid that overflowed. |
| Crawling | The original robots file allowed all agents. GitHub Pages serves these files. Live Cloudflare crawler rules, redirects and response headers require production inspection. |
| Evidence | The original PBX page documents SIP, IVR, team extensions, recording and reports. The owner confirmed production Urdu, outbound calling, human transfer and wCRM integration. Current approved rates and deployment-specific carrier details were unavailable. |

The canonical URL inventory is now generated in [sitemap.xml](../sitemap.xml). Exclusions cover the 404 page and non-site file trees. The optional XML maps are canonical subsets. Main-site HTML and generated JavaScript were reviewed for company contact references. The public blog and documentation portal have separate source and deployment processes.

## Evidence for follow-up

- Repository references include the SECP verification link, PSEB identifiers, Meta authority page and technology provider certificate.
- The supplied YouTube URL reaches the watch page. The browser evidence available during this audit did not establish its official upload date or runtime.
- Google, Bing and AI search indexing outcomes will be measured after merge and publication. See the [post-deployment checklist](POST-DEPLOYMENT-CHECKLIST.md) and [discoverability test plan](AI-DISCOVERABILITY-TESTS.md).
