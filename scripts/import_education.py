#!/usr/bin/env python3
"""
Import education records from knowledge_base/education/ to EdgeDB.

Education has:
- institutions, fields (array<Translation>)
- degree (optional Translation)
- dates (tuple<start, end>)
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


def import_education():
    """Import all education records from knowledge_base/education/."""
    edu_dir = Path('knowledge_base/education')
    
    if not edu_dir.exists():
        print(f"❌ Directory not found: {edu_dir}")
        return
    
    client = edgedb.create_client(
        host='localhost',
        port=5656,
        tls_security='insecure'
    )
    
    edu_files = sorted(edu_dir.glob('*.md'))
    print(f"\n📁 Found {len(edu_files)} education files\n")
    
    imported = 0
    skipped = 0
    errors = 0
    
    for edu_file in edu_files:
        try:
            content = edu_file.read_text()
            frontmatter, body = extract_frontmatter(content)
            
            if not frontmatter:
                print(f"Processing: {edu_file.stem}")
                print(f"  ⚠️  No frontmatter found, skipping\n")
                skipped += 1
                continue
            
            # Extract fields
            external_id = frontmatter.get('id') or edu_file.stem
            
            # Check if already exists
            exists = client.query(
                'SELECT Education { id } FILTER .external_id = <str>$id LIMIT 1',
                id=external_id
            )
            
            if exists:
                print(f"Processing: {edu_file.stem}")
                print(f"  ⏭️  Already exists, skipping")
                skipped += 1
                continue
            
            print(f"Processing: {edu_file.stem}")
            
            # Institutions (array<Translation>)
            institutions_data = frontmatter.get('institutions', [])
            if not institutions_data:
                print(f"  ❌ Missing institutions\n")
                errors += 1
                continue
            
            institutions = []
            for inst in institutions_data:
                if isinstance(inst, dict):
                    name_data = inst.get('name', inst)  # Support both {name: {...}} and {...}
                    institutions.append(build_translation(name_data))
                else:
                    institutions.append(build_translation(inst))
            
            # Fields (array<Translation>)
            fields_data = frontmatter.get('fields', [])
            if not fields_data:
                print(f"  ❌ Missing fields\n")
                errors += 1
                continue
            
            fields = []
            for field in fields_data:
                fields.append(build_translation(field))
            
            # Degree (optional Translation)
            degree_data = frontmatter.get('degree')
            degree_trans = build_translation(degree_data) if degree_data else None
            
            # Dates (required tuple)
            dates_data = frontmatter.get('dates', {})
            start_date = parse_date(dates_data.get('start'))
            end_date = parse_date(dates_data.get('end'))
            
            if not start_date or not end_date:
                print(f"  ❌ Missing or invalid dates\n")
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
            last_verified = parse_date(frontmatter.get('last_verified')) or end_date
            
            # Article (bilingual body content)
            bilingual = parse_bilingual_body(body)
            article_trans = None
            if bilingual:
                article_trans = bilingual
            
            # Tags
            tags = frontmatter.get('tags', [])
            
            # Build query
            query_parts = [
                f"external_id := <str>$external_id,",
                f"institutions := <array<Translation>>$institutions,",
                f"fields := <array<Translation>>$fields,",
                f"dates := (`start` := <IsoDate>$start_date, `end` := <IsoDate>$end_date),",
                f"verification_status := <VerificationStatus>$verification_status,",
                f"last_verified := <IsoDate>$last_verified,"
            ]
            
            query_params = {
                'external_id': external_id,
                'institutions': [json.dumps(inst) for inst in institutions],
                'fields': [json.dumps(field) for field in fields],
                'start_date': start_date,
                'end_date': end_date,
                'verification_status': verification_status,
                'last_verified': last_verified
            }
            
            if degree_trans:
                query_parts.append("degree := <Translation>$degree,")
                query_params['degree'] = json.dumps(degree_trans)
            
            if article_trans:
                query_parts.append("article := <Translation>$article,")
                query_params['article'] = json.dumps(article_trans)
            
            # Tags
            if tags:
                tags_filter = ' OR '.join([f'.name = <str>${i}' for i in range(len(tags))])
                query_parts.append(f"tags := (SELECT Tag FILTER {tags_filter})")
                for i, tag in enumerate(tags):
                    query_params[str(i)] = tag
            
            query = f"""
            INSERT Education {{
                {chr(10).join('    ' + p for p in query_parts)}
            }}
            """
            
            # Execute
            client.query(query, **query_params)
            
            # Build display name
            display = institutions[0].get('en') or institutions[0].get('et') or 'Unknown'
            
            print(f"  ✅ Imported: {display}")
            imported += 1
            
        except Exception as e:
            print(f"Processing: {edu_file.stem}")
            print(f"  ❌ Error: {e}\n")
            errors += 1
    
    print(f"\n{'='*60}")
    print(f"✅ Imported: {imported}")
    print(f"⏭️  Skipped:  {skipped}")
    print(f"❌ Errors:   {errors}")
    print(f"{'='*60}\n")


if __name__ == '__main__':
    import_education()
