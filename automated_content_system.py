#!/usr/bin/env python3
"""
EMPIRE_AGENT_INFO:
NAME: Automated Content System
PURPOSE: Continuously generates SEO-optimized articles and integrates them with the website
CATEGORY: Content & SEO Management
STATUS: Active
FREQUENCY: Continuous
"""

import os
import json
import time
import shutil
import re
from datetime import datetime, timedelta
import glob
import subprocess

class AutomatedContentSystem:
    def __init__(self):
        self.website_dir = "wealthyrobots_website"
        self.articles_dir = os.path.join(self.website_dir, "articles")
        self.content_schedule = []
        self.seo_keywords = []
        self.article_templates = []
        
        # Load SEO keywords
        self.load_seo_keywords()
        
        # Load article templates
        self.load_article_templates()
    
    def load_seo_keywords(self):
        """Load SEO keywords for content generation"""
        print("🔍 LOADING SEO KEYWORDS")
        print("=" * 30)
        
        # Long-tail keywords for AI automation
        self.seo_keywords = [
            "AI automation revenue generation",
            "passive income with artificial intelligence",
            "business automation strategies 2025",
            "AI tools for entrepreneurs",
            "automated revenue systems",
            "AI marketing automation",
            "artificial intelligence business opportunities",
            "AI automation for small business",
            "automated income streams",
            "AI-powered business growth",
            "artificial intelligence revenue optimization",
            "automation tools for entrepreneurs",
            "AI business automation strategies",
            "passive income automation",
            "artificial intelligence marketing tools",
            "automated business processes",
            "AI revenue generation techniques",
            "business automation with AI",
            "artificial intelligence for revenue growth",
            "automated income generation strategies",
            "AI customer service automation",
            "artificial intelligence for lead generation",
            "automated email marketing with AI",
            "AI-powered content creation",
            "artificial intelligence for sales automation",
            "automated social media management",
            "AI tools for business growth",
            "artificial intelligence for customer support",
            "automated data analysis with AI",
            "AI-powered business intelligence"
        ]
        
        print(f"✅ Loaded {len(self.seo_keywords)} SEO keywords")
        return self.seo_keywords
    
    def load_article_templates(self):
        """Load article templates for different content types"""
        print("📝 LOADING ARTICLE TEMPLATES")
        print("=" * 35)
        
        self.article_templates = {
            "how_to": {
                "title_pattern": "How to {keyword} in 2025: Complete Guide",
                "structure": [
                    "Introduction and problem statement",
                    "Why this matters for entrepreneurs",
                    "Step-by-step implementation",
                    "Tools and resources needed",
                    "Common mistakes to avoid",
                    "Success metrics and tracking",
                    "Conclusion and next steps"
                ]
            },
            "list_article": {
                "title_pattern": "{number} {keyword} That Will Transform Your Business",
                "structure": [
                    "Introduction to the topic",
                    "Why this list matters",
                    "Detailed explanation of each item",
                    "Implementation tips",
                    "ROI and benefits",
                    "Conclusion and call-to-action"
                ]
            },
            "case_study": {
                "title_pattern": "How {company} Used {keyword} to {result}",
                "structure": [
                    "Background and challenge",
                    "Solution implemented",
                    "Implementation process",
                    "Results and metrics",
                    "Lessons learned",
                    "Replicable strategies"
                ]
            },
            "comparison": {
                "title_pattern": "{keyword} vs {alternative}: Which is Better for Your Business?",
                "structure": [
                    "Introduction to both options",
                    "Detailed comparison criteria",
                    "Pros and cons analysis",
                    "Use case recommendations",
                    "Cost-benefit analysis",
                    "Final recommendation"
                ]
            }
        }
        
        print(f"✅ Loaded {len(self.article_templates)} article templates")
        return self.article_templates
    
    def generate_content_schedule(self):
        """Generate content schedule for the next 30 days"""
        print("📅 GENERATING CONTENT SCHEDULE")
        print("=" * 35)
        
        # Create 30 days of content
        for day in range(30):
            schedule_date = datetime.now() + timedelta(days=day)
            
            # Determine content type based on day
            if day % 7 == 0:  # Weekly
                content_type = "how_to"
                keyword = self.seo_keywords[day % len(self.seo_keywords)]
            elif day % 7 == 3:  # Mid-week
                content_type = "list_article"
                keyword = self.seo_keywords[(day + 5) % len(self.seo_keywords)]
            elif day % 7 == 5:  # Weekend
                content_type = "case_study"
                keyword = self.seo_keywords[(day + 10) % len(self.seo_keywords)]
            else:
                content_type = "comparison"
                keyword = self.seo_keywords[(day + 15) % len(self.seo_keywords)]
            
            self.content_schedule.append({
                "date": schedule_date.strftime("%Y-%m-%d"),
                "content_type": content_type,
                "keyword": keyword,
                "status": "pending",
                "priority": "high" if day < 7 else "medium"
            })
        
        print(f"✅ Generated {len(self.content_schedule)} content items")
        return self.content_schedule
    
    def create_article_with_optimized_agent(self, keyword, content_type):
        """Create article using the optimized content agent"""
        print(f"✍️ CREATING ARTICLE: {keyword}")
        print("=" * 40)
        
        try:
            # Use the optimized content agent
            from optimized_content_agent import OptimizedContentAgent
            
            content_agent = OptimizedContentAgent()
            
            # Generate blog content
            blog_content = content_agent.generate_content_piece(keyword, "blog")
            
            if isinstance(blog_content, dict) and blog_content.get("content"):
                # Create article file
                article_filename = f"article_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
                article_path = os.path.join(self.articles_dir, article_filename)
                
                # Create article with proper structure
                article_html = self.create_article_html(keyword, blog_content["content"])
                
                with open(article_path, 'w') as f:
                    f.write(article_html)
                
                print(f"✅ Article created: {article_filename}")
                return article_filename
            else:
                print(f"❌ Failed to generate content for: {keyword}")
                return None
                
        except Exception as e:
            print(f"❌ Error creating article: {e}")
            return None
    
    def create_article_html(self, title, content):
        """Create article HTML with proper structure"""
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} | WealthyRobot Empire</title>
    <meta name="description" content="Learn proven AI automation strategies for revenue generation. Professional insights from the WealthyRobot Empire.">
    <meta name="keywords" content="AI automation, revenue generation, artificial intelligence, business automation, {title.lower()}">
    
    <!-- Open Graph -->
    <meta property="og:title" content="{title} | WealthyRobot Empire">
    <meta property="og:description" content="Learn proven AI automation strategies for revenue generation">
    <meta property="og:type" content="article">
    <meta property="og:url" content="https://wealthyrobots.com/articles/{title.lower().replace(' ', '-')}">
    
    <!-- Twitter Card -->
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{title}">
    <meta name="twitter:description" content="Learn proven AI automation strategies for revenue generation">
    
    <link rel="stylesheet" href="/assets/css/main.css">
    <link rel="canonical" href="https://wealthyrobots.com/articles/{title.lower().replace(' ', '-')}">
