#!/usr/bin/env python3
"""
Fix Article Pages Script
Adds proper CSS styling, navigation, and website template to all article pages
"""

import os
import glob
from datetime import datetime

def create_article_template(article_file, title, content):
    """Create properly formatted article page with navigation and styling"""
    
    # Extract article content from the basic HTML
    lines = content.split('\n')
    article_body = ""
    in_body = False
    
    for line in lines:
        if '<body>' in line:
            in_body = True
            continue
        elif '</body>' in line:
            break
        elif in_body:
            article_body += line + '\n'
    
    # Clean up the article body
    article_body = article_body.replace('<h1>', '').replace('</h1>', '')
    article_body = article_body.replace('<p>', '').replace('</p>', '')
    article_body = article_body.replace('<h2>', '<h2>').replace('</h2>', '</h2>')
    article_body = article_body.replace('<ol>', '<ol>').replace('</ol>', '</ol>')
    article_body = article_body.replace('<ul>', '<ul>').replace('</ul>', '</ul>')
    article_body = article_body.replace('<li>', '<li>').replace('</li>', '</li>')
    
    # Create the full article template
    template = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - WealthyRobot Empire</title>
    <meta name="description" content="Learn proven AI automation strategies to generate real revenue for your business. Comprehensive guide with actionable steps and case studies.">
    <meta name="keywords" content="AI automation revenue generation, business automation, artificial intelligence revenue, AI business strategies">
    
    <!-- Open Graph -->
    <meta property="og:title" content="{title}">
    <meta property="og:description" content="Learn proven AI automation strategies to generate real revenue for your business.">
    <meta property="og:type" content="article">
    <meta property="og:url" content="https://wealthyrobots.com/articles/{os.path.basename(article_file)}">
    
    <link rel="stylesheet" href="/assets/css/main.css">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
