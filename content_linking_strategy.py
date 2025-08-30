#!/usr/bin/env python3
"""
Content Linking Strategy - WealthyRobot Empire
Creates comprehensive internal linking between articles for better SEO and user experience
"""

import os
import json
import re
from datetime import datetime
from typing import Dict, List, Any, Tuple, Optional
from dataclasses import dataclass
from collections import defaultdict
import string

@dataclass
class Article:
    """Represents an article with its metadata"""
    filename: str
    title: str
    content: str
    keywords: List[str]
    url: str
    word_count: int
    topics: List[str]
    publish_date: Optional[datetime] = None

@dataclass
class LinkRecommendation:
    """Represents a recommended internal link"""
    from_article: str
    to_article: str
    anchor_text: str
    relevance_score: float
    context: str
    position_suggestion: str

class ContentLinkingStrategy:
    """Creates intelligent internal linking strategy for articles"""

    def __init__(self):
        self.articles_dir = "wealthyrobots_website/articles"
        self.strategy_file = "content_linking_strategy.json"
        self.min_relevance_score = 0.3
        self.max_links_per_article = 5

        # Simple stop words list (no NLTK dependency)
        self.stop_words = {
            'a', 'an', 'and', 'are', 'as', 'at', 'be', 'by', 'for', 'from',
            'has', 'he', 'in', 'is', 'it', 'its', 'of', 'on', 'that', 'the',
            'to', 'was', 'will', 'with', 'but', 'or', 'not', 'this', 'these',
            'those', 'i', 'you', 'we', 'they', 'me', 'him', 'her', 'us', 'them',
            'my', 'your', 'our', 'his', 'their', 'what', 'which', 'who', 'when',
            'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more',
            'most', 'other', 'some', 'such', 'no', 'nor', 'only', 'own', 'same',
            'so', 'than', 'too', 'very'
        }

    def analyze_content_inventory(self) -> List[Article]:
        """Analyze all articles and extract metadata"""
        print("📊 ANALYZING CONTENT INVENTORY")
        print("=" * 40)

        articles = []

        if not os.path.exists(self.articles_dir):
            print(f"❌ Articles directory not found: {self.articles_dir}")
            return articles

        for filename in os.listdir(self.articles_dir):
            if not filename.endswith('.html'):
                continue

            filepath = os.path.join(self.articles_dir, filename)
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()

                article = self._extract_article_metadata(filename, content)
                if article:
                    articles.append(article)
                    print(f"✅ Analyzed: {filename} ({article.word_count} words)")

            except Exception as e:
                print(f"⚠️ Error analyzing {filename}: {e}")

        print(f"📈 Total articles analyzed: {len(articles)}")
        return articles

    def _extract_article_metadata(self, filename: str, content: str) -> Optional[Article]:
        """Extract metadata from article content"""
        try:
            # Extract title
            title_match = re.search(r'<title[^>]*>([^<]+)</title>', content, re.IGNORECASE)
            title = title_match.group(1) if title_match else filename.replace('.html', '').replace('_', ' ').title()

            # Extract meta description for keywords
            desc_match = re.search(r'<meta[^>]*description[^>]*content="([^"]+)"', content, re.IGNORECASE)
            description = desc_match.group(1) if desc_match else ""

            # Clean content for analysis
            clean_content = re.sub(r'<[^>]+>', ' ', content)  # Remove HTML tags
            clean_content = re.sub(r'\s+', ' ', clean_content).strip()

            # Extract keywords from title, description, and content
            keywords = self._extract_keywords(title + " " + description + " " + clean_content[:1000])

            # Create URL
            url = f"/articles/{filename}"

            # Word count
            word_count = len(clean_content.split())

            # Extract topics
            topics = self._categorize_topics(keywords)

            return Article(
                filename=filename,
                title=title,
                content=clean_content,
                keywords=keywords,
                url=url,
                word_count=word_count,
                topics=topics
            )

        except Exception as e:
            print(f"❌ Error extracting metadata from {filename}: {e}")
            return None

    def _extract_keywords(self, text: str) -> List[str]:
        """Extract relevant keywords from text"""
        # Simple tokenization using regex
        words = re.findall(r'\b\w+\b', text.lower())

        # Filter words
        tokens = []
        for word in words:
            if word not in self.stop_words and len(word) > 2 and word not in string.punctuation:
                tokens.append(word)

        # Get word frequency
        word_freq = defaultdict(int)
        for token in tokens:
            word_freq[token] += 1

        # Extract top keywords
        keywords = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
        return [word for word, freq in keywords[:10]]  # Top 10 keywords

    def _categorize_topics(self, keywords: List[str]) -> List[str]:
        """Categorize content into topics"""
        topics = []

        # Define topic keywords
        topic_definitions = {
            "AI Automation": ["ai", "automation", "artificial", "intelligence", "machine", "learning"],
            "Business Strategy": ["business", "strategy", "entrepreneur", "startup", "growth", "revenue"],
            "Passive Income": ["passive", "income", "revenue", "monetization", "affiliate", "money"],
            "Content Marketing": ["content", "marketing", "seo", "blog", "article", "writing"],
            "Technology": ["technology", "software", "tool", "platform", "system", "digital"],
            "Finance": ["finance", "trading", "investment", "wealth", "profit", "money"]
        }

        for topic, topic_keywords in topic_definitions.items():
            if any(keyword in " ".join(keywords) for keyword in topic_keywords):
                topics.append(topic)

        return topics[:3]  # Max 3 topics per article

    def generate_linking_strategy(self, articles: List[Article]) -> Dict[str, Any]:
        """Generate comprehensive internal linking strategy"""
        print("🔗 GENERATING INTERNAL LINKING STRATEGY")
        print("=" * 45)

        strategy = {
            "timestamp": datetime.now().isoformat(),
            "total_articles": len(articles),
            "linking_opportunities": [],
            "topic_clusters": {},
            "pillar_content": [],
            "orphan_articles": []
        }

        # Create topic clusters
        topic_clusters = defaultdict(list)
        for article in articles:
            for topic in article.topics:
                topic_clusters[topic].append(article)

        strategy["topic_clusters"] = dict(topic_clusters)

        # Identify pillar content (longest articles in each topic)
        for topic, topic_articles in topic_clusters.items():
            if topic_articles:
                pillar = max(topic_articles, key=lambda x: x.word_count)
                strategy["pillar_content"].append({
                    "topic": topic,
                    "pillar_article": pillar.filename,
                    "word_count": pillar.word_count,
                    "title": pillar.title
                })

        # Generate link recommendations
        all_recommendations = []

        for i, article in enumerate(articles):
            recommendations = self._generate_article_links(article, articles, topic_clusters)
            all_recommendations.extend(recommendations)

            # Progress indicator
            if (i + 1) % 10 == 0:
                print(f"📊 Processed {i + 1}/{len(articles)} articles")

        # Filter and rank recommendations
        filtered_recommendations = [
            rec for rec in all_recommendations
            if rec.relevance_score >= self.min_relevance_score
        ]

        # Group by source article
        recommendations_by_article = defaultdict(list)
        for rec in filtered_recommendations:
            recommendations_by_article[rec.from_article].append({
                "to_article": rec.to_article,
                "anchor_text": rec.anchor_text,
                "relevance_score": rec.relevance_score,
                "context": rec.context,
                "position_suggestion": rec.position_suggestion
            })

        # Limit links per article
        for article_filename, links in recommendations_by_article.items():
            recommendations_by_article[article_filename] = sorted(
                links, key=lambda x: x["relevance_score"], reverse=True
            )[:self.max_links_per_article]

        strategy["linking_opportunities"] = dict(recommendations_by_article)

        # Identify orphan articles (articles with no incoming links)
        linked_articles = set()
        for rec in filtered_recommendations:
            linked_articles.add(rec.to_article)

        all_articles = {article.filename for article in articles}
        orphan_articles = all_articles - linked_articles
        strategy["orphan_articles"] = list(orphan_articles)

        print(f"🎯 Generated {len(filtered_recommendations)} linking opportunities")
        print(f"📊 Topic clusters: {len(topic_clusters)}")
        print(f"🏛️ Pillar content: {len(strategy['pillar_content'])}")
        print(f"👻 Orphan articles: {len(strategy['orphan_articles'])}")

        return strategy

    def _generate_article_links(self, source_article: Article, all_articles: List[Article],
                               topic_clusters: Dict[str, List[Article]]) -> List[LinkRecommendation]:
        """Generate link recommendations for a single article"""
        recommendations = []

        # Link to pillar content in same topics
        for topic in source_article.topics:
            if topic in topic_clusters:
                pillar_candidates = [
                    article for article in topic_clusters[topic]
                    if article != source_article and article.word_count > 1500
                ]

                for pillar in pillar_candidates[:2]:  # Max 2 pillar links per topic
                    relevance_score = self._calculate_relevance_score(source_article, pillar)

                    if relevance_score >= self.min_relevance_score:
                        recommendations.append(LinkRecommendation(
                            from_article=source_article.filename,
                            to_article=pillar.filename,
                            anchor_text=f"Learn more about {topic.lower()}",
                            relevance_score=relevance_score,
                            context=f"Related {topic.lower()} content",
                            position_suggestion="middle"
                        ))

        # Link to related content based on keywords
        for target_article in all_articles:
            if target_article == source_article:
                continue

            relevance_score = self._calculate_relevance_score(source_article, target_article)

            if relevance_score >= self.min_relevance_score:
                # Generate contextual anchor text
                anchor_text = self._generate_anchor_text(source_article, target_article)

                recommendations.append(LinkRecommendation(
                    from_article=source_article.filename,
                    to_article=target_article.filename,
                    anchor_text=anchor_text,
                    relevance_score=relevance_score,
                    context="Keyword-based relevance",
                    position_suggestion="end"
                ))

        return recommendations

    def _calculate_relevance_score(self, source: Article, target: Article) -> float:
        """Calculate relevance score between two articles"""
        # Keyword overlap
        source_keywords = set(source.keywords)
        target_keywords = set(target.keywords)
        keyword_overlap = len(source_keywords.intersection(target_keywords))

        # Topic overlap
        source_topics = set(source.topics)
        target_topics = set(target.topics)
        topic_overlap = len(source_topics.intersection(target_topics))

        # Content similarity (simple word overlap)
        source_words = set(source.content.lower().split()[:100])  # First 100 words
        target_words = set(target.content.lower().split()[:100])
        content_overlap = len(source_words.intersection(target_words))

        # Calculate weighted score
        score = (
            keyword_overlap * 0.4 +
            topic_overlap * 0.3 +
            content_overlap * 0.1 +
            (1.0 if source.publish_date and target.publish_date and
             abs((source.publish_date - target.publish_date).days) < 30 else 0.0) * 0.2
        )

        return min(score, 1.0)  # Cap at 1.0

    def _generate_anchor_text(self, source: Article, target: Article) -> str:
        """Generate contextual anchor text for linking"""
        # Find common keywords
        common_keywords = set(source.keywords).intersection(set(target.keywords))

        if common_keywords:
            keyword = list(common_keywords)[0]
            return f"learn more about {keyword}"

        # Use target article title keywords
        title_words = target.title.lower().split()[:3]
        return f"read about {' '.join(title_words)}"

    def implement_linking_strategy(self, strategy: Dict[str, Any], apply_changes: bool = False) -> Dict[str, Any]:
        """Implement the linking strategy by modifying articles"""
        print("🔧 IMPLEMENTING LINKING STRATEGY")
        print("=" * 35)

        implementation_results = {
            "timestamp": datetime.now().isoformat(),
            "articles_modified": 0,
            "links_added": 0,
            "errors": [],
            "applied_changes": apply_changes
        }

        linking_opportunities = strategy.get("linking_opportunities", {})

        for article_filename, links in linking_opportunities.items():
            try:
                article_path = os.path.join(self.articles_dir, article_filename)

                if not os.path.exists(article_path):
                    implementation_results["errors"].append(f"Article not found: {article_filename}")
                    continue

                with open(article_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                links_added = 0

                for link in links:
                    # Generate HTML link
                    link_html = f'<a href="{link["to_article"]}">{link["anchor_text"]}</a>'

                    if link["position_suggestion"] == "middle":
                        # Insert in middle of content
                        content_parts = content.split('</p>')
                        if len(content_parts) > 2:
                            insert_position = len(content_parts) // 2
                            content_parts.insert(insert_position, f'<p>{link_html}</p>')
                            content = '</p>'.join(content_parts)
                            links_added += 1

                    elif link["position_suggestion"] == "end":
                        # Add at the end
                        if '</article>' in content:
                            content = content.replace('</article>', f'<p>{link_html}</p></article>')
                            links_added += 1

                if links_added > 0 and apply_changes:
                    with open(article_path, 'w', encoding='utf-8') as f:
                        f.write(content)

                    implementation_results["articles_modified"] += 1
                    implementation_results["links_added"] += links_added
                    print(f"✅ Updated {article_filename}: added {links_added} links")

                elif links_added > 0 and not apply_changes:
                    print(f"📝 Would update {article_filename}: add {links_added} links")

            except Exception as e:
                error_msg = f"Error updating {article_filename}: {str(e)}"
                implementation_results["errors"].append(error_msg)
                print(f"❌ {error_msg}")

        return implementation_results

    def save_strategy(self, strategy: Dict[str, Any], filename: str = None):
        """Save the linking strategy to file"""
        if filename is None:
            filename = self.strategy_file

        with open(filename, 'w') as f:
            json.dump(strategy, f, indent=2, default=str)

        print(f"💾 Strategy saved to: {filename}")

    def get_strategy_summary(self, strategy: Dict[str, Any]) -> Dict[str, Any]:
        """Get a summary of the linking strategy"""
        return {
            "total_articles": strategy.get("total_articles", 0),
            "topic_clusters": len(strategy.get("topic_clusters", {})),
            "pillar_content": len(strategy.get("pillar_content", [])),
            "linking_opportunities": sum(len(links) for links in strategy.get("linking_opportunities", {}).values()),
            "orphan_articles": len(strategy.get("orphan_articles", [])),
            "generated_at": strategy.get("timestamp")
        }

# Convenience functions
def analyze_content_and_create_strategy(apply_changes: bool = False):
    """Complete workflow: analyze content and create linking strategy"""
    strategy_system = ContentLinkingStrategy()

    # Analyze content
    articles = strategy_system.analyze_content_inventory()

    if not articles:
        print("❌ No articles found to analyze")
        return None

    # Generate strategy
    strategy = strategy_system.generate_linking_strategy(articles)

    # Save strategy
    strategy_system.save_strategy(strategy)

    # Implement strategy (optionally)
    if apply_changes:
        results = strategy_system.implement_linking_strategy(strategy, apply_changes=True)
        print(f"🔧 Implementation results: {results}")

    # Show summary
    summary = strategy_system.get_strategy_summary(strategy)
    print("\n📊 STRATEGY SUMMARY:")
    print(f"   Total articles: {summary['total_articles']}")
    print(f"   Topic clusters: {summary['topic_clusters']}")
    print(f"   Pillar content: {summary['pillar_content']}")
    print(f"   Linking opportunities: {summary['linking_opportunities']}")
    print(f"   Orphan articles: {summary['orphan_articles']}")

    return strategy

if __name__ == "__main__":
    print("🧪 Testing Content Linking Strategy")
    print("=" * 40)

    # Run complete analysis
    strategy = analyze_content_and_create_strategy(apply_changes=False)

    if strategy:
        print("\n✅ Content linking strategy generated successfully!")
    else:
        print("\n❌ Failed to generate content linking strategy")
