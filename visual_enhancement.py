#!/usr/bin/env python3
"""
Clean Visual Enhancement Methods
"""

def add_enhancement_methods():
    """Add enhancement methods to existing visual verifier"""
    
    enhancement_code = '''
    def analyze_visual_quality(self, tweet_elem):
        """Analyze visual quality of posted graphics"""
        try:
            # Look for images in the tweet
            images = tweet_elem.find_elements('css selector', 'img')
            quality_score = 5  # Base score
            issues = []
            
            for img in images:
                alt_text = img.get_attribute('alt') or ''
                
                # Quality indicators
                if any(word in alt_text.lower() for word in ['gradient', 'professional', 'branded']):
                    quality_score += 1
                elif any(word in alt_text.lower() for word in ['basic', 'simple', 'plain']):
                    quality_score -= 1
                    issues.append('Basic design detected')
                
                # Check for overused elements
                if 'blue' in alt_text.lower() and 'gradient' in alt_text.lower():
                    quality_score -= 1
                    issues.append('Overused blue gradient')
                
            return {
                'quality_score': max(1, min(10, quality_score)),
                'issues': issues,
                'has_visuals': len(images) > 0
            }
        except Exception as e:
            return {'error': str(e), 'quality_score': 0}
    
    def detect_duplicate_content(self, current_text, recent_tweets):
        """Detect duplicate content"""
        import difflib
        
        duplicates = []
        for recent in recent_tweets:
            similarity = difflib.SequenceMatcher(None, current_text.lower(), recent.lower()).ratio()
            if similarity > 0.7:
                duplicates.append({'similarity': similarity, 'text': recent[:50]})
        
        return {
            'is_duplicate': len(duplicates) > 0,
            'duplicates': duplicates
        }
    
    def assess_viral_potential(self, tweet_text):
        """Assess viral potential"""
        viral_score = 5
        factors = []
        
        # Viral keywords
        viral_words = ['ai', 'thread', 'reality', 'truth', 'secret']
        for word in viral_words:
            if word in tweet_text.lower():
                viral_score += 1
                factors.append(f'Contains: {word}')
        
        # Engagement hooks
        hooks = ['did you know', 'reality check', 'thread:']
        for hook in hooks:
            if hook in tweet_text.lower():
                viral_score += 2
                factors.append(f'Hook: {hook}')
        
        return {
            'viral_score': max(1, min(10, viral_score)),
            'factors': factors,
            'potential': 'high' if viral_score >= 7 else 'medium' if viral_score >= 5 else 'low'
        }
    
    def generate_recommendations(self, quality_analysis, viral_analysis, duplicate_analysis):
        """Generate improvement recommendations"""
        recommendations = []
        
        if quality_analysis.get('quality_score', 0) < 7:
            recommendations.append('UPGRADE VISUALS: Use more professional, dynamic graphics')
        
        if 'Basic design' in str(quality_analysis.get('issues', [])):
            recommendations.append('DESIGN BOOST: Replace basic elements with engaging visuals')
        
        if viral_analysis.get('viral_score', 0) < 6:
            recommendations.append('VIRAL BOOST: Add trending topics or stronger hooks')
        
        if duplicate_analysis.get('is_duplicate', False):
            recommendations.append('CONTENT VARIETY: Create fresh, unique content')
        
        return recommendations
'''
    
    # Read current file
    with open('twitter_visual_verifier.py', 'r') as f:
        content = f.read()
    
    # Find class end and insert methods
    lines = content.split('\n')
    
    # Find the last method in the class
    insert_pos = -1
    for i in range(len(lines)-1, 0, -1):
        if lines[i].strip().startswith('def ') and not lines[i].strip().startswith('def main'):
            insert_pos = i + 1
            break
    
    if insert_pos > 0:
        # Insert enhancement methods
        lines.insert(insert_pos, enhancement_code)
        
        with open('twitter_visual_verifier.py', 'w') as f:
            f.write('\n'.join(lines))
        
        print("✅ Enhancement methods added successfully")
        return True
    else:
        print("❌ Could not find insertion point")
        return False

if __name__ == "__main__":
    add_enhancement_methods()
