"""One-time cleanup: strip LLM wrapper prose from contaminated wiki pages."""
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

WIKI_DIR = Path(__file__).resolve().parent.parent / "wiki"

WRAPPER_PROSE = [
    re.compile(r"^Wiki page (?:generated|written|created) (?:at|to) .+$", re.MULTILINE),
    re.compile(r"^The wiki page has been (?:written|created|generated) .+$", re.MULTILINE),
    re.compile(r"^Here(?:'s| is) (?:the|a) (?:wiki page|summary).+$", re.MULTILINE),
    re.compile(r"^No em dashes used throughout.+$", re.MULTILINE),
    re.compile(r"^All sections use the Obsidian wikilink format.+$", re.MULTILINE),
    # "Written to `wiki/path/file.md`." or "Written to 'path'."
    re.compile(r"^Written to [`'].+[`']\.?\s*$", re.MULTILINE),
    # Broader "Here is the generated/updated/complete ..."
    re.compile(r"^Here is the (?:generated|updated|created|complete|new|full)\b.+$", re.MULTILINE),
    # "The page synthesizes/covers/is organised..." meta-commentary
    re.compile(r"^The page (?:synthesize|cover|is organis|is complete|is structured)\w*\b.+$", re.MULTILINE),
]

DECISION_BLOCK = re.compile(
    r"^(?:\*\*)?Key (?:structural choices|decisions) made:?\*?\*?\s*\n"
    r"(?:(?:[ \t]*[-\d.*]+[ \t]+.+\n?)+)",
    re.MULTILINE,
)
DECISION_HEADER = re.compile(
    r"^(?:\*\*)?Key (?:structural choices|decisions) made:?\*?\*?\s*$",
    re.MULTILINE,
)
META_DESC = re.compile(
    r"^\*\*(?:Summary paragraph|Current State|Key structural choices)\*\*:.*$",
    re.MULTILINE,
)

WHATS_IN_PAGE_BLOCK = re.compile(
    r"^\*\*What.s in the page:?\*\*\s*\n"
    r"(?:(?:[ \t]*[-*]+[ \t]+.+\n?)+)",
    re.MULTILINE,
)

CONTAMINATED = None  # None = scan all wiki pages


def sanitize_body(body: str) -> str:
    body = DECISION_BLOCK.sub("", body)
    body = DECISION_HEADER.sub("", body)
    body = WHATS_IN_PAGE_BLOCK.sub("", body)
    for pat in WRAPPER_PROSE:
        body = pat.sub("", body)
    body = META_DESC.sub("", body)
    body = re.sub(r"\n{3,}", "\n\n", body)
    body = body.lstrip("\n")
    return body


def main():
    base = WIKI_DIR.parent
    cleaned = 0

    # Scan all wiki markdown files
    pages = sorted(WIKI_DIR.rglob("*.md"))
    pages = [p for p in pages if p.name != "index.md" and p.name != "CONVENTIONS.md"
             and p.name != "log.md" and p.name != "overview.md"]

    for p in pages:
        rel = str(p.relative_to(base))

        original = p.read_text(encoding="utf-8")

        # Split frontmatter from body
        if original.startswith("---"):
            end = original.find("---", 3)
            if end != -1:
                fm = original[: end + 3]
                body = original[end + 3 :]
            else:
                print(f"NO CHANGE (bad frontmatter): {rel}")
                continue
        else:
            fm = ""
            body = original

        new_body = sanitize_body(body)
        result = fm + "\n" + new_body

        if result != original:
            p.write_text(result, encoding="utf-8")
            removed = len(original) - len(result)
            print(f"CLEANED: {rel} (removed {removed} chars)")
            cleaned += 1
        else:
            print(f"NO CHANGE: {rel}")

    print(f"\nTotal cleaned: {cleaned}/{len(pages)}")


if __name__ == "__main__":
    main()
