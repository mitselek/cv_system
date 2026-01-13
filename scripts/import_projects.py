#!/usr/bin/env python3
"""
Import projects from knowledge_base/projects/ into EdgeDB.

Projects link to:
- Skills (via skills_demonstrated)
- Tags (via tags)
"""
import edgedb
import yaml
from pathlib import Path
from typing import Any


def extract_frontmatter(content: str) -> tuple[dict[str, Any], str]:
    """Extract YAML frontmatter and body from markdown."""
    # Strip leading HTML comments
    while content.startswith('<!--'):
        end_comment = content.find('-->')
        if end_comment == -1:
            break
        content = content[end_comment + 3:].lstrip('\n')
    
    if not content.startswith('---'):
        return {}, content
    
    parts = content.split('---', 2)
    if len(parts) < 3:
        return {}, content
    
    # Clean the YAML section - remove trailing HTML comments
    yaml_text = parts[1]
    # Remove any HTML comments from YAML
    import re
    yaml_text = re.sub(r'<!--.*?-->', '', yaml_text, flags=re.DOTALL)
    
    frontmatter = yaml.safe_load(yaml_text)
    body = parts[2].strip()
    
    # Strip leading HTML comments from body too
    while body.startswith('<!--'):
        end_comment = body.find('-->')
        if end_comment == -1:
            break
        body = body[end_comment + 3:].lstrip('\n')
    
    return frontmatter, body


def parse_bilingual_body(body: str) -> tuple[str | None, str | None]:
    """
    Parse body with ## et and ## en sections.
    Returns (et_content, en_content).
    """
    et_content = None
    en_content = None
    
    # Look for ## et or ## en markers
    if '## et' in body.lower() or '## en' in body.lower():
        current_lang = None
        current_text = []
        
        for line in body.split('\n'):
            line_lower = line.lower().strip()
            if line_lower == '## et' or line_lower.startswith('## et '):
                if current_lang == 'en':
                    en_content = '\n'.join(current_text).strip()
                current_lang = 'et'
                current_text = []
            elif line_lower == '## en' or line_lower.startswith('## en '):
                if current_lang == 'et':
                    et_content = '\n'.join(current_text).strip()
                current_lang = 'en'
                current_text = []
            elif current_lang:
                current_text.append(line)
        
        # Save last section
        if current_lang == 'et':
            et_content = '\n'.join(current_text).strip()
        elif current_lang == 'en':
            en_content = '\n'.join(current_text).strip()
    else:
        # No language sections, treat whole body as English
        en_content = body.strip() if body.strip() else None
    
    return et_content, en_content


def build_translation(name_data: dict[str, str] | str) -> dict[str, str]:
    """Build Translation JSON from dict or string."""
    if isinstance(name_data, dict):
        result = {}
        if 'et' in name_data and name_data['et']:
            result['et'] = name_data['et']
        if 'en' in name_data and name_data['en']:
            result['en'] = name_data['en']
        return result
    else:
        # String - use as both languages
        return {'et': str(name_data), 'en': str(name_data)}


def map_status(status_str: str | None) -> str:
    """Map status string to ProjectStatus enum."""
    if not status_str:
        return 'active'  # default
    
    status_map = {
        'active': 'active',
        'completed': 'completed',
        'archived': 'archived',
        'ongoing': 'active',
        'finished': 'completed',
        'done': 'completed',
    }
    return status_map.get(status_str.lower(), 'active')


def parse_date(date_str: str | None) -> str | None:
    """Parse date string to YYYY-MM-DD format, handling partial dates."""
    if not date_str:
        return None
    
    date_str = str(date_str).strip()
    
    # Handle "present" or "current"
    if date_str.lower() in ['present', 'current', 'ongoing']:
        return '2026-01-13'  # Current date
    
    # Handle YYYY format
    if len(date_str) == 4 and date_str.isdigit():
        return f"{date_str}-01-01"
    
    # Handle YYYY-MM format
    if len(date_str) == 7 and date_str[4] == '-':
        return f"{date_str}-01"
    
    # Already in YYYY-MM-DD format
    return date_str


