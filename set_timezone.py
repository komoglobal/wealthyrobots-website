#!/usr/bin/env python3
import os
os.environ['TZ'] = 'America/New_York'

# This ensures all datetime operations use EST
import time
time.tzset()

print("✅ Timezone set to EST for all operations")
