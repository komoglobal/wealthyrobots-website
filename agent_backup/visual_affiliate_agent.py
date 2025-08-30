#!/usr/bin/env python3
"""
Visual Affiliate Agent - Combines AI-generated images with affiliate content
"""

import os
import glob
from datetime import datetime

class VisualAffiliateAgent:
    def __init__(self):
        print("🎨💰 VISUAL AFFILIATE AGENT - COMBINING IMAGES + AFFILIATE CONTENT")
        
    def create_complete_affiliate_package(self, affiliate_thread_file):
        """Create images that match specific affiliate content"""
        
        # Read affiliate thread
        with open(affiliate_thread_file, 'r') as f:
            content = f.read()
            
        # Extract key info from affiliate content
        if "The AI Advantage" in content:
            product_name = "The AI Advantage"
            benefits = "AI Business Strategies\nAutomated Revenue\nExpert Insights\nProven Results"
        elif "affiliate" in content.lower():
            product_name = "AI Business Tools"
            benefits = "Increase Productivity\nAutomate Tasks\nScale Revenue\nSave Time"
        else:
            product_name = "Business Success"
            benefits = "Proven Strategies\nReal Results\nExpert Guidance\nFast Growth"
            
        print(f"🎯 Creating package for: {product_name}")
        
        # Check for existing images
        existing_images = glob.glob("*.png")
        print(f"🖼️ Found {len(existing_images)} existing images")
        
        # Create posting instructions
        instructions = f"""
🎯 VISUAL AFFILIATE POSTING GUIDE
================================

THREAD: {affiliate_thread_file}
IMAGES: {existing_images[:3] if existing_images else ['No images available']}

POSTING ORDER:
1. Tweet 1 + {existing_images[0] if existing_images else 'Create opener image'}
2. Tweet 2-3 (text only with affiliate links)
3. Tweet 4-5 + {existing_images[1] if len(existing_images) > 1 else 'Create stats image'}  
4. Tweet 6-7 (text only)
5. Final tweet + {existing_images[2] if len(existing_images) > 2 else 'Create CTA image'}

AFFILIATE LINK PLACEMENT:
- Include Amazon link in tweets 2, 5, and final
- Always add transparency disclaimer
- Use engaging CTAs with images

MANUAL POSTING STRATEGY:
1. Go to Twitter.com
2. Post Tweet 1 with first image
3. Reply with Tweet 2 (include affiliate link)
4. Continue threading with strategic image placement

"""
        
        # Save instructions
        instruction_file = f"visual_affiliate_guide_{datetime.now().strftime('%H%M%S')}.txt"
        with open(instruction_file, 'w') as f:
            f.write(instructions)
            
        print(f"📋 Instructions saved: {instruction_file}")
        
        return {
            'images': existing_images[:3],
            'content_file': affiliate_thread_file,
            'instructions': instruction_file,
            'product': product_name
        }

if __name__ == "__main__":
    agent = VisualAffiliateAgent()
    
    # Find best affiliate thread
    affiliate_files = glob.glob("smart_viral_thread*.txt")
    
    if affiliate_files:
        # Use most recent affiliate thread
        latest_thread = max(affiliate_files, key=os.path.getctime)
        print(f"📝 Using thread: {latest_thread}")
        
        # Create complete package
        package = agent.create_complete_affiliate_package(latest_thread)
        
        print(f"\n🎨 VISUAL AFFILIATE PACKAGE COMPLETE!")
        print(f"🖼️ Images available: {len(package['images'])}")
        print(f"📝 Content: {package['content_file']}")
        print(f"📋 Guide: {package['instructions']}")
        
        # Show the content preview
        print(f"\n💰 AFFILIATE THREAD PREVIEW:")
        with open(package['content_file'], 'r') as f:
            preview = f.read()[:500]
            print(preview + "...")
            
    else:
        print("❌ No affiliate threads found")