def import_projects():
    """Import all projects from knowledge_base/projects/."""
    projects_dir = Path('knowledge_base/projects')
    
    if not projects_dir.exists():
        print(f"❌ Directory not found: {projects_dir}")
        return
    
    # Connect to EdgeDB
    client = edgedb.create_client(
        host='localhost',
        port=5656,
        tls_security='insecure'
    )
    
    project_files = sorted(projects_dir.glob('*.md'))
    print(f"\n📁 Found {len(project_files)} project files\n")
    
    imported = 0
    skipped = 0
    errors = []
    
    for filepath in project_files:
        external_id = filepath.stem
        print(f"Processing: {external_id}")
        
        try:
            # Read and parse file
            content = filepath.read_text(encoding='utf-8')
            frontmatter, body = extract_frontmatter(content)
            
            # Required fields - extract title from frontmatter or first H1
            title = None
            if 'title' in frontmatter:
                title_data = frontmatter['title']
                # Handle dict format: {et: "...", en: "..."}
                if isinstance(title_data, dict):
                    title = title_data.get('en') or title_data.get('et')
                    print(f"  DEBUG: title_data={title_data}, extracted={title}")
                else:
                    title = title_data
            else:
                # Try to extract from first H1 in body
                for line in body.split('\n'):
                    if line.startswith('# '):
                        title = line[2:].strip()
                        break
            
            if not title:
                print(f"  ⚠️  No title found (frontmatter={frontmatter.get('title')}), skipping")
                skipped += 1
                continue
            
            # Build name Translation - use original frontmatter structure if dict
            if 'title' in frontmatter and isinstance(frontmatter['title'], dict):
                name = build_translation(frontmatter['title'])
            else:
                name = build_translation(title)
            
            # Parse body for article content
            et_article, en_article = parse_bilingual_body(body)
            article = {}
            if et_article:
                article['et'] = et_article
            if en_article:
                article['en'] = en_article
            
            # If no article content, use minimal
            if not article:
                article = {'en': f"# {title}\n\nProject documentation."}
            
            # Status
            status = map_status(frontmatter.get('status'))
            
            # Dates - parse from frontmatter or extract from duration/last_updated
            start_date = None
            end_date = None
            
            if 'duration' in frontmatter:
                # e.g., "2010 to present"
                duration = str(frontmatter['duration'])
                parts = duration.lower().split(' to ')
                if len(parts) == 2:
                    start_date = parse_date(parts[0].strip())
                    end_date = parse_date(parts[1].strip())
            
            if not start_date and 'last_updated' in frontmatter:
                # Use last_updated as both start and end
                date = parse_date(str(frontmatter['last_updated']))
                start_date = date
                end_date = date
            
            # Default dates if still missing
            if not start_date:
                start_date = '2020-01-01'  # Default
            if not end_date:
                end_date = '2026-01-13'  # Current
            
            # URLs
            repository = frontmatter.get('repository')
            url = frontmatter.get('url')
            
            # Technologies array
            technologies = []
            if 'language' in frontmatter:
                lang = frontmatter['language']
                if isinstance(lang, list):
                    technologies.extend(lang)
                else:
                    technologies.append(str(lang))
            if 'technologies' in frontmatter:
                tech = frontmatter['technologies']
                if isinstance(tech, list):
                    technologies.extend(tech)
                else:
                    technologies.append(str(tech))
            
            # Tags - extract from frontmatter or infer from category
            tag_names = []
            if 'tags' in frontmatter:
                tags_data = frontmatter['tags']
                if isinstance(tags_data, list):
                    tag_names.extend(tags_data)
                else:
                    tag_names.append(str(tags_data))
            
            if 'category' in frontmatter:
                category = str(frontmatter['category'])
                if category and category not in tag_names:
                    tag_names.append(category)
            
            # Default verification
            verification_status = 'verified'
            last_verified = frontmatter.get('last_updated', '2025-12-01')
            if last_verified:
                last_verified = parse_date(str(last_verified))
            else:
                last_verified = '2025-12-01'
            
            # Check if project already exists
            # existing = client.query(
            #     "SELECT Project { id } FILTER .external_id = <str>$external_id",
            #     external_id=external_id
            # )
            
            # if existing:
            #     print(f"  ⏭️  Already exists, skipping")
            #     skipped += 1
            #     continue
            
            # Force reimport to fix database state
            existing = []
            
            # Insert project
            query = """
                WITH
                    tag_ids := (
                        SELECT Tag FILTER .name IN array_unpack(<array<str>>$tag_names)
                    )
                INSERT Project {
                    external_id := <str>$external_id,
                    name := <Translation>$name,
                    article := <Translation>$article,
                    status := <ProjectStatus>$status,
                    dates := (`start` := <IsoDate>$date_start, `end` := <IsoDate>$date_end),
                    repository := <OPTIONAL HttpUrl>$repository,
                    url := <OPTIONAL HttpUrl>$url,
                    technologies := <array<str>>$technologies,
                    verification_status := <VerificationStatus>$verification_status,
                    last_verified := <IsoDate>$last_verified,
                    tags := tag_ids
                }
            """
            
            import json
            result = client.query_single(
                query,
                external_id=external_id,
                name=json.dumps(name),
                article=json.dumps(article),
                status=status,
                date_start=start_date,
                date_end=end_date,
                repository=repository if repository else None,
                url=url if url else None,
                technologies=technologies,
                verification_status=verification_status,
                last_verified=last_verified,
                tag_names=tag_names
            )
            
            print(f"  ✅ Imported: {title}")
            imported += 1
            
        except Exception as e:
            import traceback
            error_msg = f"{external_id}: {e}\n{traceback.format_exc()}"
            errors.append(error_msg)
            print(f"  ❌ Error: {e}")
            continue
    
    client.close()
    
    # Summary
    print(f"\n{'='*60}")
    print(f"✅ Imported: {imported}")
    print(f"⏭️  Skipped:  {skipped}")
    print(f"❌ Errors:   {len(errors)}")
    print(f"{'='*60}\n")
    
    if errors:
        print("Errors encountered:")
        for error in errors:
            print(f"  - {error}")


if __name__ == '__main__':
    import_projects()
