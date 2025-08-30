#!/usr/bin/env python3
"""
Test Website Access
Check what's actually happening with website pages
"""

import urllib.request
import urllib.error
import subprocess
import time
import os

def test_website():
    """Test website accessibility"""
    print("🔍 TESTING WEBSITE ACCESS")
    print("=" * 40)
    
    # Start server
    print("Starting test server...")
    server_process = subprocess.Popen(
        ["python3", "-m", "http.server", "8000"],
        cwd="wealthyrobots_website",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    time.sleep(2)
    
    # Test pages
    pages_to_test = [
        "/",
        "/articles/",
        "/strategies/",
        "/tools/",
        "/resources/",
        "/about/",
        "/contact/"
    ]
    
    results = {}
    
    for page in pages_to_test:
        try:
            url = f"http://localhost:8000{page}"
            print(f"\nTesting: {page}")
            
            response = urllib.request.urlopen(url, timeout=10)
            content = response.read().decode('utf-8')
            
            status = response.getcode()
            content_length = len(content)
            
            print(f"  Status: {status}")
            print(f"  Content Length: {content_length}")
            
            # Check for key elements
            has_title = '<title>' in content
            has_nav = '<nav' in content
            has_footer = '<footer' in content
            has_css = 'main.css' in content
            
            print(f"  Has Title: {has_title}")
            print(f"  Has Navigation: {has_nav}")
            print(f"  Has Footer: {has_footer}")
            print(f"  Has CSS: {has_css}")
            
            # Check for specific content
            if page == "/articles/":
                article_links = content.count('article_') + content.count('.html')
                print(f"  Article Links Found: {article_links}")
            
            results[page] = {
                "status": status,
                "content_length": content_length,
                "has_title": has_title,
                "has_nav": has_nav,
                "has_footer": has_footer,
                "has_css": has_css
            }
            
        except urllib.error.HTTPError as e:
            print(f"  ❌ HTTP Error: {e.code}")
            results[page] = {"error": f"HTTP {e.code}"}
        except urllib.error.URLError as e:
            print(f"  ❌ URL Error: {e}")
            results[page] = {"error": str(e)}
        except Exception as e:
            print(f"  ❌ Error: {e}")
            results[page] = {"error": str(e)}
    
    # Test individual article
    try:
        article_url = "http://localhost:8000/articles/article_ai_automation_revenue_generation_strategies_20250806_230119.html"
        print(f"\nTesting individual article...")
        
        response = urllib.request.urlopen(article_url, timeout=10)
        content = response.read().decode('utf-8')
        
        status = response.getcode()
        content_length = len(content)
        
        print(f"  Status: {status}")
        print(f"  Content Length: {content_length}")
        print(f"  Has Navigation: {'<nav' in content}")
        print(f"  Has CSS: {'main.css' in content}")
        
    except Exception as e:
        print(f"  ❌ Article Error: {e}")
    
    # Stop server
    server_process.terminate()
    server_process.wait()
    
    print(f"\n📊 SUMMARY:")
    for page, result in results.items():
        if "error" in result:
            print(f"  {page}: ❌ {result['error']}")
        else:
            print(f"  {page}: ✅ {result['status']} ({result['content_length']} chars)")
    
    return results

if __name__ == "__main__":
    test_website()
