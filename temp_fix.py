#!/usr/bin/env python3
import re

# Read the file
with open('social_media_agent.py', 'r') as f:
    content = f.read()

# Find and fix incomplete try blocks
lines = content.split('\n')
fixed_lines = []
in_try_block = False
indent_level = 0

for i, line in enumerate(lines):
    if 'try:' in line:
        in_try_block = True
        indent_level = len(line) - len(line.lstrip())
        fixed_lines.append(line)
    elif in_try_block and line.strip().startswith('time.sleep(60)'):
        # This is line 68 - ensure it's properly indented in try block
        fixed_lines.append(line)
        # Add except block if missing
        if i + 1 < len(lines) and not lines[i + 1].strip().startswith('except'):
            fixed_lines.append(' ' * indent_level + 'except Exception as e:')
            fixed_lines.append(' ' * indent_level + '    print(f"Error in social media agent: {e}")')
        in_try_block = False
    else:
        fixed_lines.append(line)

# Write back
with open('social_media_agent.py', 'w') as f:
    f.write('\n'.join(fixed_lines))

print("✅ Fixed syntax error in social_media_agent.py")
#!/usr/bin/env python3
import re

# Read the file
with open('social_media_agent.py', 'r') as f:
    content = f.read()

# Find and fix incomplete try blocks
lines = content.split('\n')
fixed_lines = []
in_try_block = False
indent_level = 0

for i, line in enumerate(lines):
    if 'try:' in line:
        in_try_block = True
        indent_level = len(line) - len(line.lstrip())
        fixed_lines.append(line)
    elif in_try_block and line.strip().startswith('time.sleep(60)'):
        # This is line 68 - ensure it's properly indented in try block
        fixed_lines.append(line)
        # Add except block if missing
        if i + 1 < len(lines) and not lines[i + 1].strip().startswith('except'):
            fixed_lines.append(' ' * indent_level + 'except Exception as e:')
            fixed_lines.append(' ' * indent_level + '    print(f"Error in social media agent: {e}")')
        in_try_block = False
    else:
        fixed_lines.append(line)

# Write back
with open('social_media_agent.py', 'w') as f:
    f.write('\n'.join(fixed_lines))

print("✅ Fixed syntax error in social_media_agent.py")
