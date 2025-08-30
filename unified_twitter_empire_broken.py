#!/usr/bin/env python3
"""
Unified Twitter Empire Coordination System
Prevents API conflicts, coordinates all posting, respects rate limits
Integrates: Content → Visuals → CEO Strategy → Safe Posting
"""

import os
import json
import time
import random
import threading
from datetime import datetime, timedelta
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple
from twitter_safety_config import safe_twitter_post

@dataclass
class PostMetrics:
    """Track posting metrics and rate limits"""
    posts_last_3h: List[datetime]
    posts_today: int
    posts_this_month: int
    last_post_time: Optional[datetime]
    daily_reset: datetime
    monthly_reset: datetime

class RateLimitManager:
    """Manages all Twitter API rate limits"""
    
    def __init__(self):
        self.max_posts_3h = 250  # Conservative buffer under 300 limit
        self.max_posts_daily = 20  # Conservative for sustainable growth
        self.max_posts_monthly = 1400  # Buffer under 1500 limit
        self.min_interval_minutes = 45  # Minimum time between posts
        
    def can_post_now(self, metrics: PostMetrics) -> Tuple[bool, str]:
        """Check if we can post now without hitting limits"""
        now = datetime.now()
        
        # Check 3-hour window
        three_hours_ago = now - timedelta(hours=3)
        recent_posts = [p for p in metrics.posts_last_3h if p > three_hours_ago]
        
        if len(recent_posts) >= self.max_posts_3h:
            next_available = min(recent_posts) + timedelta(hours=3)
            return False, f"3-hour limit reached. Next available: {next_available.strftime('%H:%M')}"
        
        # Check daily limit
        if metrics.posts_today >= self.max_posts_daily:
            return False, f"Daily limit reached ({self.max_posts_daily}). Reset at midnight."
        
        # Check monthly limit
        if metrics.posts_this_month >= self.max_posts_monthly:
            return False, f"Monthly limit reached ({self.max_posts_monthly}). Wait for reset."
        
        # Check minimum interval
        if metrics.last_post_time:
            time_since_last = now - metrics.last_post_time
            min_interval = timedelta(minutes=self.min_interval_minutes)
            if time_since_last < min_interval:
                next_available = metrics.last_post_time + min_interval
                return False, f"Minimum interval not met. Next: {next_available.strftime('%H:%M')}"
        
        return True, "Ready to post"

class CEOStrategy:
    """Dynamic CEO decision making for content strategy"""
    
    def __init__(self):
        self.strategy_matrix = {
            'morning': {'type': 'educational', 'affiliate_chance': 0.15, 'viral_boost': 1.2},
            'afternoon': {'type': 'viral', 'affiliate_chance': 0.25, 'viral_boost': 1.5}, 
            'evening': {'type': 'promotional', 'affiliate_chance': 0.75, 'viral_boost': 0.8},
            'night': {'type': 'educational', 'affiliate_chance': 0.10, 'viral_boost': 1.0}
        }
        
        # Track recent posting patterns for optimization
        self.recent_patterns = []
        
    def get_current_strategy(self) -> Dict:
        """Get current strategy based on time and recent patterns"""
        hour = datetime.now().hour
        
        if 6 <= hour < 12:
            period = 'morning'
        elif 12 <= hour < 18:
            period = 'afternoon'
        elif 18 <= hour < 22:
            period = 'evening'
        else:
            period = 'night'
        
        strategy = self.strategy_matrix[period].copy()
        strategy['period'] = period
        strategy['timestamp'] = datetime.now().isoformat()
        
        # Adjust based on recent patterns (avoid oversaturation)
        recent_affiliates = sum(1 for p in self.recent_patterns[-5:] if p.get('had_affiliate'))
        if recent_affiliates >= 2:  # Too many recent affiliates
            strategy['affiliate_chance'] *= 0.5
            strategy['adjustment'] = 'reduced_affiliate_oversaturation'
        
        return strategy

