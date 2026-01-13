#!/usr/bin/env python3
"""
Import languages from knowledge_base/languages/ to EdgeDB.

KnowledgeBaseLanguage has:
- name (Translation)
- proficiency (JSON: {listening, reading, speaking, presentation, writing})
- evidence (links to Experience)
- tags (links)
"""
import edgedb
import json
import re
import yaml
from pathlib import Path


def extract_frontmatter(content: str) -> tuple[dict, str]:
    """Extract YAML frontmatter and remaining body."""
    # Remove all HTML comments first
    content = re.sub(r'<!--.*?-->', '', content, flags=re.DOTALL)
    
    # Normalize line endings and strip leading whitespace
    content = content.strip()
    
    # Check for frontmatter
    if not content.startswith('---'):
        return {}, content
    
    # Find end of frontmatter
    parts = content.split('---', 2)
    if len(parts) < 3:
        return {}, content
    
    try:
        frontmatter = yaml.safe_load(parts[1])
        body = parts[2].strip()
        return frontmatter or {}, body
    except yaml.YAMLError as e:
        print(f"  ⚠️  YAML error: {e}")
        return {}, content


def parse_bilingual_body(body: str) -> dict[str, str]:
    """Parse body with ## et and ## en sections."""
    if not body:
        return {}
    
    result = {}
    current_lang = None
    current_text = []
    
    for line in body.split('\n'):
        line_lower = line.lower().strip()
        if line_lower == '## et' or line_lower.startswith('## et '):
            if current_lang == 'en':
                result['en'] = '\n'.join(current_text).strip()
            current_lang = 'et'
            current_text = []
        elif line_lower == '## en' or line_lower.startswith('## en '):
            if current_lang == 'et':
                result['et'] = '\n'.join(current_text).strip()
            current_lang = 'en'
            current_text = []
        elif current_lang:
            if line.startswith('##') and 'connection' in line.lower():
                break
            if line.strip() == '---':
                break
            current_text.append(line)
    
    if current_lang == 'et':
        result['et'] = '\n'.join(current_text).strip()
    elif current_lang == 'en':
        result['en'] = '\n'.join(current_text).strip()
    
    return result


def build_translation(data: dict | str) -> dict:
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
    """Parse date string to YYYY-MM-DD format."""
    if not date_str:
        return None
    
    date_str = str(date_str).strip()
    
    if date_str.lower() in ['present', 'current', 'ongoing']:
        return '2026-01-13'
    
    if len(date_str) == 4 and date_str.isdigit():
        return f"{date_str}-01-01"
    
    if len(date_str) == 7 and date_str[4] == '-':
        return f"{date_str}-01"
    
    return date_str


def import_languages():
    """Import all languages from knowledge_base/languages/."""
    lang_dir = Path('knowledge_base/languages')
    
    if not lang_dir.exists():
        print(f"❌ Directory not found: {lang_dir}")
        return
    
    client = edgedb.create_client(
        host='localhost',
        port=5656,
        tls_security='insecure'
    )
    
    lang_files = sorted(lang_dir.glob('*.md'))
    print(f"\n📁 Found {len(lang_files)} language files\n")
    
    imported = 0
    skipped = 0
    errors = 0
    
    for lang_file in lang_files:
        try:
            content = lang_file.read_text()
            frontmatter, body = extract_frontmatter(content)
            
            if not frontmatter:
                print(f"Processing: {lang_file.stem}")
                print(f"  ⚠️  No frontmatter found, skipping\n")
                skipped += 1
                continue
            
            # Extract fields
            external_id = frontmatter.get('id') or lang_file.stem
            
            # Check if already exists
            exists = client.query(
                'SELECT KnowledgeBaseLanguage { id } FILTER .external_id = <str>$id LIMIT 1',
                id=external_id
            )
            
            if exists:
                print(f"Processing: {lang_file.stem}")
                print(f"  ⏭️  Already exists, skipping")
                skipped += 1
                continue
            
            print(f"Processing: {lang_file.stem}")
            
            # Name (Translation)
            name_data = frontmatter.get('language_name') or frontmatter.get('name')
            if not name_data:
                print(f"  ❌ Missing language_name or name\n")
                errors += 1
                continue
            
            name_trans = build_translation(name_data)
            
            # Proficiency (JSON)
            proficiency = frontmatter.get('proficiency', {})
            if not proficiency:
                print(f"  ❌ Missing proficiency\n")
                errors += 1
                continue
            
            # Verification status
            status = frontmatter.get('status', 'draft')
            status_map = {
                'verified': 'verified',
                'draft': 'draft',
                'unverified': 'unverified',
                'expired': 'expired'
            }
            verification_status = status_map.get(status.lower(), 'draft')
            
            # last_verified
            last_verified = parse_date(frontmatter.get('last_verified')) or '2026-01-13'
            
            # Article (bilingual body content)
            bilingual = parse_bilingual_body(body)
            article_trans = None
            if bilingual:
                article_trans = bilingual
            
            # Tags
            tags = frontmatter.get('tags', [])
            
            # Evidence (Experience links by external_id)
            evidence_ids = frontmatter.get('evidence', [])
            
            # Build query
            query_parts = [
                f"external_id := <str>$external_id,",
                f"name := <Translation>$name,",
                f"proficiency := <LanguageProficiency>$proficiency,",
                f"verification_status := <VerificationStatus>$verification_status,",
                f"last_verified := <IsoDate>$last_verified,"
            ]
            
            query_params = {
                'external_id': external_id,
                'name': json.dumps(name_trans),
                'proficiency': json.dumps(proficiency),
                'verification_status': verification_status,
                'last_verified': last_verified
            }
            
            if article_trans:
                query_parts.append("article := <Translation>$article,")
                query_params['article'] = json.dumps(article_trans)
            
            # Tags
            if tags:
                tags_filter = ' OR '.join([f'.name = <str>$tag{i}' for i in range(len(tags))])
                query_parts.append(f"tags := (SELECT Tag FILTER {tags_filter}),")
                for i, tag in enumerate(tags):
                    query_params[f'tag{i}'] = tag
            
            # Evidence (Experience links)
            if evidence_ids:
                evidence_filter = ' OR '.join([f'.external_id = <str>$ev{i}' for i in range(len(evidence_ids))])
                query_parts.append(f"evidence := (SELECT Experience FILTER {evidence_filter}),")
                for i, ev_id in enumerate(evidence_ids):
                    query_params[f'ev{i}'] = ev_id
            
            query = f"""
            INSERT KnowledgeBaseLanguage {{
                {chr(10).join('    ' + p for p in query_parts)}
            }}
            """
            
            # Execute
            client.query(query, **query_params)
            
            # Build display name
            display = name_trans.get('en') or name_trans.get('et') or 'Unknown'
            
            print(f"  ✅ Imported: {display}")
            imported += 1
            
        except Exception as e:
            print(f"Processing: {lang_file.stem}")
            print(f"  ❌ Error: {e}\n")
            errors += 1
    
    print(f"\n{'='*60}")
    print(f"✅ Imported: {imported}")
    print(f"⏭️  Skipped:  {skipped}")
    print(f"❌ Errors:   {errors}")
    print(f"{'='*60}\n")


if __name__ == '__main__':
    import_languages()
