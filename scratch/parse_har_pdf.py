import json
import sys

def analyze_har(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        har_data = json.load(f)
        
    entries = har_data.get('log', {}).get('entries', [])
    for entry in entries:
        req = entry.get('request', {})
        url = req.get('url', '')
        if 'pdf' in url.lower() or 'export' in url.lower() or 'profile' in url.lower():
            res = entry.get('response', {})
            mime_type = res.get('content', {}).get('mimeType', '')
            if 'pdf' in mime_type.lower() or 'pdf' in url.lower():
                print(f"URL: {url}")
                print(f"Method: {req.get('method')}")
                print(f"Response Status: {res.get('status')}")
                print(f"MIME Type: {mime_type}")
                print("-" * 40)

if __name__ == "__main__":
    analyze_har("/Users/maymay/projects/linkedin-cv-updater/pdfExport.har")
