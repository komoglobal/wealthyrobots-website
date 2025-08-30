#!/usr/bin/env python3
"""
CONTENT REVIEW SYSTEM
Review the TikTok clips and content that the automated system is processing
"""

import json
import os
from datetime import datetime
from typing import Dict, List

class ContentReviewSystem:
    """System to review TikTok content and clips"""
    
    def __init__(self):
        self.content_library = []
        self.review_history = []
        
    def load_recent_content(self) -> Dict:
        """Load the most recent content from the system"""
        
        content_data = {}
        
        # Load discovery results
        if os.path.exists('content_discovery_results.json'):
            with open('content_discovery_results.json', 'r') as f:
                content_data['discovery'] = json.load(f)
        
        # Load editing results
        if os.path.exists('editing_cycle_results.json'):
            with open('editing_cycle_results.json', 'r') as f:
                content_data['editing'] = json.load(f)
        
        # Load automation cycle results
        cycle_files = [f for f in os.listdir('.') if f.startswith('automation_cycle_')]
        if cycle_files:
            latest_cycle = max(cycle_files)
            with open(latest_cycle, 'r') as f:
                content_data['cycle'] = json.load(f)
        
        return content_data
    
    def generate_content_preview(self, content_item: Dict) -> Dict:
        """Generate a preview of what the content would look like"""
        
        if content_item.get('type') == 'trending':
            preview = {
                "content_type": "Trending Content",
                "source": content_item.get('source', 'Unknown'),
                "title": content_item.get('title', 'No title'),
                "engagement_score": content_item.get('engagement_score', 0),
                "preview_description": f"Trending content from {content_item.get('source', 'Unknown')} with {content_item.get('engagement_score', 0)}% engagement",
                "estimated_views": f"{content_item.get('engagement_score', 0) * 1000:,}",
                "monetization_potential": content_item.get('monetization_potential', 'Unknown'),
                "processing_status": content_item.get('processing_status', 'Unknown')
            }
        elif content_item.get('type') == 'streamer_clip':
            preview = {
                "content_type": "Streamer Clip",
                "streamer": content_item.get('streamer', 'Unknown'),
                "clip_url": content_item.get('clip_url', 'No URL'),
                "engagement_potential": content_item.get('engagement_potential', 0),
                "preview_description": f"High-engagement clip from {content_item.get('streamer', 'Unknown')} with {content_item.get('engagement_potential', 0)}% viral potential",
                "estimated_views": f"{content_item.get('engagement_potential', 0) * 1000:,}",
                "monetization_ready": content_item.get('monetization_ready', False),
                "copyright_status": content_item.get('copyright_status', 'Unknown'),
                "processing_status": content_item.get('processing_status', 'Unknown')
            }
        else:
            preview = {
                "content_type": "Unknown Content",
                "preview_description": "Content type not recognized",
                "processing_status": "Error"
            }
        
        return preview
    
    def show_content_library(self) -> None:
        """Display all discovered and processed content"""
        
        print("🎬 TIKTOK CONTENT LIBRARY - REVIEW SYSTEM")
        print("=" * 60)
        
        content_data = self.load_recent_content()
        
        if not content_data:
            print("❌ No content data found. Run the TikTok system first!")
            return
        
        # Show discovery results
        if 'discovery' in content_data:
            discovery = content_data['discovery']
            print(f"\n🔍 CONTENT DISCOVERY RESULTS:")
            print(f"   📊 Total opportunities found: {discovery.get('total_opportunities', 0)}")
            print(f"   📈 Content processed: {discovery.get('content_processed', 0)}")
            print(f"   ✅ Discovery success: {discovery.get('discovery_success', False)}")
            
            # Show processed content
            if 'processed_content' in discovery:
                print(f"\n📋 PROCESSED CONTENT ITEMS:")
                for i, content in enumerate(discovery['processed_content'], 1):
                    preview = self.generate_content_preview(content)
                    
                    print(f"\n   {i}. {preview['content_type']}")
                    print(f"      📝 {preview['preview_description']}")
                    print(f"      👁️  Estimated views: {preview['estimated_views']}")
                    print(f"      💰 Monetization: {preview.get('monetization_potential', preview.get('monetization_ready', 'Unknown'))}")
                    print(f"      🔄 Status: {preview['processing_status']}")
                    
                    if content.get('type') == 'streamer_clip':
                        print(f"      🎮 Streamer: {preview['streamer']}")
                        print(f"      🔗 Clip URL: {preview['clip_url']}")
                        print(f"      ⚖️  Copyright: {preview['copyright_status']}")
        
        # Show editing results
        if 'editing' in content_data:
            editing = content_data['editing']
            print(f"\n✂️ EDITING RESULTS:")
            print(f"   📊 Content processed: {editing.get('content_processed', 0)}")
            print(f"   ✅ Success rate: {editing.get('editing_success_rate', 0)}%")
            print(f"   📱 Ready for posting: {editing.get('ready_for_posting', 0)}")
            print(f"   📝 Details: {editing.get('processing_details', 'No details')}")
        
        # Show cycle results
        if 'cycle' in content_data:
            cycle = content_data['cycle']
            print(f"\n🔄 AUTOMATION CYCLE RESULTS:")
            print(f"   🔢 Cycle number: {cycle.get('cycle_number', 'Unknown')}")
            print(f"   ⏱️  Duration: {cycle.get('cycle_duration_seconds', 0):.2f} seconds")
            print(f"   ✅ Success: {cycle.get('cycle_success', False)}")
    
    def review_specific_content(self, content_index: int) -> None:
        """Review a specific piece of content in detail"""
        
        content_data = self.load_recent_content()
        
        if 'discovery' not in content_data or 'processed_content' not in content_data['discovery']:
            print("❌ No processed content found to review.")
            return
        
        processed_content = content_data['discovery']['processed_content']
        
        if content_index < 1 or content_index > len(processed_content):
            print(f"❌ Invalid content index. Choose 1-{len(processed_content)}")
            return
        
        content = processed_content[content_index - 1]
        preview = self.generate_content_preview(content)
        
        print(f"\n🎬 DETAILED CONTENT REVIEW - ITEM {content_index}")
        print("=" * 60)
        
        print(f"📋 CONTENT TYPE: {preview['content_type']}")
        print(f"📝 DESCRIPTION: {preview['preview_description']}")
        print(f"👁️  ESTIMATED VIEWS: {preview['estimated_views']}")
        print(f"💰 MONETIZATION: {preview.get('monetization_potential', preview.get('monetization_ready', 'Unknown'))}")
        print(f"🔄 PROCESSING STATUS: {preview['processing_status']}")
        
        if content.get('type') == 'streamer_clip':
            print(f"\n🎮 STREAMER DETAILS:")
            print(f"   👤 Name: {preview['streamer']}")
            print(f"   🔗 Clip URL: {preview['clip_url']}")
            print(f"   ⚖️  Copyright Status: {preview['copyright_status']}")
            print(f"   🎯 Engagement Potential: {preview['engagement_potential']}%")
        
        elif content.get('type') == 'trending':
            print(f"\n📈 TRENDING DETAILS:")
            print(f"   🌐 Source: {preview['source']}")
            print(f"   📊 Engagement Score: {preview['engagement_score']}%")
            print(f"   🎯 Viral Potential: {'High' if preview['engagement_score'] >= 85 else 'Medium'}")
        
        # Show what the final TikTok would look like
        print(f"\n📱 FINAL TIKTOK PREVIEW:")
        print(f"   🎬 Format: 9:16 vertical video")
        print(f"   ⏱️  Duration: 15-60 seconds")
        print(f"   🏷️  Brand: WealthyRobot watermark")
        print(f"   📝 Caption: '🔥 {preview['preview_description'][:50]}... #viral #trending #wealthyrobot'")
        print(f"   🎯 Hashtags: #viral #trending #fyp #wealthyrobot")
        
        # Show revenue potential
        estimated_views = int(preview['estimated_views'].replace(',', ''))
        revenue_potential = self.calculate_revenue_potential(estimated_views)
        
        print(f"\n💰 REVENUE POTENTIAL:")
        print(f"   💵 Creator Fund: ${revenue_potential['creator_fund']:.2f}")
        print(f"   🛍️  Shop Commissions: ${revenue_potential['shop_commissions']:.2f}")
        print(f"   📈 Total Potential: ${revenue_potential['total']:.2f}")
    
    def calculate_revenue_potential(self, views: int) -> Dict:
        """Calculate potential revenue from views"""
        
        # Creator Fund: $0.01-0.02 per view
        creator_fund = views * 0.015  # Average rate
        
        # Shop Commissions: 2% conversion, $25 average order, 10% commission
        conversion_rate = 0.02
        avg_order = 25.0
        commission_rate = 0.10
        shop_commissions = views * conversion_rate * avg_order * commission_rate
        
        total = creator_fund + shop_commissions
        
        return {
            'creator_fund': creator_fund,
            'shop_commissions': shop_commissions,
            'total': total
        }
    
    def export_content_report(self) -> None:
        """Export a detailed content report"""
        
        content_data = self.load_recent_content()
        
        if not content_data:
            print("❌ No content data to export.")
            return
        
        report = {
            "timestamp": datetime.now().isoformat(),
            "content_summary": {
                "total_discovered": content_data.get('discovery', {}).get('total_opportunities', 0),
                "total_processed": content_data.get('discovery', {}).get('content_processed', 0),
                "editing_success": content_data.get('editing', {}).get('editing_success_rate', 0),
                "ready_for_posting": content_data.get('editing', {}).get('ready_for_posting', 0)
            },
            "content_details": [],
            "revenue_projections": {
                "total_views": 0,
                "total_revenue_potential": 0.0
            }
        }
        
        # Add content details
        if 'discovery' in content_data and 'processed_content' in content_data['discovery']:
            for content in content_data['discovery']['processed_content']:
                preview = self.generate_content_preview(content)
                estimated_views = int(preview['estimated_views'].replace(',', ''))
                revenue = self.calculate_revenue_potential(estimated_views)
                
                content_detail = {
                    "content_type": preview['content_type'],
                    "description": preview['preview_description'],
                    "estimated_views": estimated_views,
                    "revenue_potential": revenue,
                    "processing_status": preview['processing_status']
                }
                
                report['content_details'].append(content_detail)
                report['revenue_projections']['total_views'] += estimated_views
                report['revenue_projections']['total_revenue_potential'] += revenue['total']
        
        # Save report
        filename = f"content_review_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"✅ Content report exported to: {filename}")
        print(f"📊 Total views projected: {report['revenue_projections']['total_views']:,}")
        print(f"💰 Total revenue potential: ${report['revenue_projections']['total_revenue_potential']:.2f}")

