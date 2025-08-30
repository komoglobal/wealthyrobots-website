print("🤖 Running your complete autonomous workforce...")

# Import and run all available agents
available_agents = []

try:
    from market_research_agent import MarketResearchAgent
    available_agents.append(("Market Research", MarketResearchAgent()))
    print("✅ Market Research Agent loaded")
except:
    print("❌ Market Research Agent not available")

try:
    from competitor_analysis_agent import CompetitorAnalysisAgent
    available_agents.append(("Competitor Analysis", CompetitorAnalysisAgent()))
    print("✅ Competitor Analysis Agent loaded")
except:
    print("❌ Competitor Analysis Agent not available")

try:
    from content_optimizer_agent import ContentOptimizerAgent
    available_agents.append(("Content Optimizer", ContentOptimizerAgent()))
    print("✅ Content Optimizer Agent loaded")
except:
    print("❌ Content Optimizer Agent not available")

try:
    from data_analytics_agent import DataAnalyticsAgent
    available_agents.append(("Data Analytics", DataAnalyticsAgent()))
    print("✅ Data Analytics Agent loaded")
except:
    print("❌ Data Analytics Agent not available")

try:
    from email_marketing_agent import EmailMarketingAgent
    available_agents.append(("Email Marketing", EmailMarketingAgent()))
    print("✅ Email Marketing Agent loaded")
except:
    print("❌ Email Marketing Agent not available")

try:
    from seo_content_agent import SEOContentAgent
    available_agents.append(("SEO Content", SEOContentAgent()))
    print("✅ SEO Content Agent loaded")
except:
    print("❌ SEO Content Agent not available")

print(f"\n🎯 Found {len(available_agents)} working agents")

results = []

for name, agent in available_agents:
    print(f"\n🚀 Running {name} Agent...")
    try:
        result = agent.run_cycle()
        status = result.get('status', 'completed')
        results.append(f"✅ {name}: {status}")
        
        # Show filename if available
        if 'filename' in result:
            print(f"   📄 Generated: {result['filename']}")
            
    except Exception as e:
        results.append(f"❌ {name}: error - {str(e)[:50]}...")
        print(f"   Error: {e}")

print("\n" + "="*60)
print("🏆 AUTONOMOUS WORKFORCE RESULTS:")
print("="*60)
for result in results:
    print(result)

print(f"\n📊 Total agents in your empire: {len(available_agents)}")
print("👑 Your autonomous business empire is generating value!")

# Show generated files
import os
print(f"\n📁 Files generated this session:")
txt_files = [f for f in os.listdir('.') if (f.endswith('.txt') or f.endswith('.md')) and '20250801' in f]
for file in sorted(txt_files):
    size = os.path.getsize(file)
    print(f"   📄 {file} ({size} bytes)")

print(f"\n💰 Total business intelligence generated: {len(txt_files)} reports")
