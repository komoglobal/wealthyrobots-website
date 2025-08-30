#!/usr/bin/env python3
"""
AI Image Generator Agent - Creates actual visual content for tweets
Uses OpenAI DALL-E and/or programmatic image creation
"""

import openai
import os
import json
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO

class AIImageGeneratorAgent:
    def __init__(self):
        print("🎨 AI IMAGE GENERATOR AGENT - CREATING VISUALS")
        print("🖼️ Generating real images for your affiliate content")
        
        self.client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.images_created = 0
        
    def create_affiliate_product_image(self, product_name, benefits):
        """Create affiliate product showcase image"""
        try:
            prompt = f"""
            Create a professional, engaging social media image for "{product_name}".
            Style: Modern, clean, business-focused
            Include: Product benefits, professional layout, call-to-action feel
            Benefits to highlight: {benefits}
            Colors: Blue and orange (trust + engagement)
            Format: Square social media post
            """
            
            response = self.client.images.generate(
                model="dall-e-3",
                prompt=prompt,
                size="1024x1024",
                quality="standard",
                n=1
            )
            
            # Download and save image
            image_url = response.data[0].url
            img_response = requests.get(image_url)
            
            filename = f"affiliate_{product_name.lower().replace(' ', '_')}_{datetime.now().strftime('%H%M%S')}.png"
            
            with open(filename, 'wb') as f:
                f.write(img_response.content)
                
            print(f"✅ Created affiliate image: {filename}")
            self.images_created += 1
            
            return filename
            
        except Exception as e:
            print(f"❌ DALL-E error: {e}")
            return self.create_simple_graphic(product_name, benefits)
            
    def create_simple_graphic(self, title, subtitle):
        """Create simple graphics using PIL (no AI API needed)"""
        try:
            # Create 1080x1080 image
            img = Image.new('RGB', (1080, 1080), color='#1a1a1a')
            draw = ImageDraw.Draw(img)
            
            # Try to load a font (fallback to default if not available)
            try:
                title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 80)
                subtitle_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 50)
            except:
                title_font = ImageFont.load_default()
                subtitle_font = ImageFont.load_default()
            
            # Add title
            title_bbox = draw.textbbox((0, 0), title, font=title_font)
            title_width = title_bbox[2] - title_bbox[0]
            title_x = (1080 - title_width) // 2
            draw.text((title_x, 300), title, fill='#ff6b35', font=title_font)
            
            # Add subtitle
            subtitle_bbox = draw.textbbox((0, 0), subtitle, font=subtitle_font)
            subtitle_width = subtitle_bbox[2] - subtitle_bbox[0]
            subtitle_x = (1080 - subtitle_width) // 2
            draw.text((subtitle_x, 450), subtitle, fill='#ffffff', font=subtitle_font)
            
            # Add branding
            brand_text = "WealthyRobot"
            brand_bbox = draw.textbbox((0, 0), brand_text, font=subtitle_font)
            brand_width = brand_bbox[2] - brand_bbox[0]
            brand_x = (1080 - brand_width) // 2
            draw.text((brand_x, 800), brand_text, fill='#4a90e2', font=subtitle_font)
            
            filename = f"graphic_{title.lower().replace(' ', '_')}_{datetime.now().strftime('%H%M%S')}.png"
            img.save(filename)
            
            print(f"✅ Created simple graphic: {filename}")
            self.images_created += 1
            
            return filename
            
        except Exception as e:
            print(f"❌ Graphics creation error: {e}")
            return None
            
    def create_stats_infographic(self, stats):
        """Create statistics infographic"""
        try:
            img = Image.new('RGB', (1080, 1080), color='#f8f9fa')
            draw = ImageDraw.Draw(img)
            
            # Load fonts
            try:
                big_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 120)
                med_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 60)
                small_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 40)
            except:
                big_font = med_font = small_font = ImageFont.load_default()
            
            # Title
            draw.text((540, 100), "AI REVENUE STATS", fill='#1a1a1a', font=med_font, anchor="mm")
            
            # Main stat
            main_stat = stats.get('main_stat', '$330+')
            draw.text((540, 300), main_stat, fill='#ff6b35', font=big_font, anchor="mm")
            
            # Subtitle
            subtitle = stats.get('subtitle', 'Generated Revenue')
            draw.text((540, 420), subtitle, fill='#666666', font=med_font, anchor="mm")
            
            # Additional stats
            y_pos = 600
            for key, value in stats.items():
                if key not in ['main_stat', 'subtitle']:
                    draw.text((540, y_pos), f"{key}: {value}", fill='#333333', font=small_font, anchor="mm")
                    y_pos += 60
            
            # Branding
            draw.text((540, 950), "WealthyRobot.ai", fill='#4a90e2', font=small_font, anchor="mm")
            
            filename = f"stats_infographic_{datetime.now().strftime('%H%M%S')}.png"
            img.save(filename)
            
            print(f"✅ Created stats infographic: {filename}")
            self.images_created += 1
            
            return filename
            
        except Exception as e:
            print(f"❌ Infographic error: {e}")
            return None
            
    def create_quote_card(self, quote, author="WealthyRobot"):
        """Create quote card for social media"""
        try:
            img = Image.new('RGB', (1080, 1080), color='#4a90e2')
            draw = ImageDraw.Draw(img)
            
            try:
                quote_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 70)
                author_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 50)
            except:
                quote_font = author_font = ImageFont.load_default()
            
            # Quote marks
            draw.text((150, 200), '"', fill='#ffffff', font=quote_font)
            
            # Quote text (wrap if needed)
            words = quote.split()
            lines = []
            current_line = []
            
            for word in words:
                test_line = ' '.join(current_line + [word])
                bbox = draw.textbbox((0, 0), test_line, font=quote_font)
                if bbox[2] - bbox[0] < 800:  # 800px max width
                    current_line.append(word)
                else:
                    if current_line:
                        lines.append(' '.join(current_line))
                        current_line = [word]
                    else:
                        lines.append(word)
            
            if current_line:
                lines.append(' '.join(current_line))
            
            # Draw quote lines
            y_start = 350
            for i, line in enumerate(lines[:4]):  # Max 4 lines
                line_bbox = draw.textbbox((0, 0), line, font=quote_font)
                line_width = line_bbox[2] - line_bbox[0]
                x = (1080 - line_width) // 2
                draw.text((x, y_start + i * 80), line, fill='#ffffff', font=quote_font)
            
            # Author
            draw.text((540, 800), f"- {author}", fill='#ffffff', font=author_font, anchor="mm")
            
            filename = f"quote_card_{datetime.now().strftime('%H%M%S')}.png"
            img.save(filename)
            
            print(f"✅ Created quote card: {filename}")
            self.images_created += 1
            
            return filename
            
        except Exception as e:
            print(f"❌ Quote card error: {e}")
            return None
            
    def create_images_for_thread(self, thread_content):
        """Create a set of images for a Twitter thread"""
        print("🎨 Creating image set for Twitter thread...")
        
        images_created = []
        
        # 1. Create opener image
        opener_img = self.create_simple_graphic(
            "AI BUSINESS", 
            "Opportunities in 2025"
        )
        if opener_img:
            images_created.append(opener_img)
        
        # 2. Create stats infographic
        stats = {
            'main_stat': '$330+',
            'subtitle': 'AI Revenue Generated',
            'Automation Level': '98%',
            'Active Agents': '29',
            'Content Created': '16+ Threads'
        }
        
        stats_img = self.create_stats_infographic(stats)
        if stats_img:
            images_created.append(stats_img)
        
        # 3. Create quote card
        quote_img = self.create_quote_card(
            "AI isn't replacing humans, it's empowering entrepreneurs to build autonomous business empires."
        )
        if quote_img:
            images_created.append(quote_img)
        
        print(f"✅ Created {len(images_created)} images for thread")
        return images_created

if __name__ == "__main__":
    print("🚀 Starting AI Image Generator Agent...")
    
    generator = AIImageGeneratorAgent()
    
    # Create sample images
    images = generator.create_images_for_thread("sample thread")
    
    print(f"\n🎨 IMAGE GENERATION COMPLETE!")
    print(f"📸 Total images created: {generator.images_created}")
    print(f"📁 Files created: {images}")
    
    print("\n🚀 Next steps:")
    print("1. Use these images in your Twitter threads")
    print("2. Attach to tweets for higher engagement")
    print("3. Track performance vs text-only posts")
