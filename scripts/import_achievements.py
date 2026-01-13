#!/usr/bin/env python3
"""
Import achievements from knowledge_base/achievements/ into EdgeDB.

Achievements link to:
- Tags (via tags)
- Parent Experience (via parent_experience)
"""
import edgedb
import yaml
import re
from pathlib import Path
from typing import Any


def extract_frontmatter(content: str) -> tuple[dict[str, Any], str]:
    """Extract YAML frontmatter and body from markdown."""
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
    
    yaml_text = parts[1]
    yaml_text = re.sub(r'<!--.*?-->', '', yaml_text, flags=re.DOTALL)
    
    frontmatter = yaml.safe_load(yaml_text)
    body = parts[2].strip()
    
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
                if line.startswith('##') and 'connection' in line.lower():
                    break
                if line.strip() == '---':
                    break
                current_text.append(line)
        
        if current_lang == 'et':
            et_content = '\n'.join(current_text).strip()
        elif current_lang == 'en':
            en_content = '\n'.join(current_text).strip()
    else:
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
        return {'et': str(data), 'en': str(data)}


def parse_date(date_str: str | None) -> str | None:
    """Parse date string to YYYY-MM-DD format. Supports YYYY, YYYY-MM, YYYY-MM-DD, and YYYY-YYYY ranges."""
    if not date_str:
        return None
    
    date_str = str(date_str).strip()
    
    if date_str.lower() in ['present', 'current', 'ongoing']:
        return '2026-01-13'
    
    # Handle date ranges (YYYY-YYYY) - use end date
    if re.match(r'^\d{4}-\d{4}$', date_str):
        end_year = date_str.split('-')[1]
        return f"{end_year}-12-31"
    
    if len(date_str) == 4 and date_str.isdigit():
        return f"{date_str}-01-01"
    
    if len(date_str) == 7 and date_str[4] == '-':
        return f"{date_str}-01"
    
    return date_str


def import_achievements():
    """Import all achievements from knowledge_base/achievements/."""
    ach_dir = Path('knowledge_base/achievements')
    
    if not ach_dir.exists():
        print(f"❌ Directory not found: {ach_dir}")
        return
    
    client = edgedb.create_client(
        host='localhost',
        port=5656,
        tls_security='insecure'
    )
    
    ach_files = sorted(ach_dir.glob('*.md'))
    print(f"\n📁 Found {len(ach_files)} achievement files\n")
    
    imported = 0
    skipped = 0
    errors = []
    
    for filepath in ach_files:
        external_id = filepath.stem
        print(f"Processing: {external_id}")
        
        try:
            content = filepath.read_text(encoding='utf-8')
            frontmatter, body = extract_frontmatter(content)
            
            # Required field
            if 'title' not in frontmatter:
                print(f"  ⚠️  Missing 'title', skipping")
                skipped += 1
                continue
            
            # Build Translation for title
            title = build_translation(frontmatter['title'])
            
            # Parse body for article
            et_article, en_article = parse_bilingual_body(body)
            article = {}
            if et_article:
                article['et'] = et_article
            if en_article:
                article['en'] = en_article
            
            # Use description if no body content
            if not article and 'description' in frontmatter:
                desc_data = frontmatter['description']
                if isinstance(desc_data, dict):
                    article = build_translation(desc_data)
                else:
                    article = {'en': str(desc_data)}
            
            # Default article if still empty
            if not article:
                title_text = title.get('en') or title.get('et') or 'Achievement'
                article = {'en': f"# {title_text}\n\nAchievement details."}
            
            # Date - extract from parent experience or use default
            date = None
            if 'date' in frontmatter:
                date = parse_date(frontmatter['date'])
            elif 'year' in frontmatter:
                date = parse_date(frontmatter['year'])
            
            # If still no date, try to extract from parent experience dates
            parent_exp_id = frontmatter.get('parent_experience')
            if not date and parent_exp_id:
                # Get parent experience end date
                parent = client.query(
                    "SELECT Experience { dates } FILTER .external_id = <str>$id",
                    id=parent_exp_id
                )
                if parent:
                    date = parent[0].dates[1]  # Use end date
            
            if not date:
                date = '2025-01-01'  # Default
            
            # Tags
            tag_names = []
            if 'tags' in frontmatter:
                tags_data = frontmatter['tags']
                if isinstance(tags_data, list):
                    tag_names.extend([str(t) for t in tags_data])
                else:
                    tag_names.append(str(tags_data))
            
            # Verification
            verification_status = frontmatter.get('status', 'verified')
            if verification_status not in ['verified', 'draft', 'outdated']:
                verification_status = 'verified'
            
            last_verified = parse_date(frontmatter.get('last_verified', '2025-12-01'))
            
            # Check if exists
            existing = client.query(
                "SELECT Achievement { id } FILTER .external_id = <str>$external_id",
                external_id=external_id
            )
            
            if existing:
                print(f"  ⏭️  Already exists, skipping")
                skipped += 1
                continue
            
            # Build query
            if parent_exp_id:
                query = """
                    WITH
                        tag_ids := (
                            SELECT Tag FILTER .name IN array_unpack(<array<str>>$tag_names)
                        ),
                        parent_exp := (
                            SELECT Experience FILTER .external_id = <str>$parent_exp_id
                        )
                    INSERT Achievement {
                        external_id := <str>$external_id,
                        title := <Translation>$title,
                        article := <Translation>$article,
                        date := <IsoDate>$date,
                        verification_status := <VerificationStatus>$verification_status,
                        last_verified := <IsoDate>$last_verified,
                        tags := tag_ids,
                        parent_experience := parent_exp
                    }
                """
            else:
                query = """
                    WITH
                        tag_ids := (
                            SELECT Tag FILTER .name IN array_unpack(<array<str>>$tag_names)
                        )
                    INSERT Achievement {
                        external_id := <str>$external_id,
                        title := <Translation>$title,
                        article := <Translation>$article,
                        date := <IsoDate>$date,
                        verification_status := <VerificationStatus>$verification_status,
                        last_verified := <IsoDate>$last_verified,
                        tags := tag_ids
                    }
                """
            
            import json
            params = {
                'external_id': external_id,
                'title': json.dumps(title),
                'article': json.dumps(article),
                'date': date,
                'verification_status': verification_status,
                'last_verified': last_verified,
                'tag_names': tag_names
            }
            
            if parent_exp_id:
                params['parent_exp_id'] = parent_exp_id
            
            result = client.query_single(query, **params)
            
            title_text = title.get('en') or title.get('et')
            print(f"  ✅ Imported: {title_text}")
            imported += 1
            
        except Exception as e:
            import traceback
            error_msg = f"{external_id}: {e}\n{traceback.format_exc()}"
            errors.append(error_msg)
            print(f"  ❌ Error: {e}")
            continue
    
    client.close()
    
    print(f"\n{'='*60}")
    print(f"✅ Imported: {imported}")
    print(f"⏭️  Skipped:  {skipped}")
    print(f"❌ Errors:   {len(errors)}")
    print(f"{'='*60}\n")
    
    if errors:
        print("Errors:")
        for error in errors[:5]:
            print(f"  - {error[:200]}")


if __name__ == '__main__':
    import_achievements()
