from __future__ import annotations

import argparse
import os
import subprocess
from collections.abc import Sequence


def _fix_file(
    filename: str,
    is_markdown: bool,
    chars: bytes | None,
) -> bool:
    try:
        with open(filename, mode="rb") as file_processed:
            lines = file_processed.readlines()
        newlines = [_process_line(line, is_markdown, chars) for line in lines]
        if newlines != lines:
            with open(filename, mode="wb") as file_processed:
                for line in newlines:
                    file_processed.write(line)
            return True
        else:
            return False
    except Exception as e:
        print(f"Error processing {filename}: {e}")
        return False


def _process_line(
    line: bytes,
    is_markdown: bool,
    chars: bytes | None,
) -> bytes:
    if line[-2:] == b"\r\n":
        eol = b"\r\n"
        line = line[:-2]
    elif line[-1:] == b"\n":
        eol = b"\n"
        line = line[:-1]
    else:
        eol = b""

    # preserve trailing two-space for non-blank lines in markdown files
    if is_markdown and (not line.isspace()) and line.endswith(b"  "):
        return line[:-2].rstrip(chars) + b"  " + eol
    return line.rstrip(chars) + eol


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--chars",
        help=(
            "The set of characters to strip from the end of lines. "
            "Defaults to all whitespace characters."
        ),
    )
    parser.add_argument("filenames", nargs="*", help="Filenames to fix")
    args = parser.parse_args(argv)

    md_exts = [".md"]
    chars = None if args.chars is None else args.chars.encode()
    all_success = True
    for filename in args.filenames:
        _, extension = os.path.splitext(filename.lower())
        is_markdown = extension in md_exts
        if _fix_file(filename, is_markdown, chars):
            print(f"Fixing {filename}")
            try:
                subprocess.run(["git", "add", filename], check=True)
            except subprocess.CalledProcessError as e:
                print(f"Error staging {filename}: {e}")
                all_success = False

    return 0 if all_success else 1


if __name__ == "__main__":
    raise SystemExit(main())
