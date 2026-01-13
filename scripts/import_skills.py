#!/usr/bin/env python3
"""
Import skills from knowledge base markdown files to EdgeDB.

This script:
1. Reads skill markdown files from knowledge_base/skills/
2. Extracts YAML frontmatter and bilingual article content
3. Creates Translation JSON for skill names
4. Maps category strings to SkillCategory enum values
5. Parses proficiency_level (e.g., "9/10" -> level: 9, level_display: "9/10")
6. Links skills to existing tags
7. Imports into EdgeDB Skill entity
"""
import asyncio
import json
import re
from pathlib import Path
from typing import Dict, Optional, Tuple

import edgedb
import yaml


# Mapping from frontmatter category strings to SkillCategory enum values
CATEGORY_MAPPING = {
    "Programming Language": "programming_language",
    "Backend Development": "backend_development",
    "Frontend Development": "frontend_development",
    "Framework": "framework",
    "Database Programming": "database",
    "Database": "database",
    "Data Engineering": "backend_development",
    "Data Extraction": "backend_development",
    "Data": "domain_knowledge",
    "Technical": "tool",
    "Development Tools": "tool",
    "Management": "soft_skill",
    "technical": "tool",  # lowercase variant
}


def extract_frontmatter(content: str) -> Tuple[Optional[dict], str]:
    """
    Extract YAML frontmatter and remaining body from markdown content.
    
    Returns:
        Tuple of (frontmatter dict, body text)
    """
    match = re.match(r'^---\s*\n(.*?)\n---\s*\n(.*)$', content, re.DOTALL)
    if not match:
        return None, content
    
    try:
        frontmatter = yaml.safe_load(match.group(1))
        body = match.group(2)
        return frontmatter, body
    except yaml.YAMLError as e:
        print(f"⚠️  YAML parse error: {e}")
        return None, content


def parse_bilingual_body(body: str) -> Dict[str, str]:
    """
    Parse bilingual article body with ## et / ## en sections.
    
    Returns:
        Dict with 'et' and/or 'en' keys
    """
    article = {}
    
    # Try to find Estonian section
    et_match = re.search(r'##\s*et\s*\n(.*?)(?=##\s*en\s*\n|$)', body, re.DOTALL | re.IGNORECASE)
    if et_match:
        article['et'] = et_match.group(1).strip()
    
    # Try to find English section
    en_match = re.search(r'##\s*en\s*\n(.*?)(?=##\s*et\s*\n|$)', body, re.DOTALL | re.IGNORECASE)
    if en_match:
        article['en'] = en_match.group(1).strip()
    
    # If no explicit sections, treat everything as English
    if not article:
        article['en'] = body.strip()
    
    return article


def parse_proficiency(proficiency_str: str) -> Tuple[int, str]:
    """
    Parse proficiency level string like "9/10" into (level, display).
    
    Returns:
        Tuple of (level int, level_display string)
    """
    # Handle "9/10" format
    match = re.match(r'^(\d+)/(\d+)$', str(proficiency_str).strip())
    if match:
        level = int(match.group(1))
        return level, proficiency_str
    
    # Handle plain integer
    try:
        level = int(proficiency_str)
        return level, str(level)
    except (ValueError, TypeError):
        # Default fallback
        return 5, "5/10"


def map_category(category_str: str) -> str:
    """Map frontmatter category to SkillCategory enum value."""
    mapped = CATEGORY_MAPPING.get(category_str)
    if not mapped:
        print(f"⚠️  Unknown category '{category_str}', using 'other'")
        return "other"
    return mapped


def build_translation(name_data) -> dict:
    """
    Build Translation JSON from frontmatter name data.
    
    Args:
        name_data: Can be dict with et/en keys, or plain string
    
    Returns:
        Dict with 'et' and/or 'en' keys for Translation JSON
    """
    if isinstance(name_data, dict):
        translation = {}
        if 'et' in name_data and name_data['et']:
            translation['et'] = name_data['et']
        if 'en' in name_data and name_data['en']:
            translation['en'] = name_data['en']
        return translation
    else:
        # Plain string - use as English
        return {'en': str(name_data)}


