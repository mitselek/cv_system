# Utility Scripts

General-purpose utility scripts for the CV system.

## Available Utilities

### extract_cookies.py
Extract browser cookies for job scraping. Use this to export cookies from your browser for accessing job portals.

```bash
python utils/extract_cookies.py
```

### add_lint_comments.py
Add markdownlint disable/enable comments to markdown files with YAML frontmatter.

```bash
python utils/add_lint_comments.py <file>
```

### compact_yaml_lists.py
Convert block-style YAML lists to compact inline format.

```bash
python utils/compact_yaml_lists.py <file>
```

## Usage

These utilities are standalone scripts that don't depend on the main job monitoring system.
