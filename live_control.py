#!/usr/bin/env python3
from live_config_manager import LiveConfigManager, LiveControlInterface

if __name__ == "__main__":
    config = LiveConfigManager()
    interface = LiveControlInterface(config)
    interface.run_interactive_control()