</head>
<body>
    <header class="main-header">
        <nav class="main-nav">
            <div class="nav-container">
                <div class="logo">
                    <a href="/">🤖 WealthyRobot Empire</a>
                </div>
                <ul class="nav-menu">
                    <li><a href="/">Home</a></li>
                    <li><a href="/articles/">Articles</a></li>
                    <li><a href="/strategies/">Strategies</a></li>
                    <li><a href="/tools/">AI Tools</a></li>
                    <li><a href="/resources/">Resources</a></li>
                    <li><a href="/about/">About</a></li>
                    <li><a href="/contact/">Contact</a></li>
                </ul>
            </div>
        </nav>
    </header>

    <main class="article-main">
        <article class="article-content">
            <div class="container">
                <header class="article-header">
                    <h1>{title}</h1>
                    <div class="article-meta">
                        <span class="publish-date">Published: {datetime.now().strftime('%B %d, %Y')}</span>
                        <span class="read-time">8 min read</span>
                        <span class="author">By WealthyRobot Empire</span>
                    </div>
                </header>
                
                <div class="article-body">
                    {content}
                </div>
                
                <footer class="article-footer">
                    <div class="article-cta">
                        <h3>Ready to Build Your AI Revenue Empire?</h3>
                        <p>Join 1000+ entrepreneurs learning AI automation strategies</p>
                        <form class="article-signup" action="/subscribe" method="POST">
                            <input type="email" placeholder="Your email address" required>
                            <button type="submit">Subscribe Now</button>
                        </form>
                    </div>
                    
                    <div class="related-articles">
                        <h4>Related Articles</h4>
                        <ul>
                            <li><a href="/articles/ai-automation-strategies">AI Automation Strategies That Work</a></li>
                            <li><a href="/articles/passive-income-automation">Building Passive Income with AI</a></li>
                            <li><a href="/articles/business-automation-tools">Top AI Tools for Business Growth</a></li>
                        </ul>
                    </div>
                </footer>
            </div>
        </article>
    </main>

    <footer class="main-footer">
        <div class="container">
            <div class="footer-content">
                <div class="footer-section">
                    <h3>WealthyRobot Empire</h3>
                    <p>AI Automation Strategies That Actually Make Money</p>
                </div>
                <div class="footer-section">
                    <h4>Quick Links</h4>
                    <ul>
                        <li><a href="/articles/">Articles</a></li>
                        <li><a href="/strategies/">Strategies</a></li>
                        <li><a href="/tools/">AI Tools</a></li>
                        <li><a href="/resources/">Resources</a></li>
                    </ul>
                </div>
                <div class="footer-section">
                    <h4>Connect</h4>
                    <ul>
                        <li><a href="https://twitter.com/WealthyRobot">Twitter</a></li>
                        <li><a href="/contact/">Contact</a></li>
                        <li><a href="/about/">About</a></li>
                    </ul>
                </div>
            </div>
            <div class="footer-bottom">
                <p>&copy; 2025 WealthyRobot Empire. All rights reserved.</p>
            </div>
        </div>
    </footer>

    <script src="/assets/js/main.js"></script>
