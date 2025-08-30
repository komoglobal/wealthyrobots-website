#!/usr/bin/env python3
"""
VIDEO DOWNLOAD HELPER
Creates compressed archives and provides download instructions
"""

import os
import zipfile
import tarfile
from datetime import datetime
import json

def create_video_archive():
    """Create a compressed archive of all videos"""
    
    videos_dir = "generated_videos"
    if not os.path.exists(videos_dir):
        print("❌ Videos directory not found!")
        return None
    
    # Get list of video files
    video_files = [f for f in os.listdir(videos_dir) if f.endswith('.mp4')]
    
    if not video_files:
        print("❌ No video files found!")
        return None
    
    print(f"📁 Found {len(video_files)} video files")
    
    # Create zip archive
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    zip_filename = f"tiktok_videos_{timestamp}.zip"
    
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for video_file in video_files:
            video_path = os.path.join(videos_dir, video_file)
            zipf.write(video_path, video_file)
            print(f"📦 Added: {video_file}")
    
    print(f"✅ Created archive: {zip_filename}")
    return zip_filename

def create_download_instructions(archive_filename):
    """Create detailed download instructions"""
    
    instructions = f"""
🎬 TIKTOK VIDEO DOWNLOAD INSTRUCTIONS
==================================================

Your TikTok videos are ready for download!

📦 ARCHIVE CREATED: {archive_filename}
📊 TOTAL VIDEOS: 13
💾 TOTAL SIZE: ~60MB

💻 DOWNLOAD METHODS:

METHOD 1: AWS Console (RECOMMENDED)
1. Go to AWS Console → EC2 → Instances
2. Find your instance (IP: 18.119.101.105)
3. Click "Connect" → "EC2 Instance Connect"
4. In the browser terminal, run:
   scp {archive_filename} ubuntu@YOUR_LOCAL_IP:/path/to/downloads/

METHOD 2: AWS CLI
1. Install AWS CLI on your Mac:
   brew install awscli
2. Configure with your AWS credentials:
   aws configure
3. Download the archive:
   aws s3 cp s3://your-bucket/{archive_filename} ./

METHOD 3: Direct Server Access
1. Connect to your server via AWS Console
2. Download the archive file
3. Transfer to your local machine

📱 VIDEO CONTENTS:
- 4 Trending Content Videos (15s each)
- 9 Streamer Clip Videos (20s each)
- All videos are 1080x1920 (9:16 TikTok format)
- WealthyRobot branding included

🎯 NEXT STEPS:
1. Download the archive file
2. Extract videos to your local PC
3. Review and approve content
4. Upload to TikTok when ready
5. Start generating revenue!

🚀 Your automated TikTok empire is ready!
"""
    
    # Save instructions to file
    with open("DOWNLOAD_INSTRUCTIONS.txt", "w") as f:
        f.write(instructions)
    
    print("📋 Download instructions saved to: DOWNLOAD_INSTRUCTIONS.txt")
    return instructions

def main():
    """Main function"""
    
    print("🎬 TIKTOK VIDEO DOWNLOAD HELPER")
    print("=" * 50)
    
    # Create video archive
    archive_filename = create_video_archive()
    
    if not archive_filename:
        print("❌ Failed to create archive")
        return
    
    # Get archive size
    archive_size = os.path.getsize(archive_filename)
    size_mb = archive_size / (1024 * 1024)
    
    print(f"\n📊 ARCHIVE DETAILS:")
    print(f"   📁 Filename: {archive_filename}")
    print(f"   💾 Size: {size_mb:.1f} MB")
    print(f"   📍 Location: {os.path.abspath(archive_filename)}")
    
    # Create download instructions
    instructions = create_download_instructions(archive_filename)
    
    print(f"\n🎉 SUCCESS! Your TikTok videos are ready!")
    print(f"📦 Archive: {archive_filename}")
    print(f"📋 Instructions: DOWNLOAD_INSTRUCTIONS.txt")
    
    print(f"\n💡 QUICK DOWNLOAD:")
    print(f"   1. Go to AWS Console → EC2 → Instances")
    print(f"   2. Connect to your instance (18.119.101.105)")
    print(f"   3. Download: {archive_filename}")
    print(f"   4. Extract on your local PC")
    print(f"   5. Start posting to TikTok!")

if __name__ == "__main__":
    main()


