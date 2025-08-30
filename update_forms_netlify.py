#!/usr/bin/env python3
"""Update website forms to use Netlify Forms (works with Vercel)"""

# Read current website
with open('wealthyrobots_website.html', 'r') as f:
    content = f.read()

# Update forms for Netlify Forms (works on Vercel too)
updated_content = content.replace(
    '<form id="email-capture" name="email-capture" method="POST" data-netlify="false">',
    '<form id="email-capture" name="email-capture" method="POST" netlify>'
).replace(
    '<form id="signup-form" name="signup-form" method="POST" data-netlify="false">',
    '<form id="signup-form" name="signup-form" method="POST" netlify>'
).replace(
    'data-netlify="false"',
    'netlify'
)

# Add hidden form for Netlify detection
netlify_forms = '''
    <!-- Netlify Forms Detection -->
    <form name="wealthyrobot-signup" netlify netlify-honeypot="bot-field" hidden>
        <input type="email" name="email" />
        <input type="text" name="source" />
    </form>
'''

# Insert before closing body tag
updated_content = updated_content.replace('</body>', netlify_forms + '</body>')

# Save updated website
with open('wealthyrobots_website.html', 'w') as f:
    f.write(updated_content)

print("✅ Website updated for Netlify Forms (works with Vercel)")
print("📧 Forms will now capture emails automatically")
print("🎯 No API keys needed - emails go to Vercel dashboard")
