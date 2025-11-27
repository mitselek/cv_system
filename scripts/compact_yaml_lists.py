#!/usr/bin/env python3
"""
Convert block-style YAML lists to compact inline format.
Converts:
  tags:
    - item1
    - item2
To:
  tags: [item1, item2]
"""

import re
from pathlib import Path


def convert_yaml_lists(content: str) -> str:
    """Convert block-style YAML lists to inline format."""
    lines = content.split('\n')
    result: list[str] = []
    i = 0
    
    while i < len(lines):
        line = lines[i]
        
        # Check if this is a list field (tags, skills_demonstrated, technology_stack)
        match = re.match(r'^(tags|skills_demonstrated|technology_stack):\s*$', line)
        if match:
            field_name = match.group(1)
            items: list[str] = []
            i += 1
            
            # Collect all list items
            while i < len(lines):
                item_match = re.match(r'^\s*-\s+(.+)$', lines[i])
                if not item_match:
                    break
                items.append(item_match.group(1))
                i += 1
            
            # Convert to inline format if items found
            if items:
                result.append(f"{field_name}: [{', '.join(items)}]")
            else:
                result.append(f"{field_name}:")
            continue
        
        result.append(line)
        i += 1
    
    return '\n'.join(result)


def process_file(file_path: Path) -> bool:
    """Process a single markdown file. Returns True if modified."""
    content = file_path.read_text()
    new_content = convert_yaml_lists(content)
    
    if content != new_content:
        file_path.write_text(new_content)
        return True
    return False


def main():
    """Process all markdown files in knowledge_base."""
    kb_path = Path(__file__).parent.parent / 'knowledge_base'
    modified_count = 0
    
    for md_file in kb_path.rglob('*.md'):
        # Skip compiled context
        if md_file.name == '_compiled_context.md':
            continue
        
        if process_file(md_file):
            modified_count += 1
            print(f"✓ {md_file.relative_to(kb_path)}")
    
    print(f"\n{modified_count} files modified")


if __name__ == '__main__':
    main()
