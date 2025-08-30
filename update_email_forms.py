#!/usr/bin/env python3
"""Update website forms to use Vercel Forms + webhook to email marketing agent"""

# Read current website
with open('wealthyrobots_website.html', 'r') as f:
    content = f.read()

# Add Vercel form integration
updated_content = content.replace(
    '<form id="email-capture">',
    '<form id="email-capture" name="email-capture" method="POST" data-netlify="false">'
).replace(
    '<form id="signup-form">',
    '<form id="signup-form" name="signup-form" method="POST" data-netlify="false">'
)

# Save updated website
with open('wealthyrobots_website.html', 'w') as f:
    f.write(updated_content)

print("✅ Website updated for Vercel Forms integration")
