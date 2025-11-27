#!/usr/bin/env python3
"""
Riigihanked Document Harvester

Investigates and harvests procurement documents from riigihanked.riik.ee

Usage:
    python harvest.py investigate <procurement_id>
    python harvest.py download <procurement_id>
    python harvest.py search --keywords "IT,tarkvara"
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Any, List, Optional
from datetime import datetime

try:
    import requests
except ImportError:
    print("Error: Required packages not installed.")
    print("Run: pip install requests beautifulsoup4")
    sys.exit(1)


class RiigihankedAPI:
    """Interface to riigihanked.riik.ee platform"""
    
    BASE_URL = "https://riigihanked.riik.ee"
    API_BASE = f"{BASE_URL}/rhr/api/public/v1"
    FILE_BASE = f"{BASE_URL}/filetransfer/client/shared/file"
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36',
            'Accept': 'application/json',
        })
    
    def get_latest_version(self, procurement_id: str) -> int:
        """Get the latest version ID for a procurement"""
        url = f"{self.API_BASE}/procurement/{procurement_id}/latest-version"
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()['value']
    
    def get_documents_list(self, proc_vers_id: int) -> list[dict[str, Any]]:
        """Get list of all documents for a procurement version"""
        url = f"{self.API_BASE}/proc-vers/{proc_vers_id}/documents/general-info"
        response = self.session.get(url)
        response.raise_for_status()
        data = response.json()
        return data.get('procurementDocuments', [])
    
    def get_temp_download_url(self, proc_vers_id: int, doc_old_id: int) -> str:
        """Get temporary download URL for a document"""
        url = f"{self.API_BASE}/proc-vers/{proc_vers_id}/documents/{doc_old_id}/temp-url"
        response = self.session.get(url)
        response.raise_for_status()
        temp_path = response.json()['value']
        return f"{self.BASE_URL}{temp_path}"
    
    def download_file(self, url: str, output_path: Path) -> None:
        """Download a file from URL to output path"""
        response = self.session.get(url, stream=True)
        response.raise_for_status()
        
        with open(output_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
    
    def investigate_procurement(self, procurement_id: str) -> dict[str, Any]:
        """
        Investigate a procurement to discover API structure
        
        Args:
            procurement_id: Procurement ID (e.g., "9559644")
        
        Returns:
            Dict with discovered information
        """
        print(f"Investigating procurement {procurement_id}...")
        
        # Try different potential API endpoints
        potential_endpoints = [
            f"{self.API_BASE}/procurements/{procurement_id}",
            f"{self.API_BASE}/procurement/{procurement_id}",
            f"{self.BASE_URL}/api/procurements/{procurement_id}",
            f"{self.BASE_URL}/api/v1/procurements/{procurement_id}",
        ]
        
        results: dict[str, Any] = {
            'procurement_id': procurement_id,
            'timestamp': datetime.now().isoformat(),
            'endpoints_tested': [],
            'working_endpoint': None,
            'data': None,
            'error': None
        }
        
        for endpoint in potential_endpoints:
            print(f"  Testing: {endpoint}")
            try:
                response = self.session.get(endpoint, timeout=10)
                results['endpoints_tested'].append({
                    'url': endpoint,
                    'status_code': response.status_code,
                    'content_type': response.headers.get('Content-Type', '')
                })
                
                if response.status_code == 200:
                    print(f"  ✓ Success! Status: {response.status_code}")
                    results['working_endpoint'] = endpoint
                    
                    # Try to parse as JSON
                    try:
                        results['data'] = response.json()
                        print(f"  ✓ JSON response received")
                        break
                    except json.JSONDecodeError:
                        # Maybe HTML page
                        results['data'] = {
                            'html_length': len(response.text),
                            'html_preview': response.text[:500]
                        }
                        print(f"  ⚠ HTML response (length: {len(response.text)})")
                else:
                    print(f"  ✗ Status: {response.status_code}")
                    
            except requests.RequestException as e:
                print(f"  ✗ Error: {e}")
                results['endpoints_tested'][-1]['error'] = str(e)
        
        if not results['working_endpoint']:
            print("\n⚠ No working API endpoint found.")
            print("The platform likely uses a JavaScript SPA with dynamic data loading.")
            print("\nRecommendation:")
            print("1. Use browser developer tools to inspect network traffic")
            print("2. Look for XHR/Fetch requests when loading a procurement")
            print("3. Copy the actual API endpoint and update this script")
        
        return results
    
    
    def download_documents(self, procurement_id: str, output_dir: Optional[Path] = None) -> dict[str, Any]:
        """
        Download all documents for a procurement
        
        Args:
            procurement_id: Procurement ID (e.g., "9559644")
            output_dir: Optional custom output directory
        
        Returns:
            Dict with download results
        """
        print(f"🔍 Fetching documents for procurement {procurement_id}...")
        
        # Get latest version
        version_id = self.get_latest_version(procurement_id)
        print(f"📌 Latest version: {version_id}")
        
        # Get documents list
        documents = self.get_documents_list(version_id)
        print(f"📄 Found {len(documents)} documents")
        
        # Create output directory
        if output_dir is None:
            output_dir = Path(f"procurements/{procurement_id}")
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Save metadata
        metadata: dict[str, Any] = {
            'procurement_id': procurement_id,
            'version_id': version_id,
            'downloaded_at': datetime.now().isoformat(),
            'documents': documents
        }
        metadata_path = output_dir / 'metadata.json'
        with open(metadata_path, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)
        print(f"💾 Saved metadata to {metadata_path}")
        
        # Download each document
        downloaded: list[dict[str, Any]] = []
        for doc in documents:
            doc_id = doc['procurementDocumentOldId']
            filename = doc['fileName']
            filepath = output_dir / filename
            
            try:
                print(f"⬇️  Downloading: {filename}...", end=' ')
                temp_url = self.get_temp_download_url(version_id, doc_id)
                self.download_file(temp_url, filepath)
                file_size = filepath.stat().st_size
                print(f"✅ ({file_size:,} bytes)")
                
                downloaded.append({
                    'filename': filename,
                    'doc_id': doc_id,
                    'size': file_size,
                    'path': str(filepath)
                })
            except Exception as e:
                print(f"❌ Failed: {e}")
        
        print(f"\n✨ Downloaded {len(downloaded)}/{len(documents)} documents to {output_dir}")
        return {
            'procurement_id': procurement_id,
            'version_id': version_id,
            'total_documents': len(documents),
            'downloaded': len(downloaded),
            'output_dir': str(output_dir),
            'files': downloaded
        }
    
    def search_procurements(self, keywords: List[str], filters: Optional[dict[str, Any]] = None) -> list[dict[str, Any]]:
        """
        Search for procurements matching keywords
        
        Args:
            keywords: List of keywords to search for
            filters: Optional filters (status, date range, etc.)
        
        Returns:
            List of matching procurements
        """
        print(f"Searching for procurements with keywords: {', '.join(keywords)}")
        
        # This will need to be implemented once we discover the search API
        print("⚠ Not yet implemented - need to discover search API endpoint first")
        
        return []


def main():
    parser = argparse.ArgumentParser(
        description='Harvest procurement documents from riigihanked.riik.ee'
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Command to execute')
    
    # Investigate command
    investigate_parser = subparsers.add_parser(
        'investigate',
        help='Investigate API structure for a procurement'
    )
    investigate_parser.add_argument('procurement_id', help='Procurement ID')
    investigate_parser.add_argument(
        '--output',
        default='investigation_results.json',
        help='Output file for investigation results'
    )
    
    # Download command
    download_parser = subparsers.add_parser(
        'download',
        help='Download documents for a procurement'
    )
    download_parser.add_argument('procurement_id', help='Procurement ID')
    download_parser.add_argument(
        '--output-dir',
        default='procurements',
        help='Directory to save documents'
    )
    
    # Search command
    search_parser = subparsers.add_parser(
        'search',
        help='Search for procurements'
    )
    search_parser.add_argument(
        '--keywords',
        required=True,
        help='Comma-separated keywords (e.g., "IT,tarkvara,arendus")'
    )
    search_parser.add_argument(
        '--output',
        default='search_results.json',
        help='Output file for search results'
    )
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    api = RiigihankedAPI()
    
    if args.command == 'investigate':
        results = api.investigate_procurement(args.procurement_id)
        
        # Save results
        output_path = Path(args.output)
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        print(f"\n✓ Investigation results saved to: {output_path}")
        
        if results['working_endpoint']:
            print(f"\n✓ Working endpoint found: {results['working_endpoint']}")
            if results['data']:
                print("\nData preview:")
                print(json.dumps(results['data'], indent=2, ensure_ascii=False)[:1000])
        
        return 0 if results['working_endpoint'] else 1
    
    elif args.command == 'download':
        output_dir = Path(args.output_dir) if args.output_dir else None
        
        results = api.download_documents(args.procurement_id, output_dir)
        
        if results['downloaded'] > 0:
            print(f"\n✅ Success! Downloaded {results['downloaded']}/{results['total_documents']} documents")
            return 0
        else:
            print("\n❌ No files downloaded")
            return 1
    
    elif args.command == 'search':
        keywords = [k.strip() for k in args.keywords.split(',')]
        
        results = api.search_procurements(keywords)
        
        # Save results
        output_path = Path(args.output)
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        print(f"\n✓ Search results saved to: {output_path}")
        print(f"Found {len(results)} procurement(s)")
        
        return 0


if __name__ == '__main__':
    sys.exit(main())
