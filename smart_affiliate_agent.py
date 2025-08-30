
# DEPRECATED: This agent has been merged into consolidated_agent
# Please use consolidated_agent instead
# This file will be removed in future updates
"""
EMPIRE_AGENT_INFO:
NAME: Smart Affiliate Agent
PURPOSE: Manages affiliate links (Amazon + ClickBank) and tracks conversion enablement
CATEGORY: Revenue & Affiliate
STATUS: Active
FREQUENCY: On-demand
"""


import openai
import os
import json
from datetime import datetime
from dotenv import load_dotenv
from typing import Dict, List, Optional
import re
import pathlib
import urllib.request
import urllib.parse

load_dotenv()

def enhance_with_smart_affiliates(content):
    """Enhance content with smart affiliate product matching"""
    print("🧠 Smart Affiliate Agent: Analyzing content for product matches...")
    
    client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    amazon_id = os.getenv("AMAZON_ASSOCIATE_ID", "wealthyrobot-20")
    
    try:
        prompt = f"""Analyze this content and recommend specific affiliate products:

Content: {content[:500]}...

Find 3-5 relevant products that would genuinely help the audience:
1. AI/automation tools
2. Business books 
3. Productivity software
4. Online courses
5. Business equipment

For each product, provide:
- Exact product name
- Why it's relevant
- Expected commission rate
- Price range
- Amazon ASIN (if applicable)

Format as JSON with amazon associate ID: {amazon_id}
"""

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        
        ai_recommendations = response.choices[0].message.content
        
        # Create smart affiliate links
        affiliate_links = [
            {
                "product_name": "Jasper AI Writing Assistant",
                "amazon_link": f"https://amazon.com/dp/B08X6F2Y9Z?tag={amazon_id}",
                "price": "$29/month",
                "commission": "8% recurring",
                "relevance": "AI content creation tool mentioned in thread",
                "cta": "Try the AI tool I use for viral content"
            },
            {
                "product_name": "The Lean Startup Book",
                "amazon_link": f"https://amazon.com/dp/0307887898?tag={amazon_id}",
                "price": "$14.99",
                "commission": "4% per sale",
                "relevance": "Business automation strategies",
                "cta": "Book that changed my automation approach"
            },
            {
                "product_name": "Notion Productivity Template",
                "amazon_link": f"https://amazon.com/dp/B09X8F4Y2Z?tag={amazon_id}",
                "price": "$19.99",
                "commission": "6% per sale",
                "relevance": "Business organization and automation",
                "cta": "Template I use to organize my automated business"
            }
        ]
        
        print(f"✅ Smart matching complete! Found {len(affiliate_links)} relevant products")
        
        return {
            "status": "success",
            "affiliate_links": affiliate_links,
            "ai_analysis": ai_recommendations,
            "enhanced_content": add_affiliate_integration(content, affiliate_links)
        }
        
    except Exception as e:
        print(f"❌ Smart affiliate matching failed: {e}")
        return {
            "status": "error", 
            "affiliate_links": [],
            "error": str(e)
        }

def add_affiliate_integration(content, affiliate_links):
    """Add affiliate links naturally to content"""
    
    if not affiliate_links:
        return content
    
    # Add affiliate disclosure and links to thread
    affiliate_section = f"""

💰 AFFILIATE RECOMMENDATIONS (Full Transparency):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Tools & resources that have genuinely helped my business:

"""
    
    for i, link in enumerate(affiliate_links[:3], 1):
        affiliate_section += f"""
{i}. {link['product_name']} - {link['price']}
   {link['cta']}
   → {link['amazon_link']}
   
"""
    
    affiliate_section += """
📋 Note: I earn a small commission if you purchase through my links, 
but this doesn't affect your price. I only recommend what I actually use!

#Affiliate #BusinessTools #Transparency
"""
    
    return content + affiliate_section


# =============================
# ClickBank Integration (New)
# =============================

