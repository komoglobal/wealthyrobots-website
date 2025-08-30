#!/usr/bin/env python3
"""
Twitter Empire Scheduler - Runs master controller at optimal times
"""
import time
import schedule
from master_twitter_controller import MasterTwitterController

def post_content():
    """Scheduled posting function"""
    controller = MasterTwitterController()
    success, content = controller.post_coordinated_content()
    
    if success:
        print(f"✅ Scheduled post successful at {time.strftime('%H:%M')}")
    else:
        print(f"⏳ Scheduled post skipped: {content}")

# Schedule posts at optimal times
schedule.every().day.at("09:00").do(post_content)  # Morning educational
schedule.every().day.at("13:00").do(post_content)  # Afternoon viral
schedule.every().day.at("17:00").do(post_content)  # Evening mixed
schedule.every().day.at("21:00").do(post_content)  # Night promotional

print("📅 Twitter Empire Scheduler started")
print("⏰ Posting times: 9:00, 13:00, 17:00, 21:00")

while True:
    schedule.run_pending()
    time.sleep(60)  # Check every minute
