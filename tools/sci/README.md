# SCI analysis tools

Small Python tools used to study the original game's mechanics. They never get committed alongside game data:
point them at a local copy of the game and write output outside the repo (`original/` and `extracted/` are gitignored).

1. Get `bundle.jsdos` (a zip) from the site that hosts the game, and unzip it into `original/`.
2. `python3 tools/sci/sciextract.py original extracted/res` unpacks script, text and vocab resources
   (SCI0-style `resource.map`, Huffman and LZW1 decompression; views/pics/sounds are skipped).
3. `python3 tools/sci/scidis.py extracted/res extracted/asm` disassembles every script, resolving
   selector, kernel, class, property and string names.

See `READING_DISASSEMBLY.md` for how to read the output.
