#!/usr/bin/env python3
"""Update docs/.pages with any new markdown files not yet listed."""

import re
from pathlib import Path

DOCS_DIR = Path(__file__).resolve().parent.parent / "docs"
PAGES_FILE = DOCS_DIR / ".pages"


def get_existing_md_files() -> set[str]:
    """Get all .md filenames in docs/ (excluding .pages)."""
    return {f.name for f in DOCS_DIR.glob("*.md")}


def parse_pages(path: Path) -> tuple[list[tuple[str | None, str]], set[str]]:
    """Parse .pages file returning (entries, listed_files).

    Each entry is (title, filename) where title is None if not specified.
    """
    entries: list[tuple[str | None, str]] = []
    listed_files: set[str] = set()
    in_nav = False
    unquoted_pat = re.compile(r"^\s*-\s+(?:(.+?):\s+)?([a-zA-Z0-9_]+\.md)$")
    quoted_pat = re.compile(r'^\s*-\s+"(.+?)":\s+([a-zA-Z0-9_]+\.md)$')

    for line in path.read_text().splitlines():
        if line.strip() == "nav:":
            in_nav = True
            continue
        if in_nav:
            m = quoted_pat.match(line) or unquoted_pat.match(line)
            if m:
                title = m.group(1).strip() if m.group(1) else None
                fname = m.group(2)
                entries.append((title, fname))
                listed_files.add(fname)
            elif not line.strip() or line.startswith(" "):
                # continuation or blank line, ignore
                pass
            else:
                # end of nav section
                in_nav = False
    return entries, listed_files


def extract_title(fname: str) -> str:
    """Extract the first H1 heading from a markdown file as the title."""
    path = DOCS_DIR / fname
    if path.exists():
        for line in path.read_text().splitlines():
            if m := re.match(r"^#\s+(.+)$", line):
                return m.group(1).strip()
    # Fallback: filename without extension
    return fname.removesuffix(".md")


def generate_pages_content(entries: list[tuple[str | None, str]]) -> str:
    """Generate .pages YAML content from entries."""
    lines = ["nav:"]
    for title, fname in entries:
        if title:
            # Quote title if it contains characters that could break YAML parsing
            if ":" in title or "#" in title or "{" in title:
                lines.append(f'  - "{title}": {fname}')
            else:
                lines.append(f"  - {title}: {fname}")
        else:
            lines.append(f"  - {fname}")
    return "\n".join(lines) + "\n"


def main():
    if not PAGES_FILE.exists():
        print(f"Error: {PAGES_FILE} not found")
        return 1

    all_md = get_existing_md_files()
    entries, listed_files = parse_pages(PAGES_FILE)

    # Remove entries for files that no longer exist
    removed = 0
    entries = [(t, f) for t, f in entries if f in all_md or (removed := removed + 1) == -1]
    if removed:
        print(f"  Removed {removed} stale entr{'ies' if removed != 1 else 'y'}")

    # Add new files not yet listed
    listed_files = {f for _, f in entries}
    new_files = sorted(all_md - listed_files)

    # Add new files before the About entry (or at end if About not found)
    about_idx = -1
    for i, (_, fname) in enumerate(entries):
        if fname == "about.md":
            about_idx = i
            break

    for fname in new_files:
        title = extract_title(fname)
        entries.insert(about_idx if about_idx >= 0 else len(entries), (title, fname))
        if about_idx >= 0:
            about_idx += 1
        print(f"  Added: {title} ({fname})")

    # Always rewrite to ensure proper formatting (e.g. quoting titles with colons)
    new_content = generate_pages_content(entries)
    if new_content != PAGES_FILE.read_text() or new_files or removed:
        PAGES_FILE.write_text(new_content)
        print(f"\nUpdated {PAGES_FILE}")
    else:
        print("All markdown files already listed in .pages")
    return 0


if __name__ == "__main__":
    exit(main())
