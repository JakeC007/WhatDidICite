# What Did I Cite: Extract Used References from a LaTeX Project

This Python script scans a LaTeX project for citations and generates a trimmed `.bib` file containing only the references actually used in the paper.

## Features

- Recursively scans `.tex` files for citation commands.
- Detects `\cite`, `\citep`, `\citet`, `\parencite`, `\footcite`, `\textcite`.
- Extracts matching entries from a `.bib` file.
- Outputs a clean `.bib` with only the required references.

## Requirements

- Python 3.7 or newer
- UTF-8 encoded LaTeX and `.bib` files

No external libraries are needed — uses only Python standard library.

## Usage

```bash
python trim_bib.py <root_dir> <bib_file> [-o output_file]
````

* `<root_dir>`: Root directory of your LaTeX project (where `.tex` files are located)
* `<bib_file>`: Path to your master `.bib` file
* `-o output_file` (optional): Name of the trimmed bib file (default: `trimmed.bib`)

### Example

```bash
python main.py ./my_paper ./references.bib -o paper_refs.bib
```

This will:

1. Walk through `./my_paper` for `.tex` files.
2. Collect all citation keys.
3. Extract corresponding entries from `./references.bib`.
4. Write a trimmed `paper_refs.bib` file with only the used references.

## Notes

* Only citations explicitly found in `.tex` files are included.
* If you use multiple `.bib` files, you can run the script multiple times or merge the `.bib` files first.
* Complex LaTeX citation macros not listed may need to be added to the `cite_pattern` regex in the script.

