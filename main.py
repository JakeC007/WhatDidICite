#!/usr/bin/env python3
import os
import re
import argparse

def find_citation_keys(root_dir):
    """Walk through LaTeX project and collect all citation keys."""
    cite_pattern = re.compile(r'\\(?:cite|citep|citet|parencite|footcite|textcite)\s*\{([^}]*)\}')
    keys = set()

    for dirpath, _, filenames in os.walk(root_dir):
        for fname in filenames:
            if fname.endswith('.tex'):
                with open(os.path.join(dirpath, fname), encoding='utf-8') as f:
                    content = f.read()
                    for match in cite_pattern.finditer(content):
                        raw_keys = match.group(1)
                        for key in raw_keys.split(','):
                            cleaned_key = key.strip()
                            if cleaned_key:
                                keys.add(cleaned_key)
    return keys

def extract_bib_entries(bib_file, keys):
    """Extract only bib entries for the used keys."""
    with open(bib_file, encoding='utf-8') as f:
        content = f.read()

    entry_pattern = re.compile(r'@(\w+)\s*\{\s*([^,]+),')
    entries = []
    pos = 0

    while True:
        match = entry_pattern.search(content, pos)
        if not match:
            break
        entry_start = match.start()
        brace_level = 0
        end_pos = entry_start
        for i, c in enumerate(content[entry_start:], start=entry_start):
            if c == '{':
                brace_level += 1
            elif c == '}':
                brace_level -= 1
                if brace_level == 0:
                    end_pos = i + 1
                    break
        entry_text = content[entry_start:end_pos]
        entry_key = match.group(2).strip()
        if entry_key in keys:
            entries.append(entry_text)
        pos = end_pos

    return entries

def main():
    parser = argparse.ArgumentParser(
        description="Trim a .bib file to only the citations used in a LaTeX project."
    )
    parser.add_argument("root_dir", help="Root directory of LaTeX project")
    parser.add_argument("bib_file", help="Path to the .bib file")
    parser.add_argument("-o", "--output", default="trimmed.bib", help="Output trimmed .bib file")
    args = parser.parse_args()

    print("[*] Collecting citation keys...")
    keys = find_citation_keys(args.root_dir)
    print(f"[*] Found {len(keys)} citation keys.")

    print("[*] Extracting bib entries...")
    entries = extract_bib_entries(args.bib_file, keys)
    print(f"[*] Extracted {len(entries)} entries from the bib file.")

    with open(args.output, 'w', encoding='utf-8') as out:
        out.write("\n\n".join(entries))

    print(f"[*] Done. Trimmed bib written to {args.output}")

if __name__ == "__main__":
    main()