</body>
</html>"""
    
    def update_website_index(self):
        """Update website index with latest articles"""
        print("📝 UPDATING WEBSITE INDEX")
        print("=" * 35)
        
        # Find all articles
        article_files = glob.glob(os.path.join(self.articles_dir, "*.html"))
        
        # Create articles index
        articles_index = []
        for article_file in sorted(article_files, key=os.path.getmtime, reverse=True)[:10]:  # Latest 10
            try:
                with open(article_file, 'r') as f:
                    content = f.read()
                
                # Extract title
                title_match = re.search(r'<title>(.*?)</title>', content)
                title = title_match.group(1) if title_match else "AI Automation Article"
                
                # Extract description
                desc_match = re.search(r'<meta name="description" content="(.*?)"', content)
                description = desc_match.group(1) if desc_match else "Learn proven AI automation strategies"
                
                articles_index.append({
                    "title": title,
                    "description": description,
                    "filename": os.path.basename(article_file),
                    "date": datetime.fromtimestamp(os.path.getmtime(article_file)).strftime("%Y-%m-%d")
                })
                
            except Exception as e:
                print(f"❌ Error processing {article_file}: {e}")
        
        # Save articles index
        index_path = os.path.join(self.website_dir, "articles_index.json")
        with open(index_path, 'w') as f:
            json.dump(articles_index, f, indent=2)
        
        print(f"✅ Updated articles index: {len(articles_index)} articles")
        return articles_index
    
    def run_content_generation_cycle(self):
        """Run complete content generation cycle"""
        print("🚀 AUTOMATED CONTENT GENERATION CYCLE")
        print("=" * 50)
        
        # Step 1: Generate content schedule
        self.generate_content_schedule()
        
        # Step 2: Create articles for next 7 days
        articles_created = 0
        for item in self.content_schedule[:7]:  # Next 7 days
            if item["status"] == "pending":
                print(f"\n📅 Creating content for {item['date']}: {item['keyword']}")
                
                article_file = self.create_article_with_optimized_agent(
                    item["keyword"], 
                    item["content_type"]
                )
                
                if article_file:
                    item["status"] = "completed"
                    item["article_file"] = article_file
                    articles_created += 1
                else:
                    item["status"] = "failed"
        
        # Step 3: Update website index
        self.update_website_index()
        
        # Step 4: Save content schedule
        schedule_path = os.path.join(self.website_dir, "content_schedule.json")
        with open(schedule_path, 'w') as f:
            json.dump(self.content_schedule, f, indent=2)
        
        print(f"\n✅ Content generation cycle complete!")
        print(f"📝 Articles created: {articles_created}")
        print(f"📅 Schedule updated: {len(self.content_schedule)} items")
        
        return {
            "articles_created": articles_created,
            "schedule_items": len(self.content_schedule),
            "cycle_complete": True
        }
    
    def run_continuous_content_generation(self):
        """Run continuous content generation"""
        print("🔄 STARTING CONTINUOUS CONTENT GENERATION")
        print("=" * 50)
        
        while True:
            try:
                # Run content generation cycle
                result = self.run_content_generation_cycle()
                
                print(f"\n⏰ Next content generation in 24 hours...")
                time.sleep(86400)  # 24 hours
                
            except KeyboardInterrupt:
                print("\n🛑 Content generation stopped by user")
                break
            except Exception as e:
                print(f"❌ Content generation error: {e}")
                time.sleep(3600)  # Wait 1 hour on error

def main():
    import re
    
    # Initialize automated content system
    content_system = AutomatedContentSystem()
    
    # Run content generation cycle
    result = content_system.run_content_generation_cycle()
    
    print(f"\n🎉 Content generation successful!")
    print(f"📝 Articles created: {result['articles_created']}")
    print(f"📅 Schedule items: {result['schedule_items']}")

if __name__ == "__main__":
    main()
