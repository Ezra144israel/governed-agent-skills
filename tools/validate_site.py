#!/usr/bin/env python3
"""Validate the local Pages HTML, links, media controls, and captions."""

from html.parser import HTMLParser
from pathlib import Path
import re
import sys
from urllib.parse import urlsplit


RESOURCE_ATTRIBUTES = {
    "audio": ("src",),
    "iframe": ("src",),
    "img": ("src", "srcset"),
    "link": ("href",),
    "script": ("src",),
    "source": ("src", "srcset"),
    "track": ("src",),
    "video": ("poster", "src"),
}
VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param", "source", "track", "wbr"}


class PageParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.tags = []
        self.problems = []
        self.local_links = []
        self.resource_urls = []
        self.videos = []
        self.tracks = []
        self.anchors = []

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        if tag not in VOID:
            self.tags.append(tag)
        for name, value in attrs:
            if name == "tabindex" and value and value.lstrip("-").isdigit() and int(value) > 0:
                self.problems.append("positive tabindex is not allowed")
        if tag == "a" and values.get("href"):
            self.anchors.append(values["href"])
            self.local_links.append(values["href"])
        if tag == "video":
            self.videos.append(values)
        if tag == "track":
            self.tracks.append(values)
        for attribute in RESOURCE_ATTRIBUTES.get(tag, ()):
            value = values.get(attribute)
            if not value:
                continue
            for candidate in value.split(",") if attribute == "srcset" else [value]:
                self.resource_urls.append(candidate.strip().split()[0])
                self.local_links.append(candidate.strip().split()[0])

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in VOID:
            self.handle_endtag(tag)

    def handle_endtag(self, tag):
        if tag in VOID:
            return
        if not self.tags or self.tags[-1] != tag:
            self.problems.append(f"unbalanced closing tag: {tag}")
            return
        self.tags.pop()

    def close(self):
        super().close()
        if self.tags:
            self.problems.append(f"unclosed tag: {self.tags[-1]}")


def is_remote(value):
    return urlsplit(value).scheme in {"http", "https", "data", "javascript"} or value.startswith("//")


def local_target(page, value):
    split = urlsplit(value)
    if split.scheme or value.startswith("//") or not split.path:
        return None
    return (page.parent / split.path).resolve()


def validate_vtt(path):
    problems = []
    text = path.read_text(encoding="utf-8")
    if not text.startswith("WEBVTT\n"):
        problems.append(f"site: caption file is not WebVTT: {path.name}")
        return problems
    timestamps = re.findall(r"(\d\d):(\d\d)\.(\d\d\d) --> (\d\d):(\d\d)\.(\d\d\d)", text)
    if not timestamps:
        problems.append(f"site: caption file has no cues: {path.name}")
        return problems
    prior = -1
    for fields in timestamps:
        start = (int(fields[0]) * 60 + int(fields[1])) * 1000 + int(fields[2])
        end = (int(fields[3]) * 60 + int(fields[4])) * 1000 + int(fields[5])
        if start < prior or end <= start:
            problems.append(f"site: caption cue timing is invalid: {path.name}")
            break
        prior = end
    return problems


def validate_site(root):
    root = Path(root).resolve()
    problems = []
    pages = sorted((root / "docs").glob("*.html"))
    if not pages:
        return ["site: no HTML pages found"]
    for page in pages:
        text = page.read_text(encoding="utf-8")
        if not text.lower().startswith("<!doctype html>"):
            problems.append(f"site: missing HTML doctype: {page.relative_to(root)}")
        parser = PageParser()
        try:
            parser.feed(text)
            parser.close()
        except Exception as error:
            problems.append(f"site: HTML parse failure in {page.relative_to(root)}: {type(error).__name__}")
            continue
        problems.extend(f"site: {page.relative_to(root)}: {item}" for item in parser.problems)
        for resource in parser.resource_urls:
            if is_remote(resource):
                problems.append(f"site: external resource load in {page.relative_to(root)}")
        if re.search(r"(?:url\s*\(|@import\s+)[^;]*https?://", text, re.IGNORECASE):
            problems.append(f"site: external CSS resource load in {page.relative_to(root)}")
        for value in parser.local_links:
            target = local_target(page, value)
            if target is not None and not target.exists():
                problems.append(f"site: broken local link in {page.relative_to(root)}: {value}")
        if page.name == "index.html":
            if len(parser.videos) != 1:
                problems.append("site: index must contain exactly one video")
            else:
                video = parser.videos[0]
                if "controls" not in video:
                    problems.append("site: video must use native keyboard-accessible controls")
                if video.get("preload") != "metadata":
                    problems.append("site: video preload must be metadata")
                if "autoplay" in video:
                    problems.append("site: video must not autoplay")
                if not video.get("poster"):
                    problems.append("site: video poster is required")
            captions = [track for track in parser.tracks if track.get("kind") == "captions"]
            if len(captions) != 1 or captions[0].get("srclang") != "en" or "default" not in captions[0]:
                problems.append("site: one default English caption track is required")
            else:
                caption_path = local_target(page, captions[0]["src"])
                if caption_path and caption_path.exists():
                    problems.extend(validate_vtt(caption_path))
            if not any("transcript" in href.lower() for href in parser.anchors):
                problems.append("site: transcript link is required")
            if "prefers-reduced-motion: reduce" not in text:
                problems.append("site: reduced-motion rule is required")
            if "@media (max-width:" not in text:
                problems.append("site: mobile layout rule is required")
            if "security.html" not in parser.anchors:
                problems.append("site: security coverage link is required")
    return problems


def main(argv=None):
    root = Path(argv[0]).resolve() if argv else Path(__file__).resolve().parents[1]
    problems = validate_site(root)
    if problems:
        for problem in problems:
            print(problem, file=sys.stderr)
        return 1
    print("site: OK (HTML, links, video controls, captions, mobile, reduced motion, local resources)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
