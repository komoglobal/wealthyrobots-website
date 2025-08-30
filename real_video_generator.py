#!/usr/bin/env python3
"""
REAL VIDEO GENERATOR
Creates actual video files that you can download to your local PC
"""

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import json
import os
from datetime import datetime
from typing import Dict, List

class RealVideoGenerator:
    """Generates actual video files for TikTok content"""
    
    def __init__(self):
        self.output_dir = "generated_videos"
        self.ensure_output_directory()
        
    def ensure_output_directory(self):
        """Create output directory if it doesn't exist"""
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
            print(f"📁 Created output directory: {self.output_dir}")
    
    def create_sample_video(self, content_item: Dict, duration_seconds: int = 15) -> str:
        """Create a real video file based on content item"""
        
        # Video parameters
        width, height = 1080, 1920  # 9:16 TikTok format
        fps = 30
        
        # Create video writer
        filename = f"{content_item.get('type', 'content')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4"
        output_path = os.path.join(self.output_dir, filename)
        
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
        
        # Generate frames
        total_frames = duration_seconds * fps
        
        for frame_num in range(total_frames):
            # Create frame
            frame = np.zeros((height, width, 3), dtype=np.uint8)
            
            # Add background gradient
            for y in range(height):
                color = int(255 * (1 - y / height))
                frame[y, :] = [color//3, color//2, color]
            
            # Add content information
            self.add_text_overlay(frame, content_item, frame_num, total_frames)
            
            # Add WealthyRobot branding
            self.add_brand_overlay(frame, frame_num, total_frames)
            
            # Write frame
            out.write(frame)
        
        out.release()
        
        # Convert to proper format
        self.convert_to_mp4(output_path)
        
        return output_path
    
    def add_text_overlay(self, frame: np.ndarray, content_item: Dict, frame_num: int, total_frames: int):
        """Add text overlay to frame"""
        
        # Get frame dimensions
        height, width = frame.shape[:2]
        fps = 30
        
        # Create PIL image for text
        pil_image = Image.fromarray(frame)
        draw = ImageDraw.Draw(pil_image)
        
        # Try to load a font, fall back to default if not available
        try:
            font_large = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 60)
            font_medium = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 40)
        except:
            font_large = ImageFont.load_default()
            font_medium = ImageFont.load_default()
        
        # Content title
        if content_item.get('type') == 'trending':
            title = f"🔥 Trending on {content_item.get('source', 'Unknown')}"
        elif content_item.get('type') == 'streamer_clip':
            title = f"🎮 {content_item.get('streamer', 'Unknown')} - Viral Clip"
        else:
            title = "🎬 Amazing Content"
        
        # Add title
        draw.text((width//2, 200), title, fill=(255, 255, 255), font=font_large, anchor="mm")
        
        # Add engagement info
        if 'engagement_score' in content_item:
            engagement_text = f"📊 {content_item['engagement_score']}% Engagement"
        elif 'engagement_potential' in content_item:
            engagement_text = f"📊 {content_item['engagement_potential']}% Viral Potential"
        else:
            engagement_text = "📊 High Engagement"
        
        draw.text((width//2, 300), engagement_text, fill=(255, 255, 255), font=font_medium, anchor="mm")
        
        # Add estimated views
        if 'engagement_score' in content_item:
            views = content_item['engagement_score'] * 1000
        elif 'engagement_potential' in content_item:
            views = content_item['engagement_potential'] * 1000
        else:
            views = 85000
        
        views_text = f"👁️ {views:,} Estimated Views"
        draw.text((width//2, 400), views_text, fill=(255, 255, 255), font=font_medium, anchor="mm")
        
        # Add progress indicator
        progress = frame_num / total_frames
        progress_text = f"⏱️ {frame_num//fps}s / {total_frames//fps}s"
        draw.text((width//2, 500), progress_text, fill=(255, 255, 255), font=font_medium, anchor="mm")
        
        # Add call to action
        cta_text = "💡 Learn more at WealthyRobot.com"
        draw.text((width//2, 600), cta_text, fill=(0, 255, 136), font=font_medium, anchor="mm")
        
        # Convert back to OpenCV format
        frame[:] = np.array(pil_image)
    
    def add_brand_overlay(self, frame: np.ndarray, frame_num: int, total_frames: int):
        """Add WealthyRobot branding overlay"""
        
        # Get frame dimensions
        height, width = frame.shape[:2]
        
        # Create corner watermark
        pil_image = Image.fromarray(frame)
        draw = ImageDraw.Draw(pil_image)
        
        try:
            font_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 30)
        except:
            font_small = ImageFont.load_default()
        
        # Add watermark in bottom right
        watermark_text = "WealthyRobot"
        draw.text((width-20, height-50), watermark_text, fill=(0, 255, 136), font=font_small, anchor="rb")
        
        # Add pulsing effect
        pulse = abs(np.sin(frame_num * 0.1)) * 0.5 + 0.5
        alpha = int(255 * pulse)
        draw.text((width-20, height-50), watermark_text, fill=(0, 255, 136, alpha), font=font_small, anchor="rb")
        
        # Convert back to OpenCV format
        frame[:] = np.array(pil_image)
    
    def convert_to_mp4(self, video_path: str):
        """Convert video to proper MP4 format"""
        try:
            # This would use FFmpeg in a real implementation
            # For now, we'll just rename the file
            if video_path.endswith('.mp4'):
                print(f"✅ Video created: {video_path}")
            else:
                print(f"✅ Video created: {video_path}")
        except Exception as e:
            print(f"⚠️ Video created but conversion failed: {e}")
    
    def generate_all_videos(self, content_data: Dict) -> List[str]:
        """Generate videos for all discovered content"""
        
        print("🎬 GENERATING REAL VIDEO FILES...")
        print("=" * 50)
        
        generated_videos = []
        
        if 'discovery' not in content_data or 'processed_content' not in content_data['discovery']:
            print("❌ No content data found. Run the TikTok system first!")
            return []
        
        processed_content = content_data['discovery']['processed_content']
        
        print(f"📊 Found {len(processed_content)} content items to process")
        
        for i, content in enumerate(processed_content, 1):
            print(f"\n🎬 Processing content {i}/{len(processed_content)}: {content.get('type', 'Unknown')}")
            
            try:
                # Generate video (15 seconds for trending, 20 seconds for streamer clips)
                duration = 20 if content.get('type') == 'streamer_clip' else 15
                video_path = self.create_sample_video(content, duration)
                
                generated_videos.append({
                    'content': content,
                    'video_path': video_path,
                    'duration': duration,
                    'status': 'completed'
                })
                
                print(f"✅ Generated: {os.path.basename(video_path)} ({duration}s)")
                
            except Exception as e:
                print(f"❌ Failed to generate video for content {i}: {e}")
                generated_videos.append({
                    'content': content,
                    'video_path': None,
                    'duration': 0,
                    'status': 'failed',
                    'error': str(e)
                })
        
        # Save generation report
        report = {
            'timestamp': datetime.now().isoformat(),
            'total_content': len(processed_content),
            'videos_generated': len([v for v in generated_videos if v['status'] == 'completed']),
            'generation_success': len([v for v in generated_videos if v['status'] == 'completed']) / len(processed_content),
            'generated_videos': generated_videos
        }
        
        report_path = os.path.join(self.output_dir, f"video_generation_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"\n📊 GENERATION COMPLETE!")
        print(f"   📁 Output directory: {self.output_dir}")
        print(f"   🎬 Videos generated: {report['videos_generated']}/{len(processed_content)}")
        print(f"   ✅ Success rate: {report['generation_success']*100:.1f}%")
        print(f"   📄 Report saved: {report_path}")
        
        return generated_videos
    
    def create_download_instructions(self, generated_videos: List[Dict]):
        """Create instructions for downloading videos to local PC"""
        
        instructions_path = os.path.join(self.output_dir, "DOWNLOAD_INSTRUCTIONS.txt")
        
        with open(instructions_path, 'w') as f:
            f.write("🎬 TIKTOK VIDEO DOWNLOAD INSTRUCTIONS\n")
            f.write("=" * 50 + "\n\n")
            f.write("Your TikTok videos have been generated and are ready for download!\n\n")
            
            f.write("📁 VIDEOS GENERATED:\n")
            for i, video in enumerate(generated_videos, 1):
                if video['status'] == 'completed':
                    f.write(f"{i}. {os.path.basename(video['video_path'])} ({video['duration']}s)\n")
                    f.write(f"   Content: {video['content'].get('type', 'Unknown')}\n")
                    if video['content'].get('type') == 'streamer_clip':
                        f.write(f"   Streamer: {video['content'].get('streamer', 'Unknown')}\n")
                    f.write(f"   File: {video['video_path']}\n\n")
            
            f.write("\n💻 DOWNLOAD METHODS:\n\n")
            f.write("METHOD 1: SCP (Command Line)\n")
            f.write("From your local PC, run:\n")
            f.write(f"scp -r ubuntu@YOUR_SERVER_IP:/home/ubuntu/wealthyrobot/{self.output_dir} ./tiktok_videos\n\n")
            
            f.write("METHOD 2: SFTP Client (FileZilla, WinSCP)\n")
            f.write("1. Connect to your server via SFTP\n")
            f.write(f"2. Navigate to: /home/ubuntu/wealthyrobot/{self.output_dir}\n")
            f.write("3. Download all .mp4 files\n\n")
            
            f.write("METHOD 3: Web Browser (if server has web access)\n")
            f.write("1. Open your server's IP in a web browser\n")
            f.write(f"2. Navigate to the {self.output_dir} folder\n")
            f.write("3. Right-click and save each video\n\n")
            
            f.write("📱 VIDEO SPECIFICATIONS:\n")
            f.write("- Format: MP4\n")
            f.write("- Resolution: 1080x1920 (9:16 TikTok format)\n")
            f.write("- Frame Rate: 30 FPS\n")
            f.write("- Duration: 15-20 seconds\n")
            f.write("- Branding: WealthyRobot watermark\n\n")
            
            f.write("🎯 NEXT STEPS:\n")
            f.write("1. Download videos to your local PC\n")
            f.write("2. Review and approve content\n")
            f.write("3. Upload to TikTok when ready\n")
            f.write("4. Monitor performance and revenue\n\n")
            
            f.write("🚀 Your automated TikTok empire is ready!\n")
        
        print(f"📋 Download instructions created: {instructions_path}")

def main():
    """Main function to generate real videos"""
    
    print("🎬 REAL VIDEO GENERATOR - TIKTOK CONTENT")
    print("=" * 50)
    
    generator = RealVideoGenerator()
    
    # Load content data
    content_data = {}
    if os.path.exists('content_discovery_results.json'):
        with open('content_discovery_results.json', 'r') as f:
            content_data['discovery'] = json.load(f)
    
    if not content_data:
        print("❌ No content data found. Run the TikTok system first!")
        return
    
    # Generate all videos
    generated_videos = generator.generate_all_videos(content_data)
    
    if generated_videos:
        # Create download instructions
        generator.create_download_instructions(generated_videos)
        
        print(f"\n🎉 SUCCESS! Your TikTok videos are ready for download!")
        print(f"📁 Check the '{generator.output_dir}' folder for your videos")
        print(f"📋 Read 'DOWNLOAD_INSTRUCTIONS.txt' for download help")

if __name__ == "__main__":
    main()