</head>
<body>
    <header class="main-header">
        <nav class="main-nav">
            <div class="nav-container">
                <div class="logo">
                    <a href="/">
                        <i class="fas fa-robot"></i>
                        <span>WealthyRobot Empire</span>
                    </a>
                </div>
                <ul class="nav-menu">
                    <li><a href="/" class="nav-link">Home</a></li>
                    <li><a href="/articles/" class="nav-link active">Articles</a></li>
                    <li><a href="/strategies/" class="nav-link">Strategies</a></li>
                    <li><a href="/tools/" class="nav-link">AI Tools</a></li>
                    <li><a href="/resources/" class="nav-link">Resources</a></li>
                    <li><a href="/about/" class="nav-link">About</a></li>
                    <li><a href="/contact/" class="nav-link">Contact</a></li>
                </ul>
                <div class="mobile-menu-toggle">
                    <span></span>
                    <span></span>
                    <span></span>
                </div>
            </div>
        </nav>
    </header>

    <main class="article-main">
        <div class="container">
            <article class="article-content">
                <header class="article-header">
                    <nav class="breadcrumb">
                        <a href="/">Home</a> / 
                        <a href="/articles/">Articles</a> / 
                        <span>{title}</span>
                    </nav>
                    <h1 class="article-title">{title}</h1>
                    <div class="article-meta">
                        <span class="article-date">August 6, 2025</span>
                        <span class="article-category">AI Automation</span>
                    </div>
                </header>

                <div class="article-body">
                    {article_body}
                </div>

                <footer class="article-footer">
                    <div class="article-tags">
                        <span class="tag">AI Automation</span>
                        <span class="tag">Revenue Generation</span>
                        <span class="tag">Business Strategy</span>
                    </div>
                    <div class="article-share">
                        <h4>Share this article:</h4>
                        <div class="share-buttons">
                            <a href="#" class="share-button twitter">
                                <i class="fab fa-twitter"></i> Twitter
                            </a>
                            <a href="#" class="share-button linkedin">
                                <i class="fab fa-linkedin"></i> LinkedIn
                            </a>
                            <a href="#" class="share-button facebook">
                                <i class="fab fa-facebook"></i> Facebook
                            </a>
                        </div>
                    </div>
                </footer>
            </article>

            <aside class="article-sidebar">
                <div class="sidebar-widget">
                    <h3>Related Articles</h3>
                    <ul class="related-articles">
                        <li><a href="/articles/article_passive_income_with_artificial_intelligence_tools_20250806_230124.html">Passive Income with Artificial Intelligence Tools</a></li>
                        <li><a href="/articles/article_business_automation_strategies_2025_20250806_230132.html">Business Automation Strategies 2025</a></li>
                        <li><a href="/articles/article_ai_tools_for_entrepreneurs_passive_income_20250806_230137.html">AI Tools for Entrepreneurs Passive Income</a></li>
                    </ul>
                </div>
                
                <div class="sidebar-widget">
                    <h3>Get Exclusive Content</h3>
                    <p>Join 1000+ entrepreneurs learning AI automation strategies</p>
                    <form class="sidebar-signup">
                        <input type="email" placeholder="Your email address" required>
                        <button type="submit" class="signup-button">
                            <span>Subscribe</span>
                            <i class="fas fa-arrow-right"></i>
                        </button>
                    </form>
                </div>
            </aside>
        </div>
    </main>

    <footer class="main-footer">
        <div class="container">
            <div class="footer-content">
                <div class="footer-section">
                    <div class="footer-logo">
                        <i class="fas fa-robot"></i>
                        <span>WealthyRobot Empire</span>
                    </div>
                    <p>AI automation strategies that actually make money</p>
                    <div class="social-links">
                        <a href="https://twitter.com/WealthyRobot" class="social-link">
                            <i class="fab fa-twitter"></i>
                        </a>
                        <a href="#" class="social-link">
                            <i class="fab fa-linkedin"></i>
                        </a>
                        <a href="#" class="social-link">
                            <i class="fab fa-youtube"></i>
                        </a>
                    </div>
                </div>
                <div class="footer-section">
                    <h3>Quick Links</h3>
                    <ul class="footer-links">
                        <li><a href="/articles/">Articles</a></li>
                        <li><a href="/strategies/">Strategies</a></li>
                        <li><a href="/tools/">AI Tools</a></li>
                        <li><a href="/resources/">Resources</a></li>
                    </ul>
                </div>
                <div class="footer-section">
                    <h3>Resources</h3>
                    <ul class="footer-links">
                        <li><a href="/about/">About Us</a></li>
                        <li><a href="/contact/">Contact</a></li>
                        <li><a href="/privacy/">Privacy Policy</a></li>
                        <li><a href="/terms/">Terms of Service</a></li>
                    </ul>
                </div>
                <div class="footer-section">
                    <h3>Connect</h3>
                    <ul class="footer-links">
                        <li><a href="https://twitter.com/WealthyRobot">Twitter</a></li>
                        <li><a href="/contact/">Contact</a></li>
                        <li><a href="/about/">About</a></li>
                        <li><a href="/newsletter/">Newsletter</a></li>
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
</html>'''
    
    return template

def fix_article_pages():
    """Fix all article pages by adding proper styling and navigation"""
    print("🔧 FIXING ARTICLE PAGES")
    print("=" * 40)
    
    articles_dir = "wealthyrobots_website/articles"
    article_files = glob.glob(f"{articles_dir}/article_*.html")
    
    fixed_count = 0
    
    for article_file in article_files:
        try:
            # Read the current article
            with open(article_file, 'r') as f:
                content = f.read()
            
            # Extract title from the file
            filename = os.path.basename(article_file)
            title = filename.replace('.html', '').replace('article_', '').replace('_', ' ').title()
            
            # Create the new template
            new_content = create_article_template(article_file, title, content)
            
            # Write the fixed article
            with open(article_file, 'w') as f:
                f.write(new_content)
            
            print(f"✅ Fixed: {filename}")
            fixed_count += 1
            
        except Exception as e:
            print(f"❌ Error fixing {article_file}: {e}")
    
    print(f"\n🎉 Fixed {fixed_count} article pages!")
    return fixed_count

if __name__ == "__main__":
    fix_article_pages()
