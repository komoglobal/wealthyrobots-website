#!/usr/bin/env python3
"""
Visual Integration Module - Automatically adds images to content
"""

import os
from datetime import datetime
from dotenv import load_dotenv

class VisualIntegrationManager:
    def __init__(self):
        load_dotenv()
        self.visual_enabled = True
        
    def enhance_content_with_visuals(self, content_data, content_type="thread"):
        """Add visual enhancements to generated content"""
        
        if not self.visual_enabled:
            return content_data
            
        print("🎨 VISUAL INTEGRATION: Enhancing content with images...")
        
        # Determine visual strategy based on content
        visual_strategy = self.determine_visual_strategy(content_data, content_type)
        
        # Generate images based on strategy
        images_created = self.generate_strategic_images(content_data, visual_strategy)
        
        # Package enhanced content
        enhanced_content = {
            **content_data,
            'visual_enhancements': {
                'images': images_created,
                'strategy': visual_strategy,
                'enhanced_at': datetime.now().isoformat()
            }
        }
        
        print(f"✅ Visual integration complete: {len(images_created)} images created")
        return enhanced_content
    
    def determine_visual_strategy(self, content_data, content_type):
        """Determine what types of images to create"""
        
        content_text = str(content_data).lower()
        strategy = {
            'thread_opener': True,  # Always create opener image
            'stats_infographic': False,
            'quote_card': False
        }
        
        # Analyze content for visual opportunities
        if any(word in content_text for word in ['stats', 'data', 'percent', 'growth']):
            strategy['stats_infographic'] = True
            
        if any(word in content_text for word in ['quote', 'says', 'advice', 'tip']):
            strategy['quote_card'] = True
            
        return strategy
    
    def generate_strategic_images(self, content_data, strategy):
        """Generate images based on strategy"""
        images_created = []
        
        try:
            # Import the AI image generator
            from ai_image_generator_agent import AIImageGeneratorAgent
            generator = AIImageGeneratorAgent()
            
            # Extract content for image generation
            if isinstance(content_data, dict):
                content_text = content_data.get('topic', 'AI Business Content')
            else:
                content_text = str(content_data)[:200]  # Limit length
            
            # Generate thread opener (always)
            if strategy['thread_opener']:
                opener_img = generator.create_simple_graphic(
                    "AI BUSINESS", 
                    "Thread Enhancement"
                )
                if opener_img:
                    images_created.append({
                        'type': 'thread_opener',
                        'filename': opener_img,
                        'usage': 'Attach to first tweet'
                    })
            
            # Generate stats infographic if relevant
            if strategy['stats_infographic']:
                stats = {
                    'main_stat': 'AI Growth',
                    'subtitle': 'Business Transformation',
                    'Automation': '85% Efficiency',
                    'Revenue': 'Up 40%',
                    'Time Saved': '20+ hrs/week'
                }
                stats_img = generator.create_stats_infographic(stats)
                if stats_img:
                    images_created.append({
                        'type': 'stats_infographic',
                        'filename': stats_img,
                        'usage': 'Attach to data tweet'
                    })
            
        except Exception as e:
            print(f"⚠️ Visual generation error: {e}")
        
        return images_created

if __name__ == "__main__":
    # Test the module
    manager = VisualIntegrationManager()
    test_content = {'topic': 'AI replacing jobs with solutions'}
    enhanced = manager.enhance_content_with_visuals(test_content)
    print("📊 Test completed successfully")