class ContentGenerator:
    """Advanced content generation with viral optimization"""
    
    def __init__(self):
        self.viral_templates = {
            'educational': [
                "🧠 {hook} that most people miss:\n\n{content}\n\n{cta}",
                "⚡ 5 {topic} mistakes I see everywhere:\n\n{mistakes}\n\n💡 {solution}\n\n{cta}",
                "🚀 How I {achievement} in {timeframe}:\n\n{method}\n\n{result}\n\n{cta}",
                "📚 {number} {topic} secrets nobody talks about:\n\n{secrets}\n\n{cta}"
            ],
            'viral': [
                "🧵 THREAD: Unpopular {topic} opinion...\n\n{hook}\n\n{controversy}\n\n{cta}",
                "🔥 Everyone's doing {topic} wrong.\n\nHere's the right way:\n\n{content}\n\n{cta}",
                "💡 I tested {number} {tools} so you don't have to:\n\n{results}\n\n{winners}\n\n{cta}",
                "🚨 {topic} industry secret they don't want you to know:\n\n{secret}\n\n{proof}\n\n{cta}"
            ],
            'promotional': [
                "🎯 Ready to {goal}?\n\n{value_prop}\n\n📚 Start here: {affiliate_link}\n\n{social_proof}",
                "💰 {benefit} in {timeframe}?\n\n{method}\n\n🔗 Get the blueprint: {affiliate_link}\n\n{testimonial}",
                "🚀 {transformation} starts today:\n\n{steps}\n\n📖 Complete guide: {affiliate_link}\n\n{urgency}"
            ]
        }
        
        self.content_vars = {
            'hooks': [
                'The AI productivity secret', 'The automation hack', 'The revenue multiplier',
                'The efficiency breakthrough', 'The game-changing strategy'
            ],
            'topics': ['AI automation', 'productivity', 'revenue generation', 'business growth'],
            'achievements': ['10x my revenue', '5x my productivity', 'automated my business'],
            'timeframes': ['30 days', '60 days', '3 months'],
            'numbers': ['3', '5', '7', '10'],
            'tools': ['AI tools', 'automation tools', 'productivity apps'],
            'goals': ['master AI automation', '10x your income', 'build passive revenue'],
            'benefits': ['Generate $10K/month', 'Save 20 hours/week', 'Automate everything']
        }
    
    def generate_content(self, strategy: Dict) -> Dict:
        """Generate optimized content based on CEO strategy"""
        content_type = strategy['type']
        templates = self.viral_templates[content_type]
        template = random.choice(templates)
        
        # Fill template with dynamic content
        vars_dict = {}
        for var in ['hook', 'topic', 'achievement', 'timeframe', 'number', 'tools', 'goal', 'benefit']:
            if f'{{{var}}}' in template:
                vars_dict[var] = random.choice(self.content_vars.get(f'{var}s', [f'{var}_placeholder']))
        
        # Add specific content based on type
        if content_type == 'educational':
            vars_dict.update({
                'content': self._generate_educational_content(),
                'cta': '💭 What\'s your biggest automation challenge?',
                'solution': 'The solution: Start with one simple workflow',
                'method': '1. Identify repetitive tasks\n2. Choose the right AI tool\n3. Test and optimize',
                'result': 'Result: 15+ hours saved weekly'
            })
            
        elif content_type == 'viral':
            vars_dict.update({
                'hook': random.choice(self.content_vars['hooks']),
                'controversy': 'Most people waste hours on manual work...',
                'content': 'AI can automate 80% of your daily tasks',
                'cta': '🔄 Retweet if you agree!',
                'results': '✅ Tool A: Great for beginners\n❌ Tool B: Overhyped\n🔥 Tool C: Hidden gem',
                'winners': 'Top 3 that actually work ↓',
                'secret': 'The real money is in automation workflows, not individual tools',
                'proof': 'I\'ve tested this with 100+ entrepreneurs'
            })
            
        elif content_type == 'promotional':
            include_affiliate = random.random() < strategy['affiliate_chance']
            affiliate_link = 'https://amzn.to/wealthyrobot-ai-advantage' if include_affiliate else ''
            
            vars_dict.update({
                'value_prop': 'Learn the exact AI systems generating $50K+/month',
                'affiliate_link': affiliate_link,
                'social_proof': '10,000+ entrepreneurs already inside',
                'method': 'The 3-step AI profit system',
                'steps': '1. Pick profitable niche\n2. Automate content\n3. Scale with AI',
                'testimonial': '"Made $5K in first month" - Sarah K.',
                'urgency': 'Limited time: 50% off this week',
                'transformation': 'Your AI empire'
            })
        
        # Fill template
        try:
            filled_content = template.format(**vars_dict)
        except KeyError as e:
            # Fallback for missing variables
            filled_content = template.replace(f'{{{e.args[0]}}}', f'[{e.args[0]}]')
        
        return {
            'content': filled_content,
            'type': content_type,
            'has_affiliate': 'affiliate_link' in vars_dict and vars_dict['affiliate_link'],
            'length': len(filled_content),
            'viral_score': self._calculate_viral_score(filled_content),
            'strategy_used': strategy
        }
    
    def _generate_educational_content(self) -> str:
        """Generate educational content snippets"""
        tips = [
            'Use AI to write your emails while you sleep',
            'Automate social media posting across 5 platforms',
            'Generate passive income with AI content creation',
            'Build chatbots that handle customer service 24/7',
            'Create automated sales funnels with AI copywriting'
        ]
        return '\n\n'.join(random.sample(tips, 3))
    
    def _calculate_viral_score(self, content: str) -> float:
        """Calculate viral potential score"""
        score = 0.0
        
        # Emoji count (up to 5 points)
        emoji_count = len([c for c in content if c in '🧠⚡🚀💡🔥🎯💰📚🧵🔄✅❌📈💭🎨'])
        score += min(emoji_count * 0.5, 5.0)
        
        # Viral words (up to 3 points)
        viral_words = ['secret', 'hack', 'mistake', 'wrong', 'unpopular', 'nobody', 'hidden']
        for word in viral_words:
            if word.lower() in content.lower():
                score += 0.5
        
        # Structure elements (up to 2 points)
        if 'THREAD:' in content: score += 1.0
        if any(x in content for x in ['1.', '2.', '3.']): score += 0.5
        if any(x in content for x in ['✅', '❌', '🔥']): score += 0.5
        
        return min(score, 10.0)

