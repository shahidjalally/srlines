#!/usr/bin/env python3
"""Validate canonical public HTML, its crawl files and shared SRLINES identity."""
from collections import Counter
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urljoin, urlsplit
from urllib.robotparser import RobotFileParser
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from site_identity import DOMAIN, PBX, PHONE, company_graph  # noqa: E402
from voice_content import LANDINGS  # noqa: E402

OBSOLETE = re.compile(r"(?<!\d)(?:(?:\+?92|0092)[\s().-]*|0)311[\s().-]*110[\s().-]*1996(?!\d)")


class PageParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.assets = []
        self.ids = set()
        self.title = ""
        self.meta = {}
        self.canonical = ""
        self.h1 = 0
        self.generated = False
        self.schema = []
        self.capture = ""

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "body" and "data-path" in attrs:
            self.generated = True
        if attrs.get("id"):
            self.ids.add(attrs["id"])
        if tag == "a" and attrs.get("href"):
            self.links.append(attrs)
        if tag in ("img", "script", "iframe", "source") and attrs.get("src"):
            self.assets.append(attrs["src"])
        if tag == "title":
            self.capture = "title"
        if tag == "meta":
            self.meta[attrs.get("name") or attrs.get("property")] = attrs.get("content", "")
        if tag == "link" and attrs.get("rel") == "canonical":
            self.canonical = attrs.get("href", "")
        if tag == "h1":
            self.h1 += 1
        if tag == "script" and attrs.get("type") == "application/ld+json":
            self.capture = "schema"

    def handle_data(self, data):
        if self.capture == "title":
            self.title += data
        if self.capture == "schema":
            self.schema.append(data)

    def handle_endtag(self, tag):
        if tag in ("script", "title"):
            self.capture = ""


def path_for(url):
    path = unquote(urlsplit(url).path)
    file = ROOT / path.lstrip("/")
    return file / "index.html" if path.endswith("/") else file


def sitemap_urls(file):
    return [entry.text for entry in ET.parse(file).findall("{*}url/{*}loc")]


def main():
    failures = []
    pages = {}
    public = set()
    for file in ROOT.rglob("*.html"):
        parts = file.relative_to(ROOT).parts
        if any(part.startswith(".") for part in parts) or parts[0] in {
            "docs", "tests", "content", "contact-form-widget",
        }:
            continue
        raw = file.read_text(encoding="utf-8")
        page = PageParser()
        page.feed(raw)
        if OBSOLETE.search(raw):
            failures.append(f"Obsolete UAN: {file}")
        if "noindex" in page.meta.get("robots", ""):
            assert file.name == "404.html", file
            continue
        assert page.canonical.startswith(DOMAIN + "/"), file
        url = page.canonical
        assert path_for(url) == file and url not in pages, url
        pages[url] = page
        public.add(url)
        if not page.title.strip() or not page.meta.get("description") or page.h1 != 1:
            failures.append(f"Missing metadata or incorrect H1 count: {url}")
        for link in page.links:
            href = link["href"]
            if page.generated and href.startswith(("http://", "https://")):
                assert link.get("target") == "_blank" and {"noopener", "noreferrer"} <= set(link.get("rel", "").split()), (url, href)
            if link["href"].startswith("tel:") and link["href"].startswith(("tel:+92311110", "tel:0311110")):
                assert link["href"] == "tel:" + PHONE, (url, link)
        try:
            assert len(page.schema) == 1
            graph = json.loads(page.schema[0])["@graph"]
            ids = [node["@id"] for node in graph if "@id" in node]
            assert len(ids) == len(set(ids))
            assert graph[:4] == company_graph()
            webpage = next(node for node in graph if node.get("@id") == url + "#webpage")
            assert webpage["publisher"] == {"@id": DOMAIN + "/#organization"}
            assert webpage["url"] == url and webpage["isPartOf"] == {"@id": DOMAIN + "/#website"}
        except (AssertionError, KeyError, ValueError, StopIteration):
            failures.append(f"Invalid structured data: {url}")

    sitemap = sitemap_urls(ROOT / "sitemap.xml")
    assert set(sitemap) == public and len(sitemap) == len(public), "Sitemap coverage mismatch"
    for file in ROOT.glob("*-sitemap.xml"):
        urls = sitemap_urls(file)
        assert len(urls) == len(set(urls)) and set(urls) <= public, file
    duplicates = [title for title, count in Counter(p.title for p in pages.values()).items() if count > 1]
    assert not duplicates, duplicates

    crawler = RobotFileParser()
    crawler.parse((ROOT / "robots.txt").read_text().splitlines())
    for url in [DOMAIN + "/", DOMAIN + PBX, *(DOMAIN + path for path in LANDINGS)]:
        assert url in public, url
        assert pages[url].meta["og:url"] == url
        for agent in ("OAI-SearchBot", "ChatGPT-User", "Googlebot", "Bingbot"):
            assert crawler.can_fetch(agent, url), (agent, url)

    navigation = {url: set() for url in pages}
    for url, page in pages.items():
        for href in [*(link["href"] for link in page.links), *page.assets]:
            target = urlsplit(urljoin(url, href))
            if target.scheme not in {"http", "https"} or target.netloc != urlsplit(DOMAIN).netloc:
                continue
            target_url = DOMAIN + (target.path or "/")
            if target_url in pages and any(link["href"] == href for link in page.links):
                navigation[url].add(target_url)
            if not path_for(target_url).is_file():
                failures.append(f"Broken internal reference: {url} → {href}")
            if target.fragment and target_url in pages and unquote(target.fragment) not in pages[target_url].ids:
                failures.append(f"Broken internal anchor: {url} → {href}")

    reachable = set()
    pending = [DOMAIN + "/"]
    while pending:
        url = pending.pop()
        if url not in reachable:
            reachable.add(url)
            pending.extend(navigation[url] - reachable)
    assert reachable == public, f"Orphan pages: {sorted(public - reachable)}"

    for path in ("site_identity.py", "site_legacy.py", "build_site.py", "assets/redesign.js", "llms.txt"):
        assert not OBSOLETE.search((ROOT / path).read_text()), path
    for path in ("index.html", "contact.html", "products/srlines-pbx.html"):
        page = pages[DOMAIN + "/" + path] if path != "index.html" else pages[DOMAIN + "/"]
        assert any(link["href"] == "tel:" + PHONE for link in page.links)

    # Retain the deployment checks for the existing app and team pages.
    team = (ROOT / "team.html").read_text()
    assert all(name in team for name in ("Shahid Rasool", "Muhammad Saim", "Rubab Javed", "Muhammad Sarim"))
    assert "Chief Executive Officer &amp; Head of Technical Operations" in team
    assert '<ol class="org-managers">' in team
    app = (ROOT / "products/shopify-mobile-app.html").read_text()
    assert "id=net.srlines.ecommerce" in app and "https://ecommerce.srlines.net/" in app
    for slug in ("signsyncer", "formsyncer", "whatsell"):
        profile = (ROOT / f"portfolio/{slug}.html").read_text().lower()
        assert "client project" in profile and "developed for a client" in profile

    assert not failures, "\n" + "\n".join(failures)
    print(f"Validated {len(public)} canonical pages and five sitemaps, metadata, headings, "
          "JSON-LD identity, internal links and assets, crawler access, and UAN.")


if __name__ == "__main__":
    main()
