import json
import os
import time
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import threading

class LiveConfigManager:
    def __init__(self):
        self.config_file = "live_config.json"
        self.config = self.load_config()
        self.observers = []
        self.callbacks = {}
        self.setup_file_watcher()
        
    def load_config(self):
        """Load configuration from JSON file"""
        default_config = {
            "ceo_settings": {
                "daily_budget": 100,
                "monthly_budget": 1000,
                "approval_threshold": 250,
                "auto_invest_percentage": 20,
                "risk_tolerance": 5,
                "aggression_level": 5
            },
            "automation_settings": {
                "cycle_interval_minutes": 60,
                "content_frequency": 4,
                "social_frequency": 6,
                "analytics_frequency": 8,
                "enabled_agents": ["content", "social", "analytics", "ceo"]
            },
            "strategy_overrides": {
                "pause_automation": False,
                "emergency_stop": False,
                "manual_mode": False,
                "focus_areas": ["affiliate_marketing", "content_creation"]
            },
            "live_commands": {
                "command": None,
                "timestamp": None,
                "executed": True
            }
        }
        
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    loaded_config = json.load(f)
                # Merge with defaults to ensure all keys exist
                for key in default_config:
                    if key not in loaded_config:
                        loaded_config[key] = default_config[key]
                return loaded_config
            except:
                pass
        
        # Create default config file
        self.save_config(default_config)
        return default_config
    
    def save_config(self, config=None):
        """Save configuration to JSON file"""
        if config is None:
            config = self.config
        
        with open(self.config_file, 'w') as f:
            json.dump(config, f, indent=2)
    
    def setup_file_watcher(self):
        """Set up file system watcher for live config changes"""
        class ConfigHandler(FileSystemEventHandler):
            def __init__(self, config_manager):
                self.config_manager = config_manager
            
            def on_modified(self, event):
                if event.src_path.endswith('live_config.json'):
                    print(f"🔄 Live config updated at {datetime.now()}")
                    self.config_manager.reload_config()
        
        event_handler = ConfigHandler(self)
        observer = Observer()
        observer.schedule(event_handler, '.', recursive=False)
        observer.start()
        self.observers.append(observer)
    
    def reload_config(self):
        """Reload configuration and notify subscribers"""
        old_config = self.config.copy()
        self.config = self.load_config()
        
        # Check for new commands
        self.process_live_commands()
        
        # Notify registered callbacks of changes
        for callback_name, callback_func in self.callbacks.items():
            try:
                callback_func(old_config, self.config)
            except Exception as e:
                print(f"❌ Error in callback {callback_name}: {e}")
    
    def register_callback(self, name, callback_func):
        """Register callback for config changes"""
        self.callbacks[name] = callback_func
        print(f"✅ Registered live config callback: {name}")
    
    def process_live_commands(self):
        """Process live commands from config"""
        command_data = self.config.get('live_commands', {})
        
        if (command_data.get('command') and 
            not command_data.get('executed', True)):
            
            command = command_data['command']
            print(f"🎮 Processing live command: {command}")
            
            # Mark as executed
            self.config['live_commands']['executed'] = True
            self.config['live_commands']['timestamp'] = datetime.now().isoformat()
            self.save_config()
            
            # Execute command
            self.execute_live_command(command)
    
    def execute_live_command(self, command):
        """Execute live commands"""
        if command == "pause_automation":
            self.config['strategy_overrides']['pause_automation'] = True
            print("⏸️ Automation paused via live command")
        
        elif command == "resume_automation":
            self.config['strategy_overrides']['pause_automation'] = False
            print("▶️ Automation resumed via live command")
        
        elif command == "emergency_stop":
            self.config['strategy_overrides']['emergency_stop'] = True
            print("🚨 EMERGENCY STOP activated!")
        
        elif command == "enable_manual_mode":
            self.config['strategy_overrides']['manual_mode'] = True
            print("🎮 Manual mode enabled")
        
        elif command == "increase_budget":
            self.config['ceo_settings']['daily_budget'] *= 1.5
            print(f"💰 Budget increased to ${self.config['ceo_settings']['daily_budget']}")
        
        elif command == "conservative_mode":
            self.config['ceo_settings']['risk_tolerance'] = 2
            self.config['ceo_settings']['aggression_level'] = 2
            print("🛡️ Conservative mode activated")
        
        elif command == "aggressive_mode":
            self.config['ceo_settings']['risk_tolerance'] = 8
            self.config['ceo_settings']['aggression_level'] = 8
            print("🚀 Aggressive mode activated")
        
        self.save_config()
    
    def get(self, key_path, default=None):
        """Get config value using dot notation (e.g., 'ceo_settings.daily_budget')"""
        keys = key_path.split('.')
        value = self.config
        
        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return default
        
        return value
    
    def set(self, key_path, value):
        """Set config value using dot notation"""
        keys = key_path.split('.')
        config = self.config
        
        for key in keys[:-1]:
            if key not in config:
                config[key] = {}
            config = config[key]
        
        config[keys[-1]] = value
        self.save_config()
        print(f"✅ Updated {key_path} = {value}")
    
    def send_live_command(self, command):
        """Send a live command to the system"""
        self.config['live_commands'] = {
            "command": command,
            "timestamp": datetime.now().isoformat(),
            "executed": False
        }
        self.save_config()
        print(f"📤 Live command sent: {command}")
    
    def cleanup(self):
        """Clean up file watchers"""
        for observer in self.observers:
            observer.stop()
            observer.join()

class LiveControlInterface:
    def __init__(self, config_manager):
        self.config = config_manager
        
    def show_live_controls(self):
        """Show available live controls"""
        print("\n" + "="*50)
        print("🎮 LIVE CONTROL INTERFACE")
        print("="*50)
        print("Current Status:")
        print(f"💰 Daily Budget: ${self.config.get('ceo_settings.daily_budget')}")
        print(f"⚡ Automation: {'PAUSED' if self.config.get('strategy_overrides.pause_automation') else 'RUNNING'}")
        print(f"🎯 Risk Level: {self.config.get('ceo_settings.risk_tolerance')}/10")
        print(f"🔥 Aggression: {self.config.get('ceo_settings.aggression_level')}/10")
        
        print("\n📋 Available Commands:")
        print("1. pause_automation - Pause all automation")
        print("2. resume_automation - Resume automation")
        print("3. emergency_stop - Stop everything immediately")
        print("4. enable_manual_mode - Switch to manual control")
        print("5. increase_budget - Increase daily budget by 50%")
        print("6. conservative_mode - Set low risk/aggression")
        print("7. aggressive_mode - Set high risk/aggression")
        print("8. exit - Exit live control")
        
        return input("\n🎮 Enter command: ").strip()
    
    def run_interactive_control(self):
        """Run interactive live control"""
        print("🎮 Starting Live Control Interface...")
        print("💡 You can edit live_config.json directly or use this interface")
        
        while True:
            try:
                command = self.show_live_controls()
                
                if command == "exit":
                    break
                elif command in ["pause_automation", "resume_automation", "emergency_stop", 
                               "enable_manual_mode", "increase_budget", "conservative_mode", 
                               "aggressive_mode"]:
                    self.config.send_live_command(command)
                    time.sleep(1)  # Give system time to process
                else:
                    print("❌ Unknown command")
                
            except KeyboardInterrupt:
                break
        
        print("👋 Exiting live control interface")

if __name__ == "__main__":
    config = LiveConfigManager()
    interface = LiveControlInterface(config)
    interface.run_interactive_control()
