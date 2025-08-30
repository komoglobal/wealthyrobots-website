#!/usr/bin/env python3
"""
WEB DOWNLOAD SERVER
Simple web server to download TikTok videos through browser
"""

import http.server
import socketserver
import os
import json
from datetime import datetime
from pathlib import Path

class TikTokDownloadHandler(http.server.SimpleHTTPRequestHandler):
    """Custom handler for TikTok video downloads"""
    
    def do_GET(self):
        """Handle GET requests"""
        
        # Set CORS headers for browser access
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        
        # Handle different routes
        if self.path == '/':
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.serve_download_page()
        elif self.path == '/videos':
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.serve_video_list()
        elif self.path.startswith('/download/'):
            self.serve_video_download()
        elif self.path == '/download-zip':
            self.serve_zip_download()
        else:
            # Serve static files
            super().do_GET()
    
    def serve_download_page(self):
        """Serve the main download page"""
        
        html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🎬 TikTok Video Download Center</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            margin: 0;
            padding: 20px;
            min-height: 100vh;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            overflow: hidden;
        }
        .header {
            background: linear-gradient(135deg, #1a1a1a 0%, #00ff88 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }
        .header h1 {
            margin: 0;
            font-size: 2.5em;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        .header p {
            margin: 10px 0 0 0;
            font-size: 1.2em;
            opacity: 0.9;
        }
        .content {
            padding: 30px;
        }
        .stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        .stat-card {
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            color: white;
            padding: 20px;
            border-radius: 15px;
            text-align: center;
            box-shadow: 0 10px 20px rgba(0,0,0,0.1);
        }
        .stat-number {
            font-size: 2em;
            font-weight: bold;
            margin-bottom: 5px;
        }
        .videos-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 20px;
            margin-top: 30px;
        }
        .video-card {
            background: white;
            border: 2px solid #f0f0f0;
            border-radius: 15px;
            padding: 20px;
            text-align: center;
            transition: all 0.3s ease;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }
        .video-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 15px 30px rgba(0,0,0,0.2);
            border-color: #00ff88;
        }
        .video-type {
            background: linear-gradient(135deg, #00ff88, #00cc6a);
            color: white;
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 0.9em;
            font-weight: bold;
            margin-bottom: 15px;
            display: inline-block;
        }
        .video-title {
            font-size: 1.1em;
            font-weight: bold;
            margin-bottom: 10px;
            color: #333;
        }
        .video-duration {
            color: #666;
            margin-bottom: 15px;
        }
        .download-btn {
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            border: none;
            padding: 12px 25px;
            border-radius: 25px;
            font-size: 1em;
            font-weight: bold;
            cursor: pointer;
            transition: all 0.3s ease;
            text-decoration: none;
            display: inline-block;
        }
        .download-btn:hover {
            transform: scale(1.05);
            box-shadow: 0 10px 20px rgba(0,0,0,0.2);
        }
        .loading {
            text-align: center;
            padding: 40px;
            color: #666;
        }
        .error {
            background: #ff6b6b;
            color: white;
            padding: 15px;
            border-radius: 10px;
            margin: 20px 0;
            text-align: center;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎬 TikTok Video Download Center</h1>
            <p>Your automated TikTok empire is ready! Download all 13 videos below.</p>
        </div>
        
        <div class="content">
            <div class="stats">
                <div class="stat-card">
                    <div class="stat-number" id="total-videos">13</div>
                    <div>Total Videos</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number" id="trending-videos">4</div>
                    <div>Trending Content</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number" id="streamer-videos">9</div>
                    <div>Streamer Clips</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">60MB</div>
                    <div>Total Size</div>
                </div>
            </div>
            
            <div id="videos-container">
                <div class="loading">Loading your TikTok videos...</div>
            </div>
        </div>
    </div>

    <script>
        // Load video list
        fetch('/videos')
            .then(response => response.json())
            .then(data => {
                displayVideos(data.videos);
            })
            .catch(error => {
                document.getElementById('videos-container').innerHTML = 
                    '<div class="error">Error loading videos: ' + error.message + '</div>';
            });

        function displayVideos(videos) {
            const container = document.getElementById('videos-container');
            
            if (!videos || videos.length === 0) {
                container.innerHTML = '<div class="error">No videos found</div>';
                return;
            }

            let html = '<div class="videos-grid">';
            
            videos.forEach(video => {
                const typeClass = video.type === 'trending' ? 'trending' : 'streamer';
                const typeText = video.type === 'trending' ? '🔥 Trending' : '🎮 Streamer Clip';
                const duration = video.type === 'trending' ? '15s' : '20s';
                
                html += `
                    <div class="video-card">
                        <div class="video-type ${typeClass}">${typeText}</div>
                        <div class="video-title">${video.filename}</div>
                        <div class="video-duration">Duration: ${duration}</div>
                        <a href="/download/${video.filename}" class="download-btn" download>
                            📥 Download Video
                        </a>
                    </div>
                `;
            });
            
            html += '</div>';
            container.innerHTML = html;
        }
    </script>
</body>
</html>
        """
        
        self.wfile.write(html_content.encode())
    
    def serve_video_list(self):
        """Serve JSON list of available videos"""
        
        videos_dir = "generated_videos"
        videos = []
        
        if os.path.exists(videos_dir):
            for filename in os.listdir(videos_dir):
                if filename.endswith('.mp4'):
                    video_type = 'trending' if 'trending' in filename else 'streamer_clip'
                    videos.append({
                        'filename': filename,
                        'type': video_type,
                        'size': os.path.getsize(os.path.join(videos_dir, filename)),
                        'path': os.path.join(videos_dir, filename)
                    })
        
        # Sort videos by type and creation time
        videos.sort(key=lambda x: (x['type'], x['filename']))
        
        response = {
            'timestamp': datetime.now().isoformat(),
            'total_videos': len(videos),
            'videos': videos
        }
        
        self.wfile.write(json.dumps(response, indent=2).encode())
    
    def serve_video_download(self):
        """Serve video file for download"""
        
        if not self.path.startswith('/download/'):
            self.send_error(404, "Not found")
            return
        
        filename = self.path[10:]  # Remove '/download/' prefix
        filepath = os.path.join('generated_videos', filename)
        
        if not os.path.exists(filepath):
            self.send_error(404, "Video not found")
            return
        
        # Set headers for file download
        self.send_header('Content-type', 'video/mp4')
        self.send_header('Content-Disposition', f'attachment; filename="{filename}"')
        self.end_headers()
        
        # Stream the file
        with open(filepath, 'rb') as f:
            self.wfile.write(f.read())
    
    def serve_zip_download(self):
        """Serve the complete video archive zip file"""
        
        zip_filename = "tiktok_videos_20250816_122409.zip"
        zip_path = os.path.join(os.getcwd(), zip_filename)
        
        if not os.path.exists(zip_path):
            self.send_error(404, "Zip file not found")
            return
        
        # Set headers for file download
        self.send_header('Content-type', 'application/zip')
        self.send_header('Content-Disposition', f'attachment; filename="{zip_filename}"')
        self.end_headers()
        
        # Stream the zip file
        with open(zip_path, 'rb') as f:
            self.wfile.write(f.read())

def main():
    """Start the web download server"""
    
    PORT = 8081
    
    # Change to the directory containing the videos
    os.chdir('/home/ubuntu/wealthyrobot')
    
    # Create server
    with socketserver.TCPServer(("", PORT), TikTokDownloadHandler) as httpd:
        print(f"🌐 TikTok Video Download Server Started!")
        print(f"📱 Server running on port {PORT}")
        print(f"🌍 Access from your browser: http://18.119.101.105:{PORT}")
        print(f"📁 Serving videos from: {os.path.abspath('generated_videos')}")
        print(f"🎬 Total videos available: {len([f for f in os.listdir('generated_videos') if f.endswith('.mp4')])}")
        print(f"\n💻 To download videos:")
        print(f"   1. Open your browser")
        print(f"   2. Go to: http://18.119.101.105:{PORT}")
        print(f"   3. Click download buttons for each video")
        print(f"   4. All 13 videos will download to your computer!")
        print(f"\n⏹️  Press Ctrl+C to stop the server")
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print(f"\n🛑 Server stopped by user")
            httpd.shutdown()

if __name__ == "__main__":
    main()
