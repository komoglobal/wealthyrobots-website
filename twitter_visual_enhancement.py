import time
#!/usr/bin/env python3
"""
Twitter Visual Enhancement Module
Works with existing twitter_visual_verifier.py
"""

import difflib
import json
from datetime import datetime

class VisualEnhancer:
    def __init__(self):
        self.quality_standards = {
            'minimum_quality': 6,
            'viral_threshold': 7,
            'duplicate_threshold': 0.7
        }
    
    def analyze_visual_quality(self, image_description="", tweet_text=""):
        """Analyze visual quality without browser automation"""
        quality_score = 5
        issues = []
        
        # Analyze based on description/text
        description = (image_description + " " + tweet_text).lower()
        
        # Positive indicators
        if any(word in description for word in ['professional', 'branded', 'dynamic', 'engaging']):
            quality_score += 2
        if any(word in description for word in ['gradient', 'modern', 'sleek']):
            quality_score += 1
            
        # Negative indicators
        if any(word in description for word in ['basic', 'simple', 'plain', 'boring']):
            quality_score -= 2
            issues.append("Basic/simple design detected")
        if 'blue gradient' in description:
            quality_score -= 1
            issues.append("Overused blue gradient background")
            
        return {
            'quality_score': max(1, min(10, quality_score)),
            'issues': issues,
            'recommendation': 'upgrade_needed' if quality_score < 6 else 'good_quality'
        }
    
    def detect_duplicates(self, current_content, recent_content_list):
        """Detect duplicate content"""
        duplicates_found = []
        
        for recent in recent_content_list:
            similarity = difflib.SequenceMatcher(None, 
                current_content.lower(), 
                recent.lower()
            ).ratio()
            
            if similarity > self.quality_standards['duplicate_threshold']:
                duplicates_found.append({
                    'similarity': round(similarity, 2),
                    'content_preview': recent[:100] + "..."
                })
        
        return {
            'is_duplicate': len(duplicates_found) > 0,
            'duplicate_count': len(duplicates_found),
            'duplicates': duplicates_found
        }
    
    def assess_viral_potential(self, tweet_content):
        """Assess viral potential of content"""
        viral_score = 5
        viral_factors = []
        
        content_lower = tweet_content.lower()
        
        # Strong viral indicators
        viral_keywords = ['ai', 'reality check', 'thread', 'truth', 'secret', 'exposed']
        for keyword in viral_keywords:
            if keyword in content_lower:
                viral_score += 1
                viral_factors.append(f"Contains viral keyword: {keyword}")
        
        # Engagement hooks
        hooks = ['did you know', "here's what", 'reality check', 'thread:', 'tweet 1']
        for hook in hooks:
            if hook in content_lower:
                viral_score += 2
                viral_factors.append(f"Strong engagement hook: {hook}")
        
        # Question format (viral)
        if '?' in tweet_content:
            viral_score += 1
            viral_factors.append("Question format increases engagement")
        
        # Thread format
        if any(f'tweet {i}' in content_lower for i in range(1, 6)):
            viral_score += 1
            viral_factors.append("Thread format detected")
        
        return {
            'viral_score': max(1, min(10, viral_score)),
            'viral_factors': viral_factors,
            'potential_level': 'high' if viral_score >= 7 else 'medium' if viral_score >= 5 else 'low'
        }
    
    def analyze_recent_posts(self, post_data_list):
        """Analyze recent posts for quality, duplicates, and viral potential"""
        analysis_results = []
        
        for i, post in enumerate(post_data_list):
            content = post.get('content', '')
            
            # Run all analyses
            quality_analysis = self.analyze_visual_quality(post.get('image_description', ''), content)
            duplicate_analysis = self.detect_duplicates(content, [p.get('content', '') for p in post_data_list[i+1:]])
            viral_analysis = self.assess_viral_potential(content)
            
            # Generate recommendations
            recommendations = self.generate_recommendations(quality_analysis, duplicate_analysis, viral_analysis)
            
            analysis_results.append({
                'post_index': i + 1,
                'content_preview': content[:100] + "...",
                'quality_analysis': quality_analysis,
                'duplicate_analysis': duplicate_analysis,
                'viral_analysis': viral_analysis,
                'recommendations': recommendations,
                'overall_score': (quality_analysis['quality_score'] + viral_analysis['viral_score']) / 2
            })
        
        return analysis_results
    
    def generate_recommendations(self, quality_analysis, duplicate_analysis, viral_analysis):
        """Generate specific improvement recommendations"""
        recommendations = []
        
        # Quality recommendations
        if quality_analysis['quality_score'] < 6:
            recommendations.append("🎨 VISUAL UPGRADE: Replace basic graphics with professional, eye-catching designs")
        
        if "blue gradient" in str(quality_analysis.get('issues', [])):
            recommendations.append("🌈 COLOR VARIETY: Try different color schemes - blues are overused")
        
        # Viral potential recommendations
        if viral_analysis['viral_score'] < 6:
            recommendations.append("📈 VIRAL BOOST: Add trending topics, stronger hooks, or question formats")
        
        # Duplicate recommendations
        if duplicate_analysis['is_duplicate']:
            recommendations.append("🔄 CONTENT FRESHNESS: Detected duplicates - create unique, varied content")
        
        # Strategic recommendations
        if not viral_analysis.get('viral_factors'):
            recommendations.append("🎯 ENGAGEMENT: Add hooks like 'Did you know', 'Reality check', or questions")
        
        return recommendations
    
    def generate_report(self, analysis_results):
        """Generate comprehensive analysis report"""
        report = {
            'timestamp': datetime.now().isoformat(),
            'total_posts_analyzed': len(analysis_results),
            'summary': {
                'avg_quality_score': sum(r['quality_analysis']['quality_score'] for r in analysis_results) / len(analysis_results),
                'avg_viral_score': sum(r['viral_analysis']['viral_score'] for r in analysis_results) / len(analysis_results),
                'duplicate_count': sum(1 for r in analysis_results if r['duplicate_analysis']['is_duplicate']),
                'low_quality_count': sum(1 for r in analysis_results if r['quality_analysis']['quality_score'] < 6)
            },
            'detailed_analysis': analysis_results
        }
        
        return report

def test_enhancer():
    """Test the visual enhancer with sample data"""
    enhancer = VisualEnhancer()
    
    # Test with your actual duplicate posts
    sample_posts = [
        {
            'content': 'AI REALITY CHECK THREAD: TWEET 1: Things AI can do: Write code, create art, analyze data',
            'image_description': 'blue gradient background with quote'
        },
        {
            'content': 'AI REALITY CHECK THREAD: TWEET 1: Things AI can do: Write code, create art, analyze data', 
            'image_description': 'blue gradient background with quote'
        }
    ]
    
    results = enhancer.analyze_recent_posts(sample_posts)
    report = enhancer.generate_report(results)
    
    print("🔍 VISUAL ENHANCEMENT TEST RESULTS:")
    print(f"📊 Average Quality Score: {report['summary']['avg_quality_score']:.1f}/10")
    print(f"📈 Average Viral Score: {report['summary']['avg_viral_score']:.1f}/10") 
    print(f"🔄 Duplicates Found: {report['summary']['duplicate_count']}")
    print(f"⚠️ Low Quality Posts: {report['summary']['low_quality_count']}")
    
    if results:
        print("\n💡 TOP RECOMMENDATIONS:")
        for rec in results[0]['recommendations']:
            print(f"   {rec}")

if __name__ == "__main__":
    test_enhancer()
