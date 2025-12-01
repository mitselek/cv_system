#!/usr/bin/env python3
"""
Add markdownlint disable/enable comments to files with YAML frontmatter.
"""

import sys
from pathlib import Path


def process_file(filepath: Path) -> bool:
    """Add markdownlint comments if needed."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Skip if already has markdownlint comments
    if 'markdownlint-disable' in content:
        return False
    
    # Check if file has YAML frontmatter
    if not content.startswith('---') and not content.startswith('<!--'):
        return False
    
    lines = content.split('\n')
    
    # Find the second --- (end of frontmatter)
    dash_count = 0
    frontmatter_end = -1
    start_offset = 0
    
    # Skip HTML comment at start if present
    if lines[0].startswith('<!--'):
        start_offset = 1
    
    for i in range(start_offset, len(lines)):
        if lines[i].strip() == '---':
            dash_count += 1
            if dash_count == 2:
                frontmatter_end = i
                break
    
    if frontmatter_end == -1:
        return False
    
    # Check if there's content after frontmatter
    has_content_after = frontmatter_end < len(lines) - 1 and any(
        line.strip() for line in lines[frontmatter_end + 1:]
    )
    
    # Add disable comment before frontmatter
    if start_offset == 0:
        new_lines = ['<!-- markdownlint-disable MD007 MD032 -->', '']
        new_lines.extend(lines)
    else:
        # HTML comment already exists, insert after it
        new_lines = lines[:start_offset]
        new_lines.extend(['', '<!-- markdownlint-disable MD007 MD032 -->', ''])
        new_lines.extend(lines[start_offset:])
        frontmatter_end += 3  # Adjust index
    
    # Add enable comment after frontmatter if there's content
    if has_content_after:
        new_lines.insert(frontmatter_end + 1, '')
        new_lines.insert(frontmatter_end + 2, '<!-- markdownlint-enable MD007 MD032 -->')
        new_lines.insert(frontmatter_end + 3, '')
    
    new_content = '\n'.join(new_lines)
    
    # Write back
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    return True

def main():
    kb_path = Path(__file__).parent.parent / 'knowledge_base'
    
    if not kb_path.exists():
        print(f"Error: {kb_path} not found")
        sys.exit(1)
    
    processed = 0
    for md_file in kb_path.rglob('*.md'):
        if process_file(md_file):
            print(f"Processed: {md_file.relative_to(kb_path)}")
            processed += 1
    
    print(f"\nTotal files processed: {processed}")

if __name__ == '__main__':
    main()
