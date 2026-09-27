#!/usr/bin/env python3
"""Small dependency-free integrity check for the static site."""

from html.parser import HTMLParser
from pathlib import Path
from typing import List, Optional, Tuple
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"


class SiteParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.ids: list[str] = []
        self.anchors: list[str] = []
        self.local_files: list[str] = []
        self.images_without_alt: list[str] = []
        self.blank_links_without_rel: list[str] = []
        self.h1_count = 0
        self.title_count = 0

    def handle_starttag(self, tag: str, attributes: List[Tuple[str, Optional[str]]]) -> None:
        attrs = dict(attributes)
        if element_id := attrs.get("id"):
            self.ids.append(element_id)
        if tag == "a" and (href := attrs.get("href")):
            if href.startswith("#"):
                self.anchors.append(href[1:])
            if attrs.get("target") == "_blank" and "noreferrer" not in (attrs.get("rel") or ""):
                self.blank_links_without_rel.append(href)
        if tag in {"link", "script", "img"}:
            reference = attrs.get("href") if tag == "link" else attrs.get("src")
            if reference and not urlparse(reference).scheme and not reference.startswith(("#", "//")):
                self.local_files.append(reference)
        if tag == "img" and "alt" not in attrs:
            self.images_without_alt.append(attrs.get("src") or "<missing src>")
        if tag == "h1":
            self.h1_count += 1
        if tag == "title":
            self.title_count += 1


def main() -> None:
    parser = SiteParser()
    parser.feed(INDEX.read_text(encoding="utf-8"))

    duplicate_ids = sorted({item for item in parser.ids if parser.ids.count(item) > 1})
    missing_anchors = sorted({anchor for anchor in parser.anchors if anchor and anchor not in parser.ids})
    missing_files = sorted({item for item in parser.local_files if not (ROOT / item).exists()})

    errors = {
        "duplicate ids": duplicate_ids,
        "missing internal anchors": missing_anchors,
        "missing local files": missing_files,
        "images without alt": parser.images_without_alt,
        "target=_blank links without noreferrer": parser.blank_links_without_rel,
    }
    errors = {label: values for label, values in errors.items() if values}

    if parser.h1_count != 1:
        errors["h1 count (expected 1)"] = [str(parser.h1_count)]
    if parser.title_count != 1:
        errors["title count (expected 1)"] = [str(parser.title_count)]

    if errors:
        for label, values in errors.items():
            print(f"ERROR: {label}: {', '.join(values)}")
        raise SystemExit(1)

    print(
        "Site integrity checks passed: "
        f"{len(parser.ids)} ids, {len(parser.anchors)} internal links, "
        f"{len(parser.local_files)} local assets."
    )


if __name__ == "__main__":
    main()
