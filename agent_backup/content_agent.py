import openai
import os
import json
import requests
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

class ContentGenerationAgent:
    def __init__(self):
        self.client = openai.OpenAI(
            api_key=os.getenv("OPENAI_API_KEY")
        )
        self.content_database = []
        self.performance_metrics = {
            "content_created": 0,
            "engagement_score": 0,
            "revenue_generated": 0
        }
    
    def analyze_trending_topics(self):
        """Identify trending topics for content creation"""
        print("📈 Content Agent: Analyzing trending topics...")
        
        prompt = """
        You are a Content Generation AI. Identify 5 trending topics in July 2025 that would be perfect for:
        - Blog posts
        - Social media content  
        - YouTube videos
        - Email newsletters
        
        Focus on topics that:
        - Have high engagement potential
        - Are monetizable through affiliate marketing
        - Appeal to tech-savvy audiences
        - Have strong SEO potential
        
        Return JSON format:
        {
            "trending_topics": [
                {
                    "topic": "topic name",
                    "reason": "why it's trending",
                    "content_types": ["blog", "video", "social"],
                    "monetization_potential": "1-10 scale",
                    "target_audience": "audience description",
                    "keywords": ["keyword1", "keyword2"]
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
            return f"Error analyzing trends: {str(e)}"
    
    def generate_content_piece(self, topic, content_type="blog"):
        """Generate specific content piece"""
        print(f"✍️ Content Agent: Creating {content_type} content about {topic}...")
        
        prompts = {
            "blog": f"""
            Write a comprehensive, engaging blog post about: {topic}
            
            Requirements:
            - 800-1200 words
            - SEO optimized with natural keyword integration
            - Include actionable tips
            - Add call-to-action for affiliate products
            - Engaging headline and subheadings
            - Include spaces for affiliate links
            """,
            
            "social": f"""
            Create 5 engaging social media posts about: {topic}
            
            Requirements:
            - Platform-specific (Twitter, LinkedIn, Instagram, Facebook, TikTok)
            - Include relevant hashtags
            - Engaging hooks
            - Call-to-action
            - Opportunity for affiliate links
            """,
            
            "email": f"""
            Write an email newsletter about: {topic}
            
            Requirements:
            - Compelling subject line
            - Personal, conversational tone
            - Value-packed content
            - Clear call-to-action
            - Affiliate product recommendations
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
                "status": "ready_for_review"
            }
            
            self.content_database.append(content)
            self.performance_metrics["content_created"] += 1
            
            return content
            
        except Exception as e:
            return f"Error generating content: {str(e)}"
    
    def optimize_for_seo(self, content):
        """Optimize content for SEO"""
        print("🔍 Content Agent: Optimizing for SEO...")
        
        prompt = f"""
        Optimize this content for SEO: {content['content'][:500]}...
        
        Provide:
        1. Optimized title (60 chars max)
        2. Meta description (160 chars max)  
        3. 5 primary keywords
        4. 10 long-tail keywords
        5. Internal linking suggestions
        6. Content structure improvements
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return f"Error optimizing SEO: {str(e)}"
    
    def suggest_affiliate_products(self, topic):
        """Suggest relevant affiliate products"""
        print("💰 Content Agent: Finding affiliate opportunities...")
        
        prompt = f"""
        For content about "{topic}", suggest 5 affiliate products/services that would be relevant:
        
        Include:
        - Product name and category
        - Why it fits the content
        - Potential commission rate
        - Where to place in content
        - How to naturally integrate
        
        Focus on high-converting, reputable products.
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.5
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return f"Error finding affiliate products: {str(e)}"
    
    def run_content_cycle(self):
        """Execute one complete content generation cycle"""
        print("=" * 60)
        print("✍️ CONTENT GENERATION AGENT - STARTING CYCLE")
        print("=" * 60)
        
        # Step 1: Analyze trends
        trends = self.analyze_trending_topics()
        print("\n📊 TRENDING TOPICS:")
        print(trends)
        
        # Step 2: Generate content for top trend
        # Extract first topic from trends (simplified)
        try:
            import json
            trends_data = json.loads(trends)
            top_topic = trends_data["trending_topics"][0]["topic"]
        except:
            top_topic = "AI Tools for Business Automation"  # Fallback
        
        # Step 3: Create different content types
        blog_content = self.generate_content_piece(top_topic, "blog")
        social_content = self.generate_content_piece(top_topic, "social")
        
        print(f"\n📝 BLOG CONTENT CREATED:")
        print(blog_content["content"][:300] + "...")
        
        print(f"\n📱 SOCIAL CONTENT CREATED:")
        print(social_content["content"][:200] + "...")
        
        # Step 4: SEO optimization
        seo_suggestions = self.optimize_for_seo(blog_content)
        print(f"\n🔍 SEO OPTIMIZATION:")
        print(seo_suggestions)
        
        # Step 5: Affiliate suggestions
        affiliate_suggestions = self.suggest_affiliate_products(top_topic)
        print(f"\n💰 AFFILIATE OPPORTUNITIES:")
        print(affiliate_suggestions)
        
        # Step 6: Save everything
        output = {
            "cycle_date": datetime.now().isoformat(),
            "trending_topics": trends,
            "content_created": [blog_content, social_content],
            "seo_optimization": seo_suggestions,
            "affiliate_suggestions": affiliate_suggestions,
            "performance_metrics": self.performance_metrics
        }
        
        with open('content_agent_output.json', 'w') as f:
            json.dump(output, f, indent=2)
        
        print("\n" + "=" * 60)
        print("✅ CONTENT CYCLE COMPLETE!")
        print("📁 Output saved to content_agent_output.json")
        print(f"📊 Total content pieces created: {self.performance_metrics['content_created']}")
        print("=" * 60)
        
        return output

if __name__ == "__main__":
    # Initialize and run Content Agent
    content_agent = ContentGenerationAgent()
    results = content_agent.run_content_cycle()
