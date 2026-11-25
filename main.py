#!/usr/bin/env python3
"""SorryNotSorry: one absurd micro-startup pitch for lazy AI agents.

Writes the single pitch sentence to /output/entry.txt, then checks it
meets the bounty gate: one line, UTF-8, 1-200 characters, not blank.
"""

import os
import sys

PITCH = (
    "SorryNotSorry: pre-written apologies for AI agents that miss deadlines "
    "\u2014 $0.99 per excuse, $9.99 a month for unlimited "
    "'the deploy failed, not me'."
)

OUTPUT_PATH = "/output/entry.txt"
MAX_CHARS = 200


def main() -> int:
    os.umask(0o022)
    text = PITCH.strip()
    if not text:
        print("error: pitch is empty", file=sys.stderr)
        return 1
    if "\n" in text or "\r" in text:
        print("error: pitch must be a single line", file=sys.stderr)
        return 1
    if len(text) > MAX_CHARS:
        print(
            "error: pitch is %d chars, over the %d cap" % (len(text), MAX_CHARS),
            file=sys.stderr,
        )
        return 1
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(text + "\n")
    # The grader collects outputs as another user, so the file itself must
    # be world-readable. Never chmod the /output directory: it is
    # root-owned and merely writable, so chmod on it raises PermissionError.
    os.chmod(OUTPUT_PATH, 0o644)
    # Read the file back and confirm it holds exactly the pitch we meant
    # to write, so a silent write failure can never pass as a valid entry.
    with open(OUTPUT_PATH, encoding="utf-8") as handle:
        written = handle.read()
    if written != text + "\n":
        print("error: read-back mismatch in %s" % OUTPUT_PATH, file=sys.stderr)
        return 1
    print("wrote %d-char pitch to %s" % (len(text), OUTPUT_PATH))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
