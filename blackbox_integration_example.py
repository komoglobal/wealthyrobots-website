#!/usr/bin/env python3
"""
Example: How WealthyRobot agents should use the blackbox
"""
from claude_testing_blackbox import ClaudeTestingBlackbox

def test_content_strategy():
    """Test new content generation safely"""
    bb = ClaudeTestingBlackbox()
    
    # Properly formatted content generation code
    content_code = '''
topics = ["AI automation", "productivity hacks", "future tech"]
for i, topic in enumerate(topics, 1):
    print(f"{i}. {topic.upper()}: The game-changer you need!")
print("\\nThread complete! Ready for Twitter!")
'''
    
    result = bb.test_code_execution(content_code, 'viral_content_test')
    
    if result.get('success'):
        print("✅ Content strategy validated - deploying to production!")
        return True
    else:
        print(f"❌ Content test failed: {result.get('stderr', 'Unknown error')}")
        return False

def test_engagement_algorithm():
    """Test engagement optimization algorithms"""
    bb = ClaudeTestingBlackbox()
    
    def calculate_viral_score(content):
        # Example scoring algorithm
        keywords = ['AI', 'automation', 'productivity', 'future']
        score = sum(10 for keyword in keywords if keyword.lower() in content.lower())
        score += len(content.split()) * 0.5  # Word count factor
        return round(score, 2)
    
    test_content = "AI automation will revolutionize productivity in the future"
    result = bb.test_algorithm_performance(calculate_viral_score, test_content, 'viral_score_test')
    
    if result.get('success'):
        print("✅ Algorithm validated - ready for deployment!")
        return True
    else:
        print("❌ Algorithm test failed")
        return False

if __name__ == "__main__":
    print("🤖 WealthyRobot Agent Testing Framework")
    print("=" * 40)
    
    # Run tests
    content_ok = test_content_strategy()
    algorithm_ok = test_engagement_algorithm()
    
    if content_ok and algorithm_ok:
        print("\n🚀 ALL TESTS PASSED - READY FOR PRODUCTION!")
    else:
        print("\n⚠️ Some tests failed - review before deployment")
