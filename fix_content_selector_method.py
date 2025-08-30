#!/usr/bin/env python3
"""
Fix the content selector method compatibility
"""

# Check what method the content selector actually has
import inspect
try:
    from dynamic_content_selector import DynamicContentSelector
    
    selector = DynamicContentSelector()
    methods = [method for method in dir(selector) if not method.startswith('_')]
    
    print("🔍 Available methods in DynamicContentSelector:")
    for method in methods:
        if 'select' in method.lower() or 'choose' in method.lower() or 'decision' in method.lower():
            print(f"  ✅ {method}")
    
    # Try to find the correct method
    if hasattr(selector, 'select_content_type'):
        print("✅ select_content_type method exists")
    elif hasattr(selector, 'select_content'):
        print("✅ select_content method exists - this might be the right one")
    elif hasattr(selector, 'choose_content_type'):
        print("✅ choose_content_type method exists")
    elif hasattr(selector, 'make_decision'):
        print("✅ make_decision method exists")
    else:
        print("❌ No obvious selection method found")
        print("All methods:", [m for m in methods if not m.startswith('_')])

except Exception as e:
    print(f"❌ Error: {e}")
