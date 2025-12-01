#!/usr/bin/env python3
"""
Interactive cookie extractor - paste cookies from browser DevTools.
"""

import json
from pathlib import Path


def extract_from_devtools():
    """Extract cookies from browser developer tools paste."""
    print("=" * 80)
    print("COOKIE EXTRACTOR - Paste from Browser DevTools")
    print("=" * 80)
    print()
    print("Instructions:")
    print("1. Open the job portal (duunitori.fi, linkedin.com, etc.) and log in")
    print("2. Press F12 to open Developer Tools")
    print("3. Go to:")
    print("   • Chrome/Brave/Edge: Application → Cookies → select domain")
    print("   • Firefox: Storage → Cookies → select domain")
    print("4. Copy ALL cookies (you can select all rows)")
    print()
    print("Then paste cookies here in ONE of these formats:")
    print()
    print("Format 1 (simple): name1=value1; name2=value2; name3=value3")
    print("Format 2 (one per line):")
    print("  name1: value1")
    print("  name2: value2")
    print()
    print("Paste cookies and press Enter twice when done:")
    print("-" * 80)
    
    lines = []
    empty_count = 0
    
    while empty_count < 2:
        try:
            line = input()
            if not line.strip():
                empty_count += 1
            else:
                empty_count = 0
                lines.append(line.strip())
        except EOFError:
            break
    
    cookie_text = ' '.join(lines)
    
    # Parse cookies
    cookies = {}
    
    # Try format 1: name=value; name=value
    if '=' in cookie_text and ';' in cookie_text:
        for pair in cookie_text.split(';'):
            pair = pair.strip()
            if '=' in pair:
                name, value = pair.split('=', 1)
                cookies[name.strip()] = value.strip()
    
    # Try format 2: name: value (line by line)
    elif ':' in cookie_text:
        for line in lines:
            if ':' in line:
                name, value = line.split(':', 1)
                cookies[name.strip()] = value.strip()
    
    # Try format 3: just dump everything and try to parse
    else:
        parts = cookie_text.replace('\t', ' ').split()
        i = 0
        while i < len(parts) - 1:
            if parts[i] and parts[i+1]:
                cookies[parts[i]] = parts[i+1]
            i += 2
    
    if not cookies:
        print("\n❌ Could not parse cookies. Please try again.")
        return None
    
    print(f"\n✅ Extracted {len(cookies)} cookies:")
    for name in list(cookies.keys())[:5]:
        print(f"  • {name}")
    if len(cookies) > 5:
        print(f"  ... and {len(cookies) - 5} more")
    
    return cookies


def save_cookies(cookies: dict, portal: str):
    """Save cookies to file."""
    config_dir = Path.home() / '.config'
    config_dir.mkdir(exist_ok=True)
    
    cookie_file = config_dir / f'job_scraper_cookies_{portal}.json'
    
    with open(cookie_file, 'w') as f:
        json.dump(cookies, f, indent=2)
    
    # Set restrictive permissions
    cookie_file.chmod(0o600)
    
    print(f"\n💾 Cookies saved to: {cookie_file}")
    return cookie_file


def main():
    """Main entry point."""
    portals = {
        '1': ('duunitori', 'Duunitori.fi'),
        '2': ('linkedin', 'LinkedIn'),
        '3': ('tyomarkkinatori', 'Tyomarkkinatori.fi'),
    }
    
    print("\nWhich portal are these cookies for?")
    for key, (_, name) in portals.items():
        print(f"{key}. {name}")
    
    choice = input("\nEnter number: ").strip()
    
    if choice not in portals:
        print("Invalid choice")
        return
    
    portal_key, portal_name = portals[choice]
    
    print(f"\n📋 Extracting cookies for {portal_name}")
    print()
    
    cookies = extract_from_devtools()
    
    if cookies:
        cookie_file = save_cookies(cookies, portal_key)
        
        print("\n" + "=" * 80)
        print("✅ SETUP COMPLETE!")
        print("=" * 80)
        print(f"\nNow you can search {portal_name}:")
        print()
        print(f"  python scripts/job_scraper.py \"project manager IT\" \\")
        print(f"    --portal {portal_key} \\")
        print(f"    --cookies {cookie_file}")
        print()


if __name__ == '__main__':
    main()