def main():
    """Main function to run the content review system"""
    
    print("🎬 TIKTOK CONTENT REVIEW SYSTEM")
    print("=" * 40)
    
    reviewer = ContentReviewSystem()
    
    while True:
        print("\n📋 REVIEW OPTIONS:")
        print("1. 📊 Show content library")
        print("2. 🔍 Review specific content")
        print("3. 📄 Export content report")
        print("4. 🚪 Exit")
        
        choice = input("\n🎯 Choose an option (1-4): ").strip()
        
        if choice == '1':
            reviewer.show_content_library()
        
        elif choice == '2':
            content_data = reviewer.load_recent_content()
            if 'discovery' in content_data and 'processed_content' in content_data['discovery']:
                count = len(content_data['discovery']['processed_content'])
                print(f"\n📋 Available content: 1-{count}")
                try:
                    index = int(input("🎬 Enter content number to review: "))
                    reviewer.review_specific_content(index)
                except ValueError:
                    print("❌ Please enter a valid number.")
            else:
                print("❌ No content available to review.")
        
        elif choice == '3':
            reviewer.export_content_report()
        
        elif choice == '4':
            print("👋 Goodbye! Your TikTok content is ready for review.")
            break
        
        else:
            print("❌ Invalid choice. Please select 1-4.")

if __name__ == "__main__":
    main()


