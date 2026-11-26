# SRLINES structured data architecture

Every canonical public HTML page carries one static JSON-LD graph. [site_identity.py](../site_identity.py) owns the common nodes and serialization. [build_site.py](../build_site.py) adds page-specific context. [site_legacy.py](../site_legacy.py) reconciles hand-maintained pages while preserving profiles and editorial entities.

| Entity | Stable identifier |
| --- | --- |
| SRLINES LocalBusiness | `https://srlines.net/#organization` |
| Public contact point | `https://srlines.net/#contact` |
| Website | `https://srlines.net/#website` |
| Featured product ItemList | `https://srlines.net/#catalog` |
| WebPage, AboutPage, ContactPage, ProfilePage or CollectionPage | Canonical URL plus `#webpage` |
| BreadcrumbList | Canonical URL plus `#breadcrumb` |
| Software description | Product canonical plus `#software` for generated pages |
| Service | Offering canonical plus `#service` |
| Visible FAQ | Canonical URL plus `#faq` |
| Official PBX demonstration when upload metadata is available | PBX canonical plus `#demo-video` |

## Website-wide review after PR #40

- The PBX page describes the managed voice platform as a Service and preserves the software identity as a CreativeWork. Other generated and legacy product descriptions use CreativeWork with stable names and IDs. This preserves the entity links. Google's SoftwareApplication feature requires a real priced offer and a qualifying review or rating. The site has no verified on-page data to support those fields for these apps. Two unsupported free-price values were removed from the partner MOU markup. [Google software app requirements](https://developers.google.com/search/docs/appearance/structured-data/software-app)
- The homepage and PBX page keep the official YouTube embed and fallback link. The generator emits VideoObject when `VIDEO_UPLOAD_DATE` in [voice_content.py](../voice_content.py) contains the original public publication date supplied by the uploader. The uploader supplied a relative publication date that resolves to `2026-11-13`. The ISO 8601 date uses day precision. [Google video requirements](https://developers.google.com/search/docs/appearance/structured-data/video)
- The company uses the supported LocalBusiness type with the same company ID, headquarters, registration references and E.164 UAN. The partner directory lists profile pages through ItemList. The profile pages identify the person and, where already established, their company. The partner disclaimer is a page element.
- Generated FAQ text and markup share the same data. Four stale legacy FAQ blocks were removed where the questions and answers differed from the visible pages. The remaining FAQs describe visible content for Schema.org consumers. Google retired the FAQ rich result in May 2026. [Google Search documentation updates](https://developers.google.com/search/updates)
- Breadcrumb labels mirror visible navigation. The noindex error page omits JSON-LD. The unpublished Hugo articles can use BlogPosting markup with actual publication dates when published.

Run `python build_site.py` and `python tests/validate_site.py` before release. Checks cover all 74 canonicals, nested rich-result fields, visible FAQ text, graph references and consistency of shared IDs. A separate vocabulary audit used Schema.org 29.4 to check typed properties against their documented domains and ranges. After deployment, run [Google's Rich Results Test](https://search.google.com/test/rich-results) and the [Schema.org Validator](https://validator.schema.org/) separately. Google determines eligibility and display based on the page and its content.
