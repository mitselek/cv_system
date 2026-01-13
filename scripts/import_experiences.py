#!/usr/bin/env python3
"""
Import experiences from knowledge_base/experiences/ into EdgeDB.

Experiences link to:
- Skills (via skills_demonstrated)
- Tags (via tags)
- Achievements (via achievements) - reverse link
"""
import edgedb
import yaml
import re
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
    """Parse body with ## et and ## en sections."""
    et_content = None
    en_content = None
    
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
                # Stop at ## Connections or ---
                if line.startswith('##') and 'connection' in line.lower():
                    break
                if line.strip() == '---':
                    break
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


def build_translation(data: dict[str, str] | str) -> dict[str, str]:
    """Build Translation JSON from dict or string."""
    if isinstance(data, dict):
        result = {}
        if 'et' in data and data['et']:
            result['et'] = data['et']
        if 'en' in data and data['en']:
            result['en'] = data['en']
        return result
    else:
        # String - use as both languages
        return {'et': str(data), 'en': str(data)}


def parse_date(date_str: str | None) -> str | None:
    """Parse date string to YYYY-MM-DD format."""
    if not date_str:
        return None
    
    date_str = str(date_str).strip()
    
    # Handle "present" or "current"
    if date_str.lower() in ['present', 'current', 'ongoing']:
        return '2026-01-13'
    
    # Handle YYYY format
    if len(date_str) == 4 and date_str.isdigit():
        return f"{date_str}-01-01"
    
    # Handle YYYY-MM format
    if len(date_str) == 7 and date_str[4] == '-':
        return f"{date_str}-01"
    
    return date_str


def import_experiences():
    """Import all experiences from knowledge_base/experiences/."""
    exp_dir = Path('knowledge_base/experiences')
    
    if not exp_dir.exists():
        print(f"❌ Directory not found: {exp_dir}")
        return
    
    # Connect to EdgeDB
    client = edgedb.create_client(
        host='localhost',
        port=5656,
        tls_security='insecure'
    )
    
    exp_files = sorted(exp_dir.glob('*.md'))
    print(f"\n📁 Found {len(exp_files)} experience files\n")
    
    imported = 0
    skipped = 0
    errors = []
    
    for filepath in exp_files:
        external_id = filepath.stem
        print(f"Processing: {external_id}")
        
        try:
            content = filepath.read_text(encoding='utf-8')
            frontmatter, body = extract_frontmatter(content)
            
            # Required fields
            if 'company' not in frontmatter:
                print(f"  ⚠️  Missing 'company', skipping")
                skipped += 1
                continue
            
            if 'title' not in frontmatter:
                print(f"  ⚠️  Missing 'title', skipping")
                skipped += 1
                continue
            
            # Build Translation fields
            company = build_translation(frontmatter['company'])
            title = build_translation(frontmatter['title'])
            
            # Parse body for article
            et_article, en_article = parse_bilingual_body(body)
            article = {}
            if et_article:
                article['et'] = et_article
            if en_article:
                article['en'] = en_article
            
            # Default article if empty
            if not article:
                company_name = company.get('en') or company.get('et') or 'Company'
                article = {'en': f"Experience at {company_name}"}
            
            # Dates
            dates_data = frontmatter.get('dates', {})
            if isinstance(dates_data, dict):
                start_date = parse_date(dates_data.get('start'))
                end_date = parse_date(dates_data.get('end'))
            else:
                # Fallback to top-level start/end
                start_date = parse_date(frontmatter.get('start'))
                end_date = parse_date(frontmatter.get('end'))
            
            if not start_date:
                print(f"  ⚠️  Missing start date, using default")
                start_date = '2020-01-01'
            if not end_date:
                end_date = '2026-01-13'
            
            # URL
            url = frontmatter.get('url') or frontmatter.get('repository')
            # Strip angle brackets if present
            if url:
                url = str(url).strip('<>').strip()
            
            # Tags
            tag_names = []
            if 'tags' in frontmatter:
                tags_data = frontmatter['tags']
                if isinstance(tags_data, list):
                    tag_names.extend([str(t) for t in tags_data])
                else:
                    tag_names.append(str(tags_data))
            
            # Skills
            skill_ids = []
            if 'skills_demonstrated' in frontmatter:
                skills_data = frontmatter['skills_demonstrated']
                if isinstance(skills_data, list):
                    skill_ids.extend([str(s) for s in skills_data])
                else:
                    skill_ids.append(str(skills_data))
            
            # Verification
            verification_status = frontmatter.get('status', 'verified')
            if verification_status not in ['verified', 'draft', 'outdated']:
                verification_status = 'verified'
            
            last_verified = parse_date(frontmatter.get('last_verified', '2025-12-01'))
            
            # Check if exists
            existing = client.query(
                "SELECT Experience { id } FILTER .external_id = <str>$external_id",
                external_id=external_id
            )
            
            if existing:
                print(f"  ⏭️  Already exists, skipping")
                skipped += 1
                continue
            
            # Insert experience
            query = """
                WITH
                    tag_ids := (
                        SELECT Tag FILTER .name IN array_unpack(<array<str>>$tag_names)
                    ),
                    skill_ids := (
                        SELECT Skill FILTER .external_id IN array_unpack(<array<str>>$skill_external_ids)
                    )
                INSERT Experience {
                    external_id := <str>$external_id,
                    company := <Translation>$company,
                    title := <Translation>$title,
                    article := <Translation>$article,
                    dates := (`start` := <IsoDate>$date_start, `end` := <IsoDate>$date_end),
                    url := <OPTIONAL HttpUrl>$url,
                    verification_status := <VerificationStatus>$verification_status,
                    last_verified := <IsoDate>$last_verified,
                    tags := tag_ids,
                    skills_demonstrated := skill_ids
                }
            """
            
            import json
            result = client.query_single(
                query,
                external_id=external_id,
                company=json.dumps(company),
                title=json.dumps(title),
                article=json.dumps(article),
                date_start=start_date,
                date_end=end_date,
                url=url if url else None,
                verification_status=verification_status,
                last_verified=last_verified,
                tag_names=tag_names,
                skill_external_ids=skill_ids
            )
            
            company_name = company.get('en') or company.get('et')
            print(f"  ✅ Imported: {company_name}")
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
        for error in errors[:5]:  # Show first 5
            print(f"  - {error[:200]}")


if __name__ == '__main__':
    import_experiences()
