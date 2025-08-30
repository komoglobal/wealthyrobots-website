#!/usr/bin/env python3
import asyncio
import json
from UNIFIED_AGI_SYSTEM import UnifiedAGISystem
from REAL_AGI_HOW_EXECUTION_ENGINE import real_how_engine


async def main():
    await real_how_engine.initialize()
    u = UnifiedAGISystem()

    insights = await u._generate_agi_insights()
    print(json.dumps({
        'insights_count': len(insights),
        'insight_summaries': [i.get('summary') for i in insights]
    }, indent=2))

    if insights:
        result = await u._implement_agi_insights(insights)
        print(json.dumps({'implementation_status': result.get('status'), 'executed': len(result.get('execution_results', []))}, indent=2))
    else:
        print(json.dumps({'implementation_status': 'no_insights'}, indent=2))


if __name__ == '__main__':
    asyncio.run(main())


