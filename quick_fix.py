import re

# Read the file
with open('unified_twitter_empire.py', 'r') as f:
    content = f.read()

# Fix the response handling
content = re.sub(
    r"tweet_result = safe_twitter_post\(content=content_data\['content'\]\)",
    """# Handle different response types from safe_twitter_post
                tweet_response = safe_twitter_post(content=content_data['content'])
                
                # Convert response to consistent format
                if isinstance(tweet_response, tuple):
                    # If tuple, assume (success, tweet_id or error)
                    success, data = tweet_response
                    if success:
                        tweet_result = {'success': True, 'tweet_id': data}
                    else:
                        tweet_result = {'success': False, 'error': data}
                elif isinstance(tweet_response, dict):
                    tweet_result = tweet_response
                else:
                    # Fallback
                    tweet_result = {'success': True, 'tweet_id': str(tweet_response)}""",
    content
)

# Write back
with open('unified_twitter_empire.py', 'w') as f:
    f.write(content)

print("✅ Fixed tuple response handling")