class VisualCoordinator:
    """Coordinates visual content creation"""
    
    def __init__(self):
        self.visual_agents = {
            'infographic': 'python3 visual_affiliate_agent.py',
            'branded_graphic': 'python3 twitter_visual_enhancement.py',
            'stats_visual': 'python3 hybrid_visual_system.py'
        }
        
    def should_add_visual(self, content_data: Dict) -> bool:
        """Determine if content should have visual"""
        # 30% chance for educational, 50% for viral, 20% for promotional
        chances = {'educational': 0.3, 'viral': 0.5, 'promotional': 0.2}
        return random.random() < chances.get(content_data['type'], 0.3)
    
    def generate_visual(self, content_data: Dict) -> Optional[str]:
        """Generate visual if needed"""
        if not self.should_add_visual(content_data):
            return None
            
        visual_type = self._select_visual_type(content_data)
        # In practice, this would call the actual visual generation agents
        return f"visual_{visual_type}_{int(time.time())}.png"
    
    def _select_visual_type(self, content_data: Dict) -> str:
        """Select appropriate visual type"""
        if content_data['type'] == 'promotional':
            return 'branded_graphic'
        elif 'stats' in content_data['content'].lower():
            return 'stats_visual'
        else:
            return 'infographic'

class UnifiedTwitterEmpire:
    """Main coordination system"""
    
    def __init__(self):
        self.rate_manager = RateLimitManager()
        self.ceo = CEOStrategy()
        self.content_gen = ContentGenerator()
        self.visual_coord = VisualCoordinator()
        
        # Load or initialize metrics
        self.metrics = self._load_metrics()
        
        # Threading lock for coordination
        self.posting_lock = threading.Lock()
        
        # Log file
        self.log_file = 'unified_empire_log.json'
        
    def _load_metrics(self) -> PostMetrics:
        """Load metrics from disk"""
        try:
            if os.path.exists('empire_metrics.json'):
                with open('empire_metrics.json', 'r') as f:
                    data = json.load(f)
                    return PostMetrics(
                        posts_last_3h=[datetime.fromisoformat(p) for p in data['posts_last_3h']],
                        posts_today=data['posts_today'],
                        posts_this_month=data['posts_this_month'],
                        last_post_time=datetime.fromisoformat(data['last_post_time']) if data['last_post_time'] else None,
                        daily_reset=datetime.fromisoformat(data['daily_reset']),
                        monthly_reset=datetime.fromisoformat(data['monthly_reset'])
                    )
        except Exception as e:
            print(f"⚠️ Error loading metrics: {e}")
        
        # Default metrics
        now = datetime.now()
        return PostMetrics(
            posts_last_3h=[],
            posts_today=0,
            posts_this_month=0,
            last_post_time=None,
            daily_reset=now.replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=1),
            monthly_reset=now.replace(day=1, hour=0, minute=0, second=0, microsecond=0) + timedelta(days=32)
        )
    
    def _save_metrics(self):
        """Save metrics to disk"""
        data = {
            'posts_last_3h': [p.isoformat() for p in self.metrics.posts_last_3h],
            'posts_today': self.metrics.posts_today,
            'posts_this_month': self.metrics.posts_this_month,
            'last_post_time': self.metrics.last_post_time.isoformat() if self.metrics.last_post_time else None,
            'daily_reset': self.metrics.daily_reset.isoformat(),
            'monthly_reset': self.metrics.monthly_reset.isoformat()
        }
        
        with open('empire_metrics.json', 'w') as f:
            json.dump(data, f, indent=2)
    
    def _reset_metrics_if_needed(self):
        """Reset daily/monthly metrics if needed"""
        now = datetime.now()
        
        if now >= self.metrics.daily_reset:
            self.metrics.posts_today = 0
            self.metrics.daily_reset = now.replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=1)
            print("📅 Daily metrics reset")
        
        if now >= self.metrics.monthly_reset:
            self.metrics.posts_this_month = 0
            next_month = now.replace(day=1) + timedelta(days=32)
            self.metrics.monthly_reset = next_month.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            print("📅 Monthly metrics reset")
    
    def attempt_post(self) -> Dict:
        """Main posting orchestration method"""
        with self.posting_lock:
            print("🎛️ UNIFIED EMPIRE POSTING ATTEMPT")
            print("=" * 40)
            
            # Reset metrics if needed
            self._reset_metrics_if_needed()
            
            # Check rate limits
            can_post, reason = self.rate_manager.can_post_now(self.metrics)
            if not can_post:
                result = {
                    'success': False,
                    'reason': reason,
                    'timestamp': datetime.now().isoformat(),
                    'action': 'rate_limited'
                }
                print(f"🛑 {reason}")
                self._log_result(result)
                return result
            
            try:
                # Get CEO strategy
                strategy = self.ceo.get_current_strategy()
                print(f"🎯 CEO Strategy: {strategy['type']} ({strategy['period']}) - Affiliate: {strategy['affiliate_chance']*100:.0f}%")
                
                # Generate content
                content_data = self.content_gen.generate_content(strategy)
                print(f"📝 Content: {content_data['length']} chars, viral score: {content_data['viral_score']:.1f}")
                
                # Generate visual if needed
                visual_path = self.visual_coord.generate_visual(content_data)
                if visual_path:
                    print(f"🎨 Visual: {visual_path}")
                
                # Post safely
                # Check function signature
                try:
                    import inspect
                    sig = inspect.signature(safe_twitter_post)
                    if 'image_path' in sig.parameters:
                        tweet_result = safe_twitter_post(
                    content=content_data['content'],
                    image_path=visual_path
                )
                
                if tweet_result.get('success'):
                    # Update metrics
                    now = datetime.now()
                    self.metrics.posts_last_3h.append(now)
                    self.metrics.posts_today += 1
                    self.metrics.posts_this_month += 1
                    self.metrics.last_post_time = now
                    
                    # Clean old 3h posts
                    three_hours_ago = now - timedelta(hours=3)
                    self.metrics.posts_last_3h = [p for p in self.metrics.posts_last_3h if p > three_hours_ago]
                    
                    # Update CEO patterns
                    self.ceo.recent_patterns.append({
                        'timestamp': now,
                        'type': content_data['type'],
                        'had_affiliate': content_data['has_affiliate'],
                        'viral_score': content_data['viral_score']
                    })
                    
                    # Keep only recent patterns
                    if len(self.ceo.recent_patterns) > 10:
                        self.ceo.recent_patterns = self.ceo.recent_patterns[-10:]
                    
                    # Save metrics
                    self._save_metrics()
                    
                    result = {
                        'success': True,
                        'tweet_id': tweet_result.get('tweet_id'),
                        'content_type': content_data['type'],
                        'has_affiliate': content_data['has_affiliate'],
                        'viral_score': content_data['viral_score'],
                        'has_visual': visual_path is not None,
                        'posts_today': self.metrics.posts_today,
                        'posts_this_month': self.metrics.posts_this_month,
                        'timestamp': now.isoformat(),
                        'strategy': strategy
                    }
                    
                    print(f"✅ SUCCESS! Tweet ID: {tweet_result.get('tweet_id')}")
                    print(f"📊 Posts today: {self.metrics.posts_today}, this month: {self.metrics.posts_this_month}")
                    
                else:
                    result = {
                        'success': False,
                        'reason': tweet_result.get('error', 'Unknown posting error'),
                        'timestamp': datetime.now().isoformat(),
                        'action': 'post_failed'
                    }
                    print(f"❌ Post failed: {result['reason']}")
                
                self._log_result(result)
                return result
                
            except Exception as e:
                result = {
                    'success': False,
                    'reason': f'System error: {str(e)}',
                    'timestamp': datetime.now().isoformat(),
                    'action': 'system_error'
                }
                print(f"💥 System error: {e}")
                self._log_result(result)
                return result
    
    def _log_result(self, result: Dict):
        """Log result to file"""
        try:
            # Load existing logs
            logs = []
            if os.path.exists(self.log_file):
                with open(self.log_file, 'r') as f:
                    logs = json.load(f)
            
            # Add new result
            logs.append(result)
            
            # Keep only recent logs (last 100)
            if len(logs) > 100:
                logs = logs[-100:]
            
            # Save logs
            with open(self.log_file, 'w') as f:
                json.dump(logs, f, indent=2)
                
        except Exception as e:
            print(f"⚠️ Logging error: {e}")
    
    def get_status(self) -> Dict:
        """Get current empire status"""
        self._reset_metrics_if_needed()
        can_post, reason = self.rate_manager.can_post_now(self.metrics)
        
        return {
            'can_post': can_post,
            'reason': reason,
            'posts_today': self.metrics.posts_today,
            'posts_this_month': self.metrics.posts_this_month,
            'last_post': self.metrics.last_post_time.isoformat() if self.metrics.last_post_time else None,
            'next_reset': self.metrics.daily_reset.isoformat()
        }

def main():
    """Main execution"""
    empire = UnifiedTwitterEmpire()
    
    print("🏰 UNIFIED TWITTER EMPIRE STARTING")
    print("=" * 40)
    
    # Show current status
    status = empire.get_status()
    print(f"📊 Current Status:")
    print(f"   Can post: {'✅' if status['can_post'] else '❌'}")
    print(f"   Reason: {status['reason']}")
    print(f"   Posts today: {status['posts_today']}")
    print(f"   Posts this month: {status['posts_this_month']}")
    print()
    
    # Attempt to post
    result = empire.attempt_post()
    
    print("\n🎯 Final Status:")
    if result['success']:
        print(f"✅ Posted successfully: {result['tweet_id']}")
    else:
        print(f"❌ Failed: {result['reason']}")

if __name__ == "__main__":
    main()
