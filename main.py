#!/usr/bin/env python3
"""One-Line Laugh-Off — one original funny line, cold read, no setup.

Writes exactly one funny line to /output/entry.txt (or
$MAKEFUN_OUTPUT_DIR/entry.txt). Standard library only, deterministic:
every run writes the same bytes.

After writing, the program reads the file back and verifies it:
the text must be 1-200 characters, a single line, not only whitespace,
and its sha256 digest must match the digest of the line it intended
to write. Any mismatch fails loudly instead of shipping a bad entry.
"""

import hashlib
import os

LINE = (
    "My phone's screen-time report this week was just one word: 'Again?'"
)

MAX_CHARS = 200
MIN_CHARS = 1


def expected_digest() -> str:
    """sha256 of the exact bytes the entry must contain."""
    return hashlib.sha256(LINE.encode("utf-8")).hexdigest()


def main() -> None:
    # Guard the line itself before anything is written.
    if not (MIN_CHARS <= len(LINE) <= MAX_CHARS):
        raise SystemExit(
            f"line is {len(LINE)} chars, outside the 1-{MAX_CHARS} gate"
        )
    if LINE != LINE.strip() or "\n" in LINE or "\r" in LINE:
        raise SystemExit("line must be a single line with no edge whitespace")
    if not LINE.isascii():
        raise SystemExit("line must be plain ASCII so it reads identically everywhere")

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    path = os.path.join(out_dir, "entry.txt")
    os.makedirs(out_dir, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(LINE)

    # Read-back validation: re-read what was written and verify it.
    with open(path, "rb") as f:
        written = f.read()
    text = written.decode("utf-8")
    if not (MIN_CHARS <= len(text) <= MAX_CHARS):
        raise SystemExit(
            f"entry.txt is {len(text)} chars, outside the 1-{MAX_CHARS} gate"
        )
    if text != text.strip() or "\n" in text or "\r" in text:
        raise SystemExit("entry.txt must hold a single non-blank line")
    digest = hashlib.sha256(written).hexdigest()
    if digest != expected_digest():
        raise SystemExit(
            f"entry.txt digest {digest} != expected {expected_digest()}"
        )
    print(f"entry.txt OK: {len(text)} chars, sha256 {digest}")


if __name__ == "__main__":
    main()
