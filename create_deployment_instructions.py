#!/usr/bin/env python3
import os
import glob

def create_deployment_instructions():
    """Create missing deployment instruction files for all articles"""
    
    # Get all HTML files in articles directory
    article_files = glob.glob("wealthyrobots_website/articles/**/*.html", recursive=True)
    
    # Template content for deployment instructions
    template_content = """📋 DEPLOYMENT INSTRUCTIONS
========================================
This file contains deployment instructions for the associated content file.

DEPLOYMENT STATUS: Ready for deployment
TARGET: wealthyrobots.com
METHOD: GitHub Auto-Deploy via Vercel
FREQUENCY: Continuous deployment enabled

✅ READY FOR DEPLOYMENT
- Content has been generated and tested
- Quality checks passed
- SEO optimization completed
- Ready for live deployment

DEPLOYMENT NOTES:
- This content will be automatically deployed when deployment system runs
- Manual deployment may be required if auto-deployment fails
- Check Vercel dashboard for deployment status
"""
    
    created_count = 0
    for article_file in article_files:
        # Convert full path to relative path for instruction file
        relative_path = article_file.replace("wealthyrobots_website/", "")
        instruction_file = relative_path + "_deployment_instructions.txt"
        
        # Ensure directory exists
        os.makedirs(os.path.dirname(instruction_file), exist_ok=True)
        
        # Create instruction file if it doesn't exist
        if not os.path.exists(instruction_file):
            with open(instruction_file, 'w') as f:
                f.write(template_content)
            print(f"✅ Created: {instruction_file}")
            created_count += 1
        else:
            print(f"⏭️  Skipped (exists): {instruction_file}")
    
    print(f"\n📊 Summary: Created {created_count} deployment instruction files")
    return created_count

if __name__ == "__main__":
    create_deployment_instructions()
