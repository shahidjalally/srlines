# SRLINES structured data architecture

Every canonical public HTML page carries one static JSON-LD graph. [site_identity.py](../site_identity.py) owns the common nodes and serialization. [build_site.py](../build_site.py) adds page-specific context. [site_legacy.py](../site_legacy.py) reconciles the hand-maintained pages while preserving specific editorial entities, including profiles and service descriptions.

| Entity | Stable identifier |
| --- | --- |
| SRLINES Organization and local ProfessionalService | `https://srlines.net/#organization` |
| Public contact point | `https://srlines.net/#contact` |
| Website | `https://srlines.net/#website` |
| Catalog | `https://srlines.net/#catalog` |
| WebPage, AboutPage, ContactPage, ProfilePage or CollectionPage | Canonical URL plus `#webpage` |
| BreadcrumbList | Canonical URL plus `#breadcrumb` |
| SoftwareApplication | Product canonical plus `#software` |
| Service | Offering canonical plus `#service` |
| Visible FAQ | Canonical URL plus `#faq` |
| Official PBX demonstration | PBX canonical plus `#demo-video` |

The shared contact point carries the E.164 UAN. The Organization contains the headquarters, published registration references and established company social links. The catalog references software and implementation services. Product and service pages use the company as publisher, creator or provider as applicable. The voice landing pages reference the flagship software even when the local page describes a distinct deployment service.

Organization and website definitions are identical across the site. Generated FAQ text and markup share the same data. Breadcrumb labels mirror visible navigation. The demo graph uses the supplied video identifier and embed URL. Confirm the upload date, runtime, official title and thumbnail in YouTube Studio before completing Google's video eligibility inputs. The pricing page uses quotation language and has no price or Offer node. External Hugo articles should emit BlogPosting markup using real publication dates when published.

Validate syntax and relationships with `python tests/validate_site.py`. After publication, use the [Schema.org Validator](https://validator.schema.org/) and [Google Rich Results Test](https://search.google.com/test/rich-results) separately. FAQ markup describes visible content. Google limits FAQ rich results to eligible authoritative government and health sites.
