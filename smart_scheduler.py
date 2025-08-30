#!/usr/bin/env python3
"""
Smart Empire Scheduler - Prevents conflicts and optimizes timing
Coordinates with Unified Twitter Empire to respect rate limits
"""

import os
import time
import json
import signal
import threading
from datetime import datetime, timedelta
from typing import Dict, List
import subprocess
import logging

# Configure logging for scheduler (stdout so cron captures to log file)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s [smart_scheduler] %(message)s",
    handlers=[logging.StreamHandler()]
)

class SmartScheduler:
    """Intelligent scheduling system that prevents API conflicts"""
    
    def __init__(self):
        self.running = False
        self.schedule_file = 'empire_schedule.json'
        self.lock_file = 'empire.lock'
        
        # Optimal posting times (in 24h format)
        self.optimal_times = [
            {'hour': 8, 'minute': 30, 'type': 'educational'},   # Morning commute
            {'hour': 12, 'minute': 15, 'type': 'viral'},       # Lunch break
            {'hour': 17, 'minute': 45, 'type': 'educational'}, # Evening commute
            {'hour': 20, 'minute': 30, 'type': 'promotional'}  # Evening engagement
        ]
        
        # Minimum intervals to prevent conflicts
        self.min_interval_minutes = 45
        self.safety_buffer_minutes = 5
        
    def create_lock(self) -> bool:
        """Create lock file to prevent multiple schedulers"""
        if os.path.exists(self.lock_file):
            try:
                with open(self.lock_file, 'r') as f:
                    existing_pid = int(f.read().strip())
                
                # Check if process is still running
                try:
                    os.kill(existing_pid, 0)  # Doesn't actually kill, just checks
                    logging.warning(f"Another scheduler is running (PID: {existing_pid})")
                    return False
                except OSError:
                    # Process doesn't exist, remove stale lock
                    os.remove(self.lock_file)
                    logging.info("Removed stale lock file")
            except (ValueError, IOError):
                # Invalid lock file, remove it
                os.remove(self.lock_file)
        
        # Create new lock
        with open(self.lock_file, 'w') as f:
            f.write(str(os.getpid()))
        
        logging.info(f"Lock created (PID: {os.getpid()})")
        return True
    
    def remove_lock(self):
        """Remove lock file"""
        try:
            if os.path.exists(self.lock_file):
                os.remove(self.lock_file)
                logging.info("Lock removed")
        except Exception as e:
            logging.error(f"Error removing lock: {e}")
    
    def load_schedule(self) -> List[Dict]:
        """Load existing schedule"""
        try:
            if os.path.exists(self.schedule_file):
                with open(self.schedule_file, 'r') as f:
                    schedule = json.load(f)
                    # Filter out past items
                    now = datetime.now()
                    return [item for item in schedule if datetime.fromisoformat(item['scheduled_time']) > now]
        except Exception as e:
            logging.error(f"Error loading schedule: {e}")
        
        return []
    
    def save_schedule(self, schedule: List[Dict]):
        """Save schedule to disk"""
        try:
            with open(self.schedule_file, 'w') as f:
                json.dump(schedule, f, indent=2)
        except Exception as e:
            logging.error(f"Error saving schedule: {e}")
    
    def generate_daily_schedule(self) -> List[Dict]:
        """Generate optimized daily schedule"""
        schedule = []
        today = datetime.now().date()
        
        for time_slot in self.optimal_times:
            scheduled_time = datetime.combine(today, datetime.min.time().replace(
                hour=time_slot['hour'], 
                minute=time_slot['minute']
            ))
            
            # Skip if time has passed today
            if scheduled_time <= datetime.now():
                # Schedule for tomorrow instead
                scheduled_time += timedelta(days=1)
            
            schedule.append({
                'id': f"{scheduled_time.strftime('%Y%m%d_%H%M')}_{time_slot['type']}",
                'scheduled_time': scheduled_time.isoformat(),
                'content_type': time_slot['type'],
                'status': 'pending',
                'created': datetime.now().isoformat()
            })
        
        return schedule
    
    def is_safe_to_post(self) -> bool:
        """Check if it's safe to post (no other posting processes)"""
        # Check for other Twitter processes
        conflicting_processes = [
            'master_twitter_controller.py',
            'automated_twitter_revenue.py',
            'twitter_posting_agent.py',
            'social_media_agent.py'
        ]
        
        for process in conflicting_processes:
            try:
                result = subprocess.run(
                    ['pgrep', '-f', process], 
                    capture_output=True, 
                    text=True
                )
                if result.returncode == 0 and result.stdout.strip():
                    logging.warning(f"Conflicting process detected: {process}")
                    return False
            except Exception:
                pass
        
        return True
    
    def execute_post(self, schedule_item: Dict) -> bool:
        """Execute a scheduled post"""
        logging.info(f"EXECUTE POST | time={schedule_item['scheduled_time']} type={schedule_item['content_type']}")
        
        # Safety check
        if not self.is_safe_to_post():
            logging.warning("Unsafe to post - conflicting processes detected")
            return False
        
        try:
            # Execute unified empire posting
            result = subprocess.run([
                'python3', 'unified_twitter_empire.py'
            ], capture_output=True, text=True, timeout=120)
            
            if result.returncode == 0:
                logging.info("Post executed successfully")
                logging.debug(result.stdout[-200:] if result.stdout else 'No output')
                return True
            else:
                logging.error(f"Post execution failed: {result.stderr}")
                return False
                
        except subprocess.TimeoutExpired:
            logging.error("Post execution timed out")
            return False
        except Exception as e:
            logging.exception(f"Error executing post: {e}")
            return False
    
    def run_scheduler(self):
        """Main scheduler loop"""
        logging.info("SMART EMPIRE SCHEDULER STARTING")
        
        if not self.create_lock():
            return
        
        # Set up signal handlers
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
        
        self.running = True
        schedule = self.load_schedule()
        
        # Generate schedule if empty
        if not schedule:
            logging.info("Generating new daily schedule…")
            schedule = self.generate_daily_schedule()
            self.save_schedule(schedule)
        
        logging.info(f"Loaded scheduled items: {len(schedule)}")
        
        try:
            while self.running:
                now = datetime.now()
                executed_any = False
                
                # Check for items to execute
                for item in schedule[:]:
                    if item['status'] != 'pending':
                        continue
                    
                    scheduled_time = datetime.fromisoformat(item['scheduled_time'])
                    
                    # Check if it's time to post (within 2 minutes)
                    if abs((now - scheduled_time).total_seconds()) <= 120:
                        logging.info(f"Scheduled time reached: {item['id']}")
                        
                        # Execute post
                        success = self.execute_post(item)
                        
                        # Update status
                        item['status'] = 'completed' if success else 'failed'
                        item['executed_time'] = now.isoformat()
                        
                        executed_any = True
                        
                        # Save updated schedule
                        self.save_schedule(schedule)
                        
                        # Wait a bit before checking again
                        time.sleep(60)
                
                # Generate new schedule if we're running low
                pending_items = [item for item in schedule if item['status'] == 'pending']
                if len(pending_items) < 2:
                    logging.info("Generating additional schedule items…")
                    new_items = self.generate_daily_schedule()
                    schedule.extend(new_items)
                    self.save_schedule(schedule)
                
                # Clean up old completed items
                cutoff = now - timedelta(days=2)
                schedule = [item for item in schedule if 
                           item['status'] == 'pending' or 
                           datetime.fromisoformat(item.get('executed_time', item['created'])) > cutoff]
                
                if not executed_any:
                    # Sleep for 30 seconds before next check
                    time.sleep(30)
                
                # Status update every 10 minutes
                if now.minute % 10 == 0 and now.second < 30:
                    self._print_status(schedule)
                    time.sleep(30)  # Avoid printing multiple times
        
        except Exception as e:
            logging.exception(f"Scheduler error: {e}")
        
        finally:
            self.running = False
            self.remove_lock()
            logging.info("Scheduler stopped")
    
    def _print_status(self, schedule: List[Dict]):
        """Print current status"""
        now = datetime.now()
        pending = [item for item in schedule if item['status'] == 'pending']
        
        logging.info(f"📊 SCHEDULER STATUS - {now.strftime('%H:%M:%S')} - Pending posts: {len(pending)}")
        
        if pending:
            next_post = min(pending, key=lambda x: datetime.fromisoformat(x['scheduled_time']))
            next_time = datetime.fromisoformat(next_post['scheduled_time'])
            time_until = next_time - now
            
            if time_until.total_seconds() > 0:
                hours, remainder = divmod(int(time_until.total_seconds()), 3600)
                minutes, _ = divmod(remainder, 60)
                logging.info(f"Next post: {next_time.strftime('%H:%M')} ({hours:02d}:{minutes:02d} remaining)")
            else:
                logging.warning(f"Next post: {next_time.strftime('%H:%M')} (overdue)")
    
    def _signal_handler(self, signum, frame):
        """Handle shutdown signals"""
        print(f"\n🛑 Received signal {signum}, shutting down gracefully...")
        self.running = False
    
    def get_schedule_status(self) -> Dict:
        """Get current schedule status"""
        schedule = self.load_schedule()
        now = datetime.now()
        
        pending = [item for item in schedule if item['status'] == 'pending']
        completed_today = [item for item in schedule if 
                          item['status'] == 'completed' and 
                          item.get('executed_time') and
                          datetime.fromisoformat(item['executed_time']).date() == now.date()]
        
        return {
            'total_scheduled': len(schedule),
            'pending': len(pending),
            'completed_today': len(completed_today),
            'next_post': min(pending, key=lambda x: x['scheduled_time'])['scheduled_time'] if pending else None,
            'is_running': os.path.exists(self.lock_file)
        }

def main():
    """Main execution"""
    import sys
    
    scheduler = SmartScheduler()
    
    if len(sys.argv) > 1 and sys.argv[1] == '--status':
        # Just show status
        status = scheduler.get_schedule_status()
        logging.info("🏰 EMPIRE SCHEDULER STATUS")
        logging.info(f"Running: {'✅' if status['is_running'] else '❌'}")
        logging.info(f"Scheduled posts: {status['total_scheduled']}")
        logging.info(f"Pending: {status['pending']}")
        logging.info(f"Completed today: {status['completed_today']}")
        if status['next_post']:
            next_time = datetime.fromisoformat(status['next_post'])
            logging.info(f"Next post: {next_time.strftime('%Y-%m-%d %H:%M')}")
    else:
        # Run the scheduler
        scheduler.run_scheduler()

if __name__ == "__main__":
    main()
