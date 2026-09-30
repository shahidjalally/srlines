#!/usr/bin/env python3
"""Dependency-free checks for the redesigned public sitemap."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
from xml.etree import ElementTree as ET

ROOT = Path(__file__).parents[1]
NS = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}

class PageParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links=[]; self.title=False; self.description=False; self.canonical=False; self.h1=0
    def handle_starttag(self, tag, attrs):
        a=dict(attrs)
        if tag == "a": self.links.append(a)
        if tag == "title": self.title=True
        if tag == "meta" and a.get("name") == "description": self.description=bool(a.get("content"))
        if tag == "link" and a.get("rel") == "canonical": self.canonical=bool(a.get("href"))
        if tag == "h1": self.h1 += 1

def path_for(url):
    path=unquote(urlsplit(url).path.lstrip("/"))
    return ROOT/(path or "index.html")

def main():
    tree=ET.parse(ROOT/"sitemap.xml")
    urls=[n.text for n in tree.findall("s:url/s:loc",NS)]
    assert len(urls)==30, f"expected 30 public pages, found {len(urls)}"
    failures=[]
    for url in urls:
        file=path_for(url)
        if not file.is_file(): failures.append(f"missing {file.relative_to(ROOT)}"); continue
        parser=PageParser(); parser.feed(file.read_text(encoding="utf-8"))
        if not all((parser.title,parser.description,parser.canonical)) or parser.h1 != 1:
            failures.append(f"metadata/headings: {file.relative_to(ROOT)}")
        for link in parser.links:
            href=link.get("href","")
            if href.startswith(("http://","https://")):
                if link.get("target") != "_blank" or set(link.get("rel","").split()) != {"noopener","noreferrer"}:
                    failures.append(f"external link attributes: {file.relative_to(ROOT)} {href}")
            elif href.startswith("/") and not href.startswith("//"):
                local=path_for(href)
                if not local.exists(): failures.append(f"broken internal link: {file.relative_to(ROOT)} {href}")
    # Check body labels on the three project profiles rather than relying on brand ownership inference.
    for slug in ("signsyncer","formsyncer","whatsell"):
        text=(ROOT/f"portfolio/{slug}.html").read_text(encoding="utf-8").lower()
        if "client project" not in text or "developed for a client" not in text:
            failures.append(f"portfolio ownership label: {slug}")
    assert not failures, "\n".join(failures)
    print(f"Validated {len(urls)} sitemap pages, metadata, headings, internal links, external-link safety, and portfolio labels.")

if __name__ == "__main__": main()