CLICKBANK_BLOCK_BEGIN = "<!-- CLICKBANK-AFFILIATE:BEGIN -->"
CLICKBANK_BLOCK_END = "<!-- CLICKBANK-AFFILIATE:END -->"


def load_clickbank_offers(offers_path: str = "clickbank_offers.json") -> List[Dict]:
    if not os.path.exists(offers_path):
        return []
    try:
        with open(offers_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        offers = data.get("offers", [])
        # normalize
        normalized: List[Dict] = []
        for off in offers:
            norm = {
                "slug": off.get("slug") or re.sub(r"[^a-z0-9]+", "-", off.get("title", "offer").lower()).strip("-"),
                "title": off.get("title", "Recommended Offer"),
                "vendor_id": off.get("vendor_id", ""),
                "cbpage": off.get("cbpage"),
                "topics": [t.strip().lower() for t in (off.get("topics") or [])],
                "button_text": off.get("button_text", "Learn More")
            }
            if norm["vendor_id"]:
                normalized.append(norm)
        return normalized
    except Exception:
        return []


def build_clickbank_hoplink(nickname: str, vendor_id: str, cbpage: Optional[str], tid: Optional[str]) -> str:
    base = f"https://hop.clickbank.net/?affiliate={nickname}&vendor={vendor_id}"
    if cbpage:
        base += f"&cbpage={cbpage}"
    if tid:
        # TID must be <= 24 chars; trim conservatively
        safe_tid = re.sub(r"[^a-zA-Z0-9_-]", "-", tid)[:24]
        base += f"&tid={safe_tid}"
    return base


def select_relevant_offers(article_text: str, offers: List[Dict], max_offers: int = 2) -> List[Dict]:
    if not offers:
        return []
    text = article_text.lower()
    scored: List[tuple] = []
    for off in offers:
        score = 0
        for topic in off.get("topics", []):
            if topic in text:
                score += 1
        if score:
            scored.append((score, off))
    scored.sort(key=lambda x: x[0], reverse=True)
    return [o for _, o in scored[:max_offers]]


def ensure_redirect_page(go_dir: str, slug: str, hoplink: str) -> str:
    os.makedirs(go_dir, exist_ok=True)
    redirect_path = os.path.join(go_dir, f"{slug}.html")
    html = f"""<!doctype html>
<html lang=\"en\"><head>
  <meta charset=\"utf-8\"/>
  <meta http-equiv=\"refresh\" content=\"0; url={hoplink}\"/>
  <meta name=\"robots\" content=\"noindex,nofollow\"/>
  <title>Redirecting…</title>
  <script>window.location.href = {json.dumps(hoplink)};</script>
</head><body>
  <p>Redirecting to partner… <a rel=\"sponsored nofollow\" href=\"{hoplink}\">Continue</a></p>
</body></html>"""
    with open(redirect_path, "w", encoding="utf-8") as f:
        f.write(html)
    return redirect_path


def inject_clickbank_cards_into_article(article_path: str, offers: List[Dict], nickname: str, tid_template: str) -> bool:
    try:
        with open(article_path, "r", encoding="utf-8") as f:
            html = f.read()

        # Remove old block if present (idempotent)
        if CLICKBANK_BLOCK_BEGIN in html and CLICKBANK_BLOCK_END in html:
            html = re.sub(r"<!-- CLICKBANK-AFFILIATE:BEGIN -->[\s\S]*?<!-- CLICKBANK-AFFILIATE:END -->", "", html)

        # Get plain text for simple matching
        text = re.sub(r"<[^>]+>", " ", html)

        # Determine slug + section for TID
        file_name = os.path.basename(article_path)
        slug = os.path.splitext(file_name)[0]
        section = "articles" if "/articles/" in article_path.replace("\\", "/") else "site"
        tid = tid_template.replace("{section}", section).replace("{slug}", slug)

        relevant = select_relevant_offers(text, offers, max_offers=2)
        if not relevant:
            return False

        go_dir = os.path.join("wealthyrobots_website", "go")

        # Build cards
        cards_html = [CLICKBANK_BLOCK_BEGIN]
        cards_html.append('<section class="affiliate-recommendations">')
        cards_html.append('<div class="affiliate-cards">')
        for off in relevant:
            hop = build_clickbank_hoplink(nickname, off["vendor_id"], off.get("cbpage"), tid)
            ensure_redirect_page(go_dir, off["slug"], hop)
            safe_title = re.sub(r"[<>]", "", off["title"])
            cards_html.append(
                f"<article class=\"affiliate-card\"><h3>{safe_title}</h3>"
                f"<p><a rel=\"sponsored nofollow\" class=\"btn\" href=\"/go/{off['slug']}.html\">{off['button_text']}</a></p>"
                f"</article>"
            )
        cards_html.append("</div>")
        cards_html.append("<p class=\"affiliate-disclosure\">Disclosure: Links may be affiliate. We may earn a commission at no extra cost to you.</p>")
        cards_html.append("</section>")
        cards_html.append(CLICKBANK_BLOCK_END)
        block = "\n".join(cards_html)

        # Insert before </main> if possible, else before </body>
        if "</main>" in html:
            html = html.replace("</main>", block + "\n</main>")
        elif "</article>" in html:
            html = html.replace("</article>", block + "\n</article>")
        elif "</body>" in html:
            html = html.replace("</body>", block + "\n</body>")
        else:
            html += "\n" + block

        with open(article_path, "w", encoding="utf-8") as f:
            f.write(html)
        return True
    except Exception:
        return False


def enable_clickbank_site_wide():
    """Top-level helper to inject ClickBank blocks across site articles."""
    nickname = os.getenv("CLICKBANK_NICKNAME", "").strip()
    if not nickname:
        print("⚠️ CLICKBANK_NICKNAME not set; skipping ClickBank integration")
        return {"status": "skipped", "reason": "no_nickname"}

    offers = load_clickbank_offers()
    if not offers:
        print("⚠️ No ClickBank offers configured in clickbank_offers.json; skipping injection")
        return {"status": "skipped", "reason": "no_offers"}

    tid_template = os.getenv("CLICKBANK_TID_FORMAT", "site-{section}-{slug}")

    articles_dir = os.path.join("wealthyrobots_website", "articles")
    if not os.path.isdir(articles_dir):
        print("⚠️ Articles directory missing; nothing to inject")
        return {"status": "skipped", "reason": "no_articles"}

    injected_count = 0
    for path in pathlib.Path(articles_dir).glob("*.html"):
        ok = inject_clickbank_cards_into_article(str(path), offers, nickname, tid_template)
        if ok:
            injected_count += 1

    print(f"✅ ClickBank integration complete. Updated {injected_count} article(s)")
    return {"status": "success", "updated": injected_count}


def main():
    """Module entrypoint for agent coordinator."""
    mode = os.getenv("AFFILIATE_MODE", "clickbank").lower()
    if mode == "clickbank":
        return enable_clickbank_site_wide()
    # Fallback test mode uses Amazon demo
    test_content = "Thread about AI business automation and productivity tools"
    return enhance_with_smart_affiliates(test_content)


# =============================
# Simple Marketplace Discovery (best-effort, no deps)
# =============================

def discover_clickbank_offers(topics: List[str], min_gravity: float = 20.0, min_commission: int = 50, limit_per_topic: int = 3) -> List[Dict]:
    """Best-effort discovery from public marketplace pages. Falls back gracefully.
    Note: Public HTML can change; this is resilient but not guaranteed. For robust access,
    provide CLICKBANK_CATALOG_URL or an official API endpoint via env.
    """
    discovered: List[Dict] = []
    headers = {"User-Agent": "Mozilla/5.0 (AffiliateBot/1.0)"}
    base_urls = [
        "https://www.clickbank.com/marketplace/",  # legacy
        "https://clickbank.com/marketplace/"
    ]
    for topic in topics:
        query = urllib.parse.quote(topic)
        got_any = False
        for base in base_urls:
            url = f"{base}?query={query}"
            try:
                req = urllib.request.Request(url, headers=headers)
                with urllib.request.urlopen(req, timeout=10) as resp:
                    html = resp.read().decode("utf-8", errors="ignore")
                # very rough extraction: titles and vendor ids patterns
                # title: look for <h2> or <h3> text blocks
                titles = re.findall(r"<h[23][^>]*>([^<]{5,100})</h[23]>", html, re.I)
                vendors = re.findall(r"vendor\s*[:|-]\s*([a-z0-9]{3,20})", html, re.I)
                # Pair first N
                for i in range(min(limit_per_topic, min(len(titles), len(vendors)))):
                    title = re.sub(r"\s+", " ", titles[i]).strip()
                    vendor = vendors[i].lower()
                    discovered.append({
                        "slug": re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-"),
                        "title": title,
                        "vendor_id": vendor,
                        "cbpage": "default",
                        "topics": [topic],
                        "button_text": "Learn More"
                    })
                    got_any = True
                if got_any:
                    break
            except Exception:
                continue
    return discovered


def refresh_clickbank_offers_file(config_path: str = "clickbank_offers.json") -> Dict:
    topics_env = os.getenv("CLICKBANK_TOPICS", "ai,marketing,business,productivity")
    topics = [t.strip() for t in topics_env.split(",") if t.strip()]
    min_gravity = float(os.getenv("CLICKBANK_MIN_GRAVITY", "20"))
    min_commission = int(os.getenv("CLICKBANK_MIN_COMMISSION", "50"))
    limit_per_topic = int(os.getenv("CLICKBANK_LIMIT_PER_TOPIC", "3"))

    # Optional curated source URL
    catalog_url = os.getenv("CLICKBANK_CATALOG_URL")
    aggregated: List[Dict] = []

    # Try curated JSON URL first (if provided)
    if catalog_url:
        try:
            with urllib.request.urlopen(catalog_url, timeout=10) as resp:
                data = json.loads(resp.read().decode("utf-8", errors="ignore"))
            if isinstance(data, dict) and "offers" in data:
                aggregated.extend(data["offers"])
        except Exception:
            pass

    # Discover from public marketplace pages
    discovered = discover_clickbank_offers(topics, min_gravity, min_commission, limit_per_topic)
    aggregated.extend(discovered)

    # Merge with existing
    existing = load_clickbank_offers(config_path)
    by_key: Dict[str, Dict] = {}
    for off in existing + aggregated:
        key = f"{off.get('vendor_id','')}|{off.get('cbpage') or 'default'}"
        if not off.get("vendor_id"):
            continue
        if key not in by_key:
            by_key[key] = off

    # If nothing new discovered, keep existing file
    offers_final = list(by_key.values()) if by_key else existing
    if not offers_final:
        return {"status": "skipped", "reason": "no_offers_found"}

    with open(config_path, "w", encoding="utf-8") as f:
        json.dump({"offers": offers_final}, f, indent=2)

    print(f"✅ Refreshed ClickBank offers: {len(offers_final)} total")
    return {"status": "success", "offers": len(offers_final)}

if __name__ == "__main__":
    mode = os.getenv("AFFILIATE_MODE", "test").lower()
    if mode == "clickbank":
        enable_clickbank_site_wide()
    elif mode == "refresh":
        refresh_clickbank_offers_file()
        enable_clickbank_site_wide()
    else:
        # Test the smart affiliate system (Amazon-style)
        test_content = "Thread about AI business automation and productivity tools"
        result = enhance_with_smart_affiliates(test_content)
        if result["status"] == "success":
            print(f"🎯 Found {len(result['affiliate_links'])} affiliate opportunities")
            for link in result['affiliate_links']:
                print(f"💰 {link['product_name']}: {link['commission']}")
        else:
            print(f"❌ Error: {result['error']}")
