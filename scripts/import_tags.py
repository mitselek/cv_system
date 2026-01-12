#!/usr/bin/env python3
"""
Import tags from knowledge base markdown files to EdgeDB.

This script:
1. Scans all markdown files in knowledge_base/
2. Extracts tags from YAML frontmatter
3. Creates unique Tag entries in EdgeDB with name, category, last_verified
"""
import asyncio
import json
import re
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Dict, Set, Tuple

import edgedb
import yaml


# Tag category mapping based on frontmatter context
TAG_CATEGORIES = {
    # From skills files
    "programming": "technology",
    "scripting": "technology",
    "backend": "technology",
    "frontend": "technology",
    "database": "technology",
    "devops": "technology",
    "cloud": "technology",
    "data-processing": "domain",
    "api-development": "domain",
    "web-scraping": "domain",
    "testing": "methodology",
    "security": "domain",
    
    # From experiences/projects
    "leadership": "soft-skill",
    "management": "soft-skill",
    "architecture": "domain",
    "design": "domain",
    "documentation": "methodology",
    
    # Languages
    "language": "language",
    "estonian": "language",
    "english": "language",
    "russian": "language",
    "latvian": "language",
    
    # Hobbies
    "music": "hobby",
    "sports": "hobby",
    "gaming": "hobby",
    "cooking": "hobby",
    "reading": "hobby",
    
    # Default fallback
    "default": "general"
}


def extract_frontmatter(content: str) -> dict | None:
    """Extract YAML frontmatter from markdown content."""
    # Match YAML frontmatter between --- markers
    match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
    if not match:
        return None
    
    try:
        return yaml.safe_load(match.group(1))
    except yaml.YAMLError as e:
        print(f"⚠️  YAML parse error: {e}")
        return None


def categorize_tag(tag: str, file_path: Path) -> str:
    """Determine tag category based on tag name and file context."""
    tag_lower = tag.lower()
    
    # Direct mapping
    if tag_lower in TAG_CATEGORIES:
        return TAG_CATEGORIES[tag_lower]
    
    # Context-based categorization
    parent_dir = file_path.parent.name
    
    if parent_dir == "skills":
        return "technology"
    elif parent_dir == "experiences":
        return "experience"
    elif parent_dir == "projects":
        return "project"
    elif parent_dir == "achievements":
        return "achievement"
    elif parent_dir == "languages":
        return "language"
    elif parent_dir == "hobbies":
        return "hobby"
    elif parent_dir == "certifications":
        return "certification"
    elif parent_dir == "education":
        return "education"
    
    return "general"


def collect_tags(knowledge_base_dir: Path) -> Dict[Tuple[str, str], str]:
    """
    Collect all unique tags from knowledge base files.
    
    Returns:
        Dict mapping (tag_name, category) -> last_verified date
    """
    tags: Dict[Tuple[str, str], str] = {}
    
    # Scan all markdown files
    for md_file in knowledge_base_dir.rglob("*.md"):
        if md_file.name.startswith("_"):
            continue  # Skip compiled files
        
        content = md_file.read_text(encoding="utf-8")
        frontmatter = extract_frontmatter(content)
        
        if not frontmatter:
            continue
        
        # Get last_verified date
        last_verified = frontmatter.get("last_verified", datetime.now().strftime("%Y-%m-%d"))
        
        # Extract tags array
        file_tags = frontmatter.get("tags", [])
        if not isinstance(file_tags, list):
            file_tags = [file_tags] if file_tags else []
        
        # Categorize and store
        for tag in file_tags:
            tag_str = str(tag).strip()
            if not tag_str:
                continue
            
            category = categorize_tag(tag_str, md_file)
            key = (tag_str, category)
            
            # Keep most recent verification date
            if key not in tags or last_verified > tags[key]:
                tags[key] = last_verified
    
    return tags


async def import_tags(client: edgedb.AsyncIOClient, tags: Dict[Tuple[str, str], str]) -> None:
    """Import tags into EdgeDB."""
    print(f"\n📊 Found {len(tags)} unique tags")
    
    # Group by category for display
    by_category = defaultdict(list)
    for (name, category), _ in tags.items():
        by_category[category].append(name)
    
    print("\n📋 Tags by category:")
    for category in sorted(by_category.keys()):
        print(f"  {category}: {len(by_category[category])} tags")
    
    # Insert tags
    print("\n⏳ Importing tags...")
    inserted_count = 0
    skipped_count = 0
    
    for (name, category), last_verified in sorted(tags.items()):
        try:
            # Check if tag already exists
            existing = await client.query_single(
                """
                SELECT Tag {id} 
                FILTER .name = <str>$name AND .category = <str>$category
                LIMIT 1
                """,
                name=name,
                category=category
            )
            
            if existing:
                skipped_count += 1
                continue
            
            # Insert new tag
            await client.query(
                """
                INSERT Tag {
                    name := <str>$name,
                    category := <str>$category,
                    last_verified := <IsoDate>$last_verified
                }
                """,
                name=name,
                category=category,
                last_verified=last_verified
            )
            
            inserted_count += 1
            print(f"  ✅ {name} ({category})")
            
        except Exception as e:
            print(f"  ❌ Failed to insert {name} ({category}): {e}")
    
    print(f"\n✨ Import complete:")
    print(f"   Inserted: {inserted_count}")
    print(f"   Skipped (existing): {skipped_count}")
    print(f"   Total: {len(tags)}")


async def main():
    """Main entry point."""
    print("🏷️  Tag Import Script")
    print("=" * 60)
    
    # Paths
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    knowledge_base_dir = project_root / "knowledge_base"
    
    if not knowledge_base_dir.exists():
        print(f"❌ Knowledge base directory not found: {knowledge_base_dir}")
        return 1
    
    print(f"📁 Knowledge base: {knowledge_base_dir}")
    
    # Collect tags
    print("\n🔍 Scanning markdown files...")
    tags = collect_tags(knowledge_base_dir)
    
    if not tags:
        print("⚠️  No tags found!")
        return 1
    
    # Connect to EdgeDB
    print("\n🔌 Connecting to EdgeDB...")
    client = edgedb.create_async_client(
        host="localhost",
        port=5656,
        user="edgedb",
        tls_security="insecure"
    )
    
    try:
        # Test connection
        await client.query("SELECT 1")
        print("✅ Connected to EdgeDB")
        
        # Import tags
        await import_tags(client, tags)
        
    finally:
        await client.aclose()
    
    return 0


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    exit(exit_code)
