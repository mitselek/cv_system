#!/usr/bin/env python3
"""
Import certifications from knowledge_base/certifications/ to EdgeDB.

Certifications have:
- title, issuer (Translation)
- date (IsoDate)
- credential_id, credential_url (optional)
- expiry_date (optional)
- tags (links)
"""
import edgedb
import json
import re
import yaml
from pathlib import Path


def extract_frontmatter(content: str) -> tuple[dict, str]:
    """Extract YAML frontmatter and remaining body."""
    # Remove any HTML comments before parsing
    lines = content.split('\n')
    clean_lines = []
    in_comment = False
    
    for line in lines:
        if '<!--' in line:
            in_comment = True
        if not in_comment:
            clean_lines.append(line)
        if '-->' in line:
            in_comment = False
            continue
    
    content = '\n'.join(clean_lines)
    
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


def import_certifications():
    """Import all certifications from knowledge_base/certifications/."""
    cert_dir = Path('knowledge_base/certifications')
    
    if not cert_dir.exists():
        print(f"❌ Directory not found: {cert_dir}")
        return
    
    client = edgedb.create_client(
        host='localhost',
        port=5656,
        tls_security='insecure'
    )
    
    cert_files = sorted(cert_dir.glob('*.md'))
    print(f"\n📁 Found {len(cert_files)} certification files\n")
    
    imported = 0
    skipped = 0
    errors = 0
    
    for cert_file in cert_files:
        try:
            content = cert_file.read_text()
            frontmatter, body = extract_frontmatter(content)
            
            if not frontmatter:
                print(f"Processing: {cert_file.stem}")
                print(f"  ⚠️  No frontmatter found, skipping\n")
                skipped += 1
                continue
            
            # Extract fields
            external_id = frontmatter.get('id') or cert_file.stem
            
            # Check if already exists
            exists = client.query(
                'SELECT Certification { id } FILTER .external_id = <str>$id LIMIT 1',
                id=external_id
            )
            
            if exists:
                print(f"Processing: {cert_file.stem}")
                print(f"  ⏭️  Already exists, skipping")
                skipped += 1
                continue
            
            print(f"Processing: {cert_file.stem}")
            
            # Title (Translation)
            title = frontmatter.get('title')
            if not title:
                print(f"  ❌ Missing title\n")
                errors += 1
                continue
            
            title_trans = build_translation(title)
            
            # Issuer (Translation)
            issuer = frontmatter.get('issuer')
            if not issuer:
                print(f"  ❌ Missing issuer\n")
                errors += 1
                continue
            
            issuer_trans = build_translation(issuer)
            
            # Date (required)
            date_str = frontmatter.get('date')
            if not date_str:
                print(f"  ❌ Missing date\n")
                errors += 1
                continue
            
            date = parse_date(date_str)
            if not date:
                print(f"  ❌ Invalid date: {date_str}\n")
                errors += 1
                continue
            
            # Optional fields
            credential_id = frontmatter.get('credential_id')
            credential_url = frontmatter.get('credential_url')
            expiry_date = parse_date(frontmatter.get('expiry_date'))
            
            # Verification status
            status = frontmatter.get('status', 'draft')
            status_map = {
                'verified': 'verified',
                'draft': 'draft',
                'unverified': 'unverified',
                'expired': 'expired'
            }
            verification_status = status_map.get(status.lower(), 'draft')
            
            # last_verified (if status is verified)
            last_verified = parse_date(frontmatter.get('last_verified')) or date
            
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
                f"title := <Translation>$title,",
                f"issuer := <Translation>$issuer,",
                f"date := <IsoDate>$date,",
                f"verification_status := <VerificationStatus>$verification_status,",
                f"last_verified := <IsoDate>$last_verified,"
            ]
            
            query_params = {
                'external_id': external_id,
                'title': json.dumps(title_trans),
                'issuer': json.dumps(issuer_trans),
                'date': date,
                'verification_status': verification_status,
                'last_verified': last_verified
            }
            
            if credential_id:
                query_parts.append("credential_id := <str>$credential_id,")
                query_params['credential_id'] = credential_id
            
            if credential_url:
                # Normalize URL
                url = str(credential_url).strip('<>').strip()
                query_parts.append("credential_url := <HttpUrl>$credential_url,")
                query_params['credential_url'] = url
            
            if expiry_date:
                query_parts.append("expiry_date := <IsoDate>$expiry_date,")
                query_params['expiry_date'] = expiry_date
            
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
            INSERT Certification {{
                {chr(10).join('    ' + p for p in query_parts)}
            }}
            """
            
            # Execute
            client.query(query, **query_params)
            
            print(f"  ✅ Imported: {title if isinstance(title, str) else title.get('en') or title.get('et')}")
            imported += 1
            
        except Exception as e:
            print(f"Processing: {cert_file.stem}")
            print(f"  ❌ Error: {e}\n")
            errors += 1
    
    print(f"\n{'='*60}")
    print(f"✅ Imported: {imported}")
    print(f"⏭️  Skipped:  {skipped}")
    print(f"❌ Errors:   {errors}")
    print(f"{'='*60}\n")


if __name__ == '__main__':
    import_certifications()
