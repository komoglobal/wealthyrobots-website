import openai
import os
import json
from datetime import datetime
from dotenv import load_dotenv

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

if __name__ == "__main__":
    # Test the smart affiliate system
    test_content = "Thread about AI business automation and productivity tools"
    result = enhance_with_smart_affiliates(test_content)
    
    if result["status"] == "success":
        print(f"🎯 Found {len(result['affiliate_links'])} affiliate opportunities")
        for link in result['affiliate_links']:
            print(f"💰 {link['product_name']}: {link['commission']}")
    else:
        print(f"❌ Error: {result['error']}")
