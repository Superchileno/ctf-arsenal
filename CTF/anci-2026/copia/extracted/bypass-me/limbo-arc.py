#!/usr/bin/env python3
"""
limbo-arc 1.3 - cold-storage retrieval client.

Fetches a block from a LIMBO archive node by number. Blocks are addressed with
16-bit values; the public catalog starts at block 1. Benches built after 2021
append their maintenance block to the local catalog.

    limbo-arc.py --list
    limbo-arc.py 3
"""

import argparse
import base64
import os
import sys

ARCHIVE_ROOT = os.environ.get(
    "LIMBO_ROOT", os.path.join(os.path.dirname(os.path.abspath(__file__)), "archive")
)

# local block catalog, in order. block N -> CATALOG[N - 1].
CATALOG = [
    "pub/welcome.txt",
    "pub/changelog.txt",
    "pub/support.txt",
    "pub/status.txt",
    "maint/keys.blk",      # PS-2291: appended by the bench refresh script
]

# number of blocks the node advertises as public
PUBLIC_BLOCKS = 4

# controller seal (rotating keystream). do not edit by hand.
_K = b"\x11\x2a\x7c\x03\x5e\x44\x9f\x08"
_SEALED = "d0YdZCV1qWogXiNhMnT8Y04aI3YwIKx6d0ZMdAF2wHohGgh+"


def unseal(blob):
    raw = base64.b64decode(blob)
    return bytes(c ^ _K[i % len(_K)] for i, c in enumerate(raw)).decode()


def lookup(block):
    """Resolve a block number to a catalog entry, or None."""
    block &= 0xFFFF
    if block > PUBLIC_BLOCKS:
        return None
    slot = block - 1
    if slot < len(CATALOG):
        return CATALOG[slot]
    return None


def main():
    ap = argparse.ArgumentParser(prog="limbo-arc", description="fetch a block")
    ap.add_argument("block", nargs="?", type=int, help="block number")
    ap.add_argument("--list", action="store_true", help="list public blocks")
    ap.add_argument("--where", action="store_true", help="print the archive root")
    args = ap.parse_args()

    if args.where:
        print(ARCHIVE_ROOT)
        return 0

    if args.list:
        for n in range(1, PUBLIC_BLOCKS + 1):
            print("%2d  %s" % (n, CATALOG[n - 1]))
        return 0

    if args.block is None:
        ap.print_help()
        return 2

    entry = lookup(args.block)
    if entry is None:
        print("limbo-arc: block %d is not allocated on this node" % args.block)
        return 1

    if entry.endswith(".blk"):
        sys.stdout.write(unseal(_SEALED) + "\n")
        return 0

    path = os.path.join(ARCHIVE_ROOT, entry)
    try:
        with open(path, "r") as fh:
            sys.stdout.write(fh.read())
    except FileNotFoundError:
        print("limbo-arc: block %d has no local copy (%s)" % (args.block, path))
    return 0


if __name__ == "__main__":
    sys.exit(main())
