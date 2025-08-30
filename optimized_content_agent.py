#!/usr/bin/env python3
"""
EMPIRE_AGENT_INFO:
NAME: Optimized Content Generation Agent
PURPOSE: Creates comprehensive educational and affiliate content with SEO optimization and deployment
CATEGORY: Content & Social Media
STATUS: Active - Optimized
FREQUENCY: Continuous
"""

import openai
import os
import json
import requests
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

class OptimizedContentAgent:
    def __init__(self):
        """Initialize the Optimized Content Generation Agent"""
        self.client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.brand = "WealthyRobot"
        self.niche = "AI Automation Revenue Generation"
        self.strategy = "80% Educational Value + 20% Smart Monetization"
        
        # Enhanced performance tracking
        self.performance_metrics = {
            "content_created": 0,
            "engagement_score": 0,
            "revenue_generated": 0,
            "seo_optimized": 0,
            "affiliate_integrated": 0
        }
        
        # Content database
        self.content_database = []
        
    def analyze_trending_topics(self):
        """Analyze trending topics with enhanced AI focus"""
        print("📈 Analyzing AI automation revenue topics...")
        
        prompt = """
        You are an AI Content Strategist. Identify 5 trending topics in AI automation and revenue generation for 2025.
        
        Focus on:
        - AI automation strategies that generate real revenue
        - Tools and techniques for passive income
        - Business automation opportunities
        - Emerging AI technologies with monetization potential
        
        Return JSON format with:
        {
            "trending_topics": [
                {
                    "topic": "topic name",
                    "reason": "why it's trending",
                    "content_types": ["blog", "video", "social", "email"],
                    "monetization_potential": 1-10,
                    "target_audience": "audience description",
                    "keywords": ["keyword1", "keyword2"],
                    "affiliate_opportunities": ["product1", "product2"]
                }
            ]
        }
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"❌ Error analyzing topics: {e}")
            return self.get_fallback_topics()
    
    def get_fallback_topics(self):
        """Fallback topics focused on AI revenue"""
        return {
            "trending_topics": [
                {
                    "topic": "AI Revenue Automation: From $0 to $50K Monthly",
                    "reason": "Entrepreneurs need proven systems to scale revenue with AI",
                    "content_types": ["blog", "video", "social"],
                    "monetization_potential": 10,
                    "target_audience": "Business owners seeking automated revenue systems",
                    "keywords": ["AI revenue automation", "passive income AI", "business automation"],
                    "affiliate_opportunities": ["AI tools", "automation software", "business courses"]
                }
            ]
        }
    
    def generate_content_piece(self, topic, content_type="blog"):
        """Generate optimized content with SEO and affiliate integration"""
        print(f"✍️ Generating {content_type} content for: {topic}")
        
        prompts = {
            "blog": f"""
            Create a comprehensive blog post about: {topic}
            
            Requirements:
            - 1500-3000 words
            - SEO optimized with target keywords
            - Include affiliate product recommendations naturally
            - Educational value with actionable insights
            - Professional tone for business audience
            - Include call-to-action for email signup
            
            Format with proper headings, bullet points, and engaging content.
            """,
            "social": f"""
            Create a viral Twitter thread about: {topic}
            
            Requirements:
            - 8-12 tweets in thread format
            - Educational value with viral potential
            - Include affiliate links naturally
            - Use engaging hooks and storytelling
            - End with strong call-to-action
            
            Format as TWEET 1:, TWEET 2:, etc.
            """,
            "email": f"""
            Create an email newsletter about: {topic}
            
            Requirements:
            - 500-800 words
            - Personal and engaging tone
            - Include affiliate recommendations
            - Clear call-to-action
            - Value-focused content
            """
        }
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompts.get(content_type, prompts["blog"])}],
                temperature=0.6
            )
            
            content = {
                "type": content_type,
                "topic": topic,
                "content": response.choices[0].message.content,
                "created_at": datetime.now().isoformat(),
                "status": "ready_for_deployment"
            }
            
            self.content_database.append(content)
            self.performance_metrics["content_created"] += 1
            
            return content
            
        except Exception as e:
            return f"Error generating content: {str(e)}"
    
    def optimize_for_seo(self, content):
        """Optimize content for SEO with enhanced features"""
        print("🔍 Optimizing content for SEO...")
        
        prompt = f"""
        Optimize this content for SEO: {content['content'][:500]}...
        
        Provide:
        1. Optimized title (60 chars max)
        2. Meta description (160 chars max)
        3. 5 primary keywords
        4. 10 long-tail keywords
        5. Internal linking suggestions
        6. Content structure improvements
        7. Schema markup suggestions
        8. Featured snippet optimization
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3
            )
            
            self.performance_metrics["seo_optimized"] += 1
            return response.choices[0].message.content
            
        except Exception as e:
            return f"Error optimizing SEO: {str(e)}"
    
    def integrate_affiliate_products(self, content, topic):
        """Integrate affiliate products naturally into content"""
        print("💰 Integrating affiliate products...")
        
        # Amazon affiliate products for AI automation
        affiliate_products = {
            "AI automation": [
                {"name": "The AI Advantage Book", "link": "https://amazon.com/dp/B0XXXXX", "commission": "8%"},
                {"name": "AI Business Tools Course", "link": "https://amazon.com/dp/B0XXXXX", "commission": "8%"}
            ],
            "business automation": [
                {"name": "Automation Software Suite", "link": "https://amazon.com/dp/B0XXXXX", "commission": "8%"},
                {"name": "Business Process Guide", "link": "https://amazon.com/dp/B0XXXXX", "commission": "8%"}
            ]
        }
        
        # Find relevant products
        relevant_products = []
        for category, products in affiliate_products.items():
            if category.lower() in topic.lower():
                relevant_products.extend(products)
        
        if relevant_products:
            self.performance_metrics["affiliate_integrated"] += 1
            
            # Integrate products naturally
            integration_text = "\n\n**Recommended Resources:**\n"
            for product in relevant_products[:2]:  # Limit to 2 products
                integration_text += f"- [{product['name']}]({product['link']}) - {product['commission']} commission\n"
            
            content['content'] += integration_text
        
        return content
    
    def deploy_content(self, content):
        """Deploy content to appropriate platforms"""
        print("🚀 Deploying content...")
        
        if content['type'] == 'blog':
            # Create HTML file for website
            html_content = self.create_html_content(content)
            filename = f"ai_automation_article_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
            
            with open(filename, 'w') as f:
                f.write(html_content)
            
            print(f"✅ Blog content deployed: {filename}")
            
        elif content['type'] == 'social':
            # Save for social media posting
            filename = f"smart_viral_thread_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            
            with open(filename, 'w') as f:
                f.write(content['content'])
            
            print(f"✅ Social content ready: {filename}")
        
        return filename
    
    def create_html_content(self, content):
        """Create HTML content for website deployment"""
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{content['topic']} | Wealthy Robots Empire</title>
    <meta name="description" content="Learn proven AI automation strategies for revenue generation. Join 1000+ entrepreneurs building AI empires.">
    <style>
        body {{ font-family: 'Segoe UI', sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; line-height: 1.6; }}
        h1 {{ color: #4f46e5; }}
        .affiliate {{ background: #f0f9ff; padding: 15px; border-left: 4px solid #4f46e5; margin: 20px 0; }}
        .cta {{ background: #4f46e5; color: white; padding: 20px; text-align: center; border-radius: 10px; margin: 30px 0; }}
        .cta a {{ color: white; text-decoration: none; font-weight: bold; }}
    </style>
</head>
<body>
    <header>
        <h1>🤖 WealthyRobot Empire</h1>
        <p>AI Automation Strategies That Actually Make Money</p>
    </header>
    
    <article>
        {content['content'].replace('#', '<h2>').replace('##', '<h3>').replace('###', '<h4>')}
    </article>
    
    <div class="cta">
        <h3>Ready to Build Your AI Revenue Empire?</h3>
        <p><a href="https://wealthyrobots.com">Join 1000+ Entrepreneurs → WealthyRobots.com</a></p>
    </div>
    
    <footer>
        <p>© 2025 Wealthy Robots Empire | Follow @WealthyRobot on Twitter</p>
    </footer>
</body>
</html>"""
    
    def run_optimized_cycle(self):
        """Run complete optimized content generation cycle"""
        print("=" * 60)
        print("✍️ OPTIMIZED CONTENT AGENT - COMPLETE CYCLE")
        print("=" * 60)
        
        # Step 1: Analyze trends
        trends = self.analyze_trending_topics()
        print("\n📊 TRENDING TOPICS ANALYZED")
        
        # Step 2: Generate comprehensive content
        try:
            import json
            trends_data = json.loads(trends) if isinstance(trends, str) else trends
            top_topic = trends_data["trending_topics"][0]["topic"]
        except:
            top_topic = "AI Revenue Automation Strategies"
        
        # Step 3: Create multiple content types
        blog_content = self.generate_content_piece(top_topic, "blog")
        social_content = self.generate_content_piece(top_topic, "social")
        email_content = self.generate_content_piece(top_topic, "email")
        
        # Step 4: Optimize for SEO
        seo_optimization = self.optimize_for_seo(blog_content)
        
        # Step 5: Integrate affiliate products
        blog_content = self.integrate_affiliate_products(blog_content, top_topic)
        
        # Step 6: Deploy content
        blog_file = self.deploy_content(blog_content)
        social_file = self.deploy_content(social_content)
        
        # Step 7: Save comprehensive report
        report = {
            "cycle_date": datetime.now().isoformat(),
            "trending_topics": trends,
            "content_created": [blog_content, social_content, email_content],
            "seo_optimization": seo_optimization,
            "performance_metrics": self.performance_metrics,
            "deployed_files": [blog_file, social_file]
        }
        
        with open(f"content_cycle_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json", 'w') as f:
            json.dump(report, f, indent=2)
        
        print("\n✅ Optimized content cycle complete!")
        return report

if __name__ == "__main__":
    agent = OptimizedContentAgent()
    agent.run_optimized_cycle()