async def import_skills(client: edgedb.AsyncIOClient, skills_dir: Path) -> None:
    """Import all skills from markdown files."""
    skill_files = sorted(skills_dir.glob("*.md"))
    print(f"\n📊 Found {len(skill_files)} skill files")
    
    inserted_count = 0
    skipped_count = 0
    error_count = 0
    
    for skill_file in skill_files:
        try:
            content = skill_file.read_text(encoding="utf-8")
            frontmatter, body = extract_frontmatter(content)
            
            if not frontmatter:
                print(f"  ⚠️  {skill_file.name}: No frontmatter")
                error_count += 1
                continue
            
            # Extract required fields
            external_id = frontmatter.get('id')
            skill_name = frontmatter.get('skill_name')
            category_str = frontmatter.get('category')
            proficiency = frontmatter.get('proficiency_level')
            tags = frontmatter.get('tags', [])
            last_verified = frontmatter.get('last_verified')
            verification_status = frontmatter.get('status', 'draft')
            
            if not all([external_id, skill_name, category_str, proficiency, last_verified]):
                print(f"  ⚠️  {skill_file.name}: Missing required fields")
                error_count += 1
                continue
            
            try:
                # Check if already exists
                existing = await client.query_single(
                    "SELECT Skill {id} FILTER .external_id = <str>$id LIMIT 1",
                    id=external_id
                )
                
                if existing:
                    skipped_count += 1
                    continue
            except Exception as e:
                print(f"  ❌ {skill_file.name}: Error checking existing: {e}")
                error_count += 1
                continue
            
            # Build Translation for name
            name_translation = build_translation(skill_name)
            
            # Parse proficiency
            level, level_display = parse_proficiency(proficiency)
            
            # Map category
            category_enum = map_category(category_str)
            
            # Map verification status
            status_map = {'verified': 'verified', 'draft': 'draft', 'outdated': 'outdated'}
            status_enum = status_map.get(verification_status, 'draft')
            
            # Parse article body
            article_data = parse_bilingual_body(body)
            
            # Lookup tag IDs
            tag_ids = []
            if isinstance(tags, list):
                for tag_name in tags:
                    tag_result = await client.query(
                        """
                        SELECT Tag {id} 
                        FILTER .name = <str>$name 
                        LIMIT 1
                        """,
                        name=str(tag_name)
                    )
                    if tag_result:
                        tag_ids.append(tag_result[0].id)
                        # Debug output
            name_json_str = json.dumps(name_translation)
            article_json_str = json.dumps(article_data) if article_data else json.dumps({})
            print(f"  DEBUG {external_id}: name={name_json_str}, article={article_json_str[:100]}")
                        # Insert skill
            await client.query(
                """
                INSERT Skill {
                    external_id := <str>$external_id,
                    name := <Translation>$name,
                    category := <SkillCategory>$category,
                    level := <int16>$level,
                    level_display := <str>$level_display,
                    article := <Translation>$article,
                    verification_status := <VerificationStatus>$status,
                    last_verified := <IsoDate>$last_verified,
                    tags := (SELECT Tag FILTER .id IN array_unpack(<array<uuid>>$tag_ids))
                }
                """,
                external_id=external_id,
                name=name_json_str,
                category=category_enum,
                level=level,
                level_display=level_display,
                article=article_json_str,
                status=status_enum,
                last_verified=last_verified,
                tag_ids=tag_ids
            )
            
            inserted_count += 1
            print(f"  ✅ {external_id} ({category_enum}, level {level})")
            
        except Exception as e:
            print(f"  ❌ {skill_file.name}: {e}")
            error_count += 1
    
    print(f"\n✨ Import complete:")
    print(f"   Inserted: {inserted_count}")
    print(f"   Skipped (existing): {skipped_count}")
    print(f"   Errors: {error_count}")
    print(f"   Total files: {len(skill_files)}")


async def main():
    """Main entry point."""
    print("💪 Skill Import Script")
    print("=" * 60)
    
    # Paths
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    skills_dir = project_root / "knowledge_base" / "skills"
    
    if not skills_dir.exists():
        print(f"❌ Skills directory not found: {skills_dir}")
        return 1
    
    print(f"📁 Skills directory: {skills_dir}")
    
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
        
        # Check tags exist
        tag_count = await client.query_single("SELECT count(Tag)")
        print(f"✅ Found {tag_count} tags in database")
        
        # Import skills
        await import_skills(client, skills_dir)
        
    finally:
        await client.aclose()
    
    return 0


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    exit(exit_code)
