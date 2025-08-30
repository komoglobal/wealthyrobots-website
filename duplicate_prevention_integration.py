#!/usr/bin/env python3
"""
Integrate Duplicate Prevention into Live System
"""

import hashlib
import os
import json
from datetime import datetime

class LiveDuplicateChecker:
    def __init__(self):
        self.content_history_file = 'content_history.json'
        self.load_history()
    
    def load_history(self):
        """Load existing content history"""
        if os.path.exists(self.content_history_file):
            with open(self.content_history_file, 'r') as f:
                self.history = json.load(f)
        else:
            self.history = []
    
    def save_history(self):
        """Save content history"""
        with open(self.content_history_file, 'w') as f:
            json.dump(self.history[-50:], f)  # Keep last 50 posts only
    
    def is_duplicate(self, content):
        """Check if content is duplicate"""
        content_clean = content.lower().replace('tweet 1:', '').replace('tweet 2:', '').strip()
        content_hash = hashlib.md5(content_clean.encode()).hexdigest()
        
        # Check exact duplicates
        for item in self.history:
            if item['hash'] == content_hash:
                return True, f"Exact duplicate of post from {item['timestamp']}"
        
        # Check similarity
        content_words = set(content_clean.split())
        for item in self.history[-10:]:  # Check last 10 posts
            prev_words = set(item['content'].split())
            if len(content_words) > 0 and len(prev_words) > 0:
                similarity = len(content_words & prev_words) / len(content_words | prev_words)
                if similarity > 0.7:  # 70% similar
                    return True, f"Very similar to post from {item['timestamp']} (similarity: {similarity:.1%})"
        
        # Not a duplicate - add to history
        self.history.append({
            'timestamp': datetime.now().isoformat(),
            'content': content_clean,
            'hash': content_hash
        })
        self.save_history()
        
        return False, "Unique content"

# Global duplicate checker
global_duplicate_checker = LiveDuplicateChecker()

# Test it
if __name__ == "__main__":
    checker = LiveDuplicateChecker()
    
    # Test with sample content
    test_content = "AI REALITY CHECK THREAD: TWEET 1: Things AI can do"
    is_dup, message = checker.is_duplicate(test_content)
    
    print(f"Test: {message}")
    print("✅ Duplicate prevention system ready")
