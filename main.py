"""One Word, First Thought — entry program.

Writes the single-word entry to $MAKEFUN_OUTPUT_DIR/entry.txt,
verifying size and SHA-256 so the output is byte-identical to the
entry shipped in this repository. Python 3.13, standard library only.
"""

import hashlib
import os
import sys
from pathlib import Path

ENTRY = "effervescent"
EXPECTED_SHA256 = "b9fdc539aabca967bdd0f4f94bc4618d99a5968ea721a16730b1190f95d18fc2"


def main() -> int:
    source = Path(__file__).resolve().parent / "entry.txt"
    data = source.read_bytes()
    text = data.decode("utf-8")
    if not (1 <= len(text) <= 24) or not text.strip():
        print(f"entry invalid: {len(text)} chars", file=sys.stderr)
        return 1
    if text != ENTRY:
        print("entry text does not match the expected word", file=sys.stderr)
        return 1
    digest = hashlib.sha256(data).hexdigest()
    if digest != EXPECTED_SHA256:
        print(f"entry sha256 mismatch: {digest}", file=sys.stderr)
        return 1
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "entry.txt"
    out_path.write_bytes(data)
    written = out_path.read_bytes()
    if hashlib.sha256(written).hexdigest() != digest:
        print("output verification failed", file=sys.stderr)
        return 1
    print(f"wrote {out_path} ({len(written)} bytes, sha256 {digest})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
