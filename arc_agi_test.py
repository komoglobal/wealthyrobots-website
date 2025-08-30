#!/usr/bin/env python3
"""
🧩 ARC-AGI BENCHMARK TEST
=========================

Tests AGI system on the Abstraction and Reasoning Corpus (ARC) benchmark.
This evaluates the system's ability to solve abstract visual reasoning puzzles
that require pattern recognition, logical reasoning, and generalization.

The ARC dataset contains 800+ puzzles designed to test AGI capabilities in:
- Pattern recognition and completion
- Spatial reasoning
- Object manipulation
- Rule inference
- Generalization to novel situations

Official ARC Challenge: https://arcprize.org/
"""

import asyncio
import sys
import os
import json
import requests
import random
from datetime import datetime
from typing import Dict, List, Any, Tuple, Optional
from pathlib import Path

# Add the current directory to the path
sys.path.append('/home/ubuntu/wealthyrobot')

# Import your AGI system
try:
    from UNRESTRICTED_AGI_SYSTEM import UnrestrictedAGISystem
except ImportError:
    try:
        from comprehensive_agi_system_test import ComprehensiveAGITest
    except ImportError:
        print("❌ Could not import AGI system. Please ensure your AGI system is properly set up.")
        sys.exit(1)

class ARCAGITest:
    """🧩 ARC-AGI Benchmark Test Implementation"""

    def __init__(self):
        self.agi_system = None
        self.test_results = {}
        self.arc_data = {}
        self.puzzle_solutions = {}
        self.test_start_time = None
        self.test_end_time = None

        # ARC dataset URLs
        self.arc_urls = {
            'training': 'https://arcprize.org/data/training.json',
            'evaluation': 'https://arcprize.org/data/evaluation.json',
            'test': 'https://arcprize.org/data/test.json'
        }

    async def initialize_agi_system(self) -> bool:
        """Initialize the AGI system for testing"""
        try:
            print("🚀 Initializing AGI System for ARC Testing...")
            self.agi_system = UnrestrictedAGISystem()
            print("✅ AGI System ready for ARC evaluation!")

            # Check available methods
            available_methods = [method for method in dir(self.agi_system) if not method.startswith('_')]
            print(f"🔍 Available AGI methods: {len(available_methods)}")
            key_methods = [m for m in available_methods if 'process' in m.lower() or 'run' in m.lower() or 'reason' in m.lower()]
            if key_methods:
                print(f"🎯 Key processing methods: {', '.join(key_methods[:5])}")

            return True
        except Exception as e:
            print(f"❌ Failed to initialize AGI system: {e}")
            return False

    def download_arc_data(self) -> bool:
        """Download ARC dataset from official source"""
        try:
            print("📥 Downloading ARC dataset...")

            for dataset_name, url in self.arc_urls.items():
                print(f"   Downloading {dataset_name} dataset...")
                response = requests.get(url, timeout=30)

                if response.status_code == 200:
                    self.arc_data[dataset_name] = response.json()
                    print(f"   ✅ Downloaded {len(self.arc_data[dataset_name])} {dataset_name} puzzles")
                else:
                    print(f"   ❌ Failed to download {dataset_name}: HTTP {response.status_code}")
                    return False

            print(f"📊 Total ARC puzzles loaded: {sum(len(puzzles) for puzzles in self.arc_data.values())}")
            return True

        except Exception as e:
            print(f"❌ Error downloading ARC data: {e}")
            return False

    def create_sample_arc_puzzles(self) -> Dict[str, Any]:
        """Create sample ARC-style puzzles for testing when download fails"""
        print("🎨 Creating sample ARC puzzles for testing...")

        # Simple pattern completion puzzle
        puzzle_1 = {
            "train": [
                {
                    "input": [[0, 1, 0], [1, 0, 1], [0, 1, 0]],
                    "output": [[0, 1, 0, 1], [1, 0, 1, 0], [0, 1, 0, 1], [1, 0, 1, 0]]
                }
            ],
            "test": [
                {
                    "input": [[1, 0, 1], [0, 1, 0], [1, 0, 1]]
                }
            ]
        }

        # Symmetry puzzle
        puzzle_2 = {
            "train": [
                {
                    "input": [[1, 0, 0], [0, 1, 0], [0, 0, 1]],
                    "output": [[1, 0, 0, 0, 1], [0, 1, 0, 1, 0], [0, 0, 1, 0, 0]]
                }
            ],
            "test": [
                {
                    "input": [[0, 1, 0], [1, 0, 1], [0, 1, 0]]
                }
            ]
        }

        # Color transformation puzzle
        puzzle_3 = {
            "train": [
                {
                    "input": [[1, 1, 2], [2, 2, 1], [1, 2, 1]],
                    "output": [[3, 3, 4], [4, 4, 3], [3, 4, 3]]
                }
            ],
            "test": [
                {
                    "input": [[2, 2, 1], [1, 1, 2], [2, 1, 2]]
                }
            ]
        }

        sample_puzzles = {
            "sample_puzzle_1": puzzle_1,
            "sample_puzzle_2": puzzle_2,
            "sample_puzzle_3": puzzle_3
        }

        print(f"   ✅ Created {len(sample_puzzles)} sample puzzles")
        return sample_puzzles

    def format_puzzle_for_agi(self, puzzle_data: Dict[str, Any], puzzle_id: str) -> str:
        """Format ARC puzzle for AGI system consumption"""
        prompt = f"""
🧩 ARC PUZZLE ANALYSIS: {puzzle_id}
====================================

You are presented with an abstract reasoning puzzle from the ARC (Abstraction and Reasoning Corpus) dataset.
Your task is to analyze the training examples and determine the pattern or rule that transforms the input grid into the output grid.

TRAINING EXAMPLES:
"""

        for i, example in enumerate(puzzle_data.get("train", [])):
            prompt += f"""
Example {i+1}:
Input Grid:
{self.grid_to_text(example["input"])}

Output Grid:
{self.grid_to_text(example["output"])}

Rule: [Please identify the transformation rule]
"""

        # Add test case
        test_input = puzzle_data.get("test", [{}])[0].get("input", [])
        prompt += f"""

TEST CASE:
Input Grid:
{self.grid_to_text(test_input)}

INSTRUCTIONS:
1. Analyze the training examples to identify the pattern/transformation rule
2. Apply this rule to the test input to generate the expected output
3. Provide your solution as a grid in the same format as the training outputs
4. Explain your reasoning step by step

Your response should include:
- The identified pattern/rule
- Step-by-step reasoning
- The predicted output grid
"""

        return prompt

    def grid_to_text(self, grid: List[List[int]]) -> str:
        """Convert grid to readable text format"""
        if not grid:
            return "[Empty Grid]"

        text = ""
        color_map = {
            0: "⬛",  # Black/Empty
            1: "🔴",  # Red
            2: "🔵",  # Blue
            3: "🟡",  # Yellow
            4: "🟢",  # Green
            5: "🟣",  # Purple
            6: "🟠",  # Orange
            7: "⚪",  # White
            8: "🟤",  # Brown
            9: "⚫"   # Gray
        }

        for row in grid:
            for cell in row:
                text += color_map.get(cell, str(cell))
            text += "\n"

        return text

    async def test_puzzle(self, puzzle_id: str, puzzle_data: Dict[str, Any]) -> Dict[str, Any]:
        """Test AGI system on a single ARC puzzle"""
        print(f"🧩 Testing puzzle: {puzzle_id}")

        try:
            # Format puzzle for AGI
            puzzle_prompt = self.format_puzzle_for_agi(puzzle_data, puzzle_id)

            # Send to AGI system
            print("   🤔 AGI analyzing puzzle...")

            # Use your AGI system's reasoning capabilities
            if hasattr(self.agi_system, 'run_unrestricted_intelligence_cycle'):
                # Create a processing context for the puzzle
                processing_context = {
                    "task_type": "abstract_reasoning",
                    "puzzle_data": puzzle_data,
                    "puzzle_prompt": puzzle_prompt,
                    "input_modalities": ["text"],
                    "processing_requirements": {
                        "reasoning_depth": "deep",
                        "creativity_required": True,
                        "pattern_recognition": True
                    }
                }

                # Run intelligence cycle with puzzle context
                result = await self.agi_system.run_unrestricted_intelligence_cycle()

                # Format result with puzzle context
                result = f"AGI Analysis Result:\n{result}\n\nPuzzle Context: {puzzle_prompt[:500]}..."

            elif hasattr(self.agi_system, 'process_multimodal_input'):
                # Use multimodal processing for puzzle analysis
                multimodal_input = {
                    "text": puzzle_prompt,
                    "task": "pattern_reasoning",
                    "expected_output": "grid_solution"
                }
                result = await self.agi_system.process_multimodal_input(multimodal_input)

            else:
                # Fallback: basic processing
                result = f"AGI System initialized but no suitable processing method found for puzzle: {puzzle_id}"

            # Evaluate result
            evaluation = self.evaluate_puzzle_solution(result, puzzle_data)

            return {
                "puzzle_id": puzzle_id,
                "solved": evaluation["correct"],
                "confidence": evaluation["confidence"],
                "reasoning_quality": evaluation["reasoning_quality"],
                "agi_response": result,
                "evaluation": evaluation
            }

        except Exception as e:
            print(f"   ❌ Error testing puzzle {puzzle_id}: {e}")
            return {
                "puzzle_id": puzzle_id,
                "solved": False,
                "error": str(e),
                "confidence": 0.0,
                "reasoning_quality": 0.0
            }

    def evaluate_puzzle_solution(self, agi_response: str, puzzle_data: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluate AGI's solution against expected output"""
        try:
            expected_output = puzzle_data.get("test", [{}])[0].get("output")

            if not expected_output:
                return {
                    "correct": False,
                    "confidence": 0.5,
                    "reasoning_quality": 0.3,
                    "reasoning": "No expected output available for evaluation"
                }

            # Parse AGI response for grid pattern
            predicted_grid = self.extract_grid_from_response(agi_response)

            if not predicted_grid:
                return {
                    "correct": False,
                    "confidence": 0.2,
                    "reasoning_quality": 0.1,
                    "reasoning": "Could not extract grid from AGI response"
                }

            # Compare grids
            correct = self.compare_grids(predicted_grid, expected_output)

            # Evaluate reasoning quality
            reasoning_quality = self.evaluate_reasoning_quality(agi_response)

            return {
                "correct": correct,
                "confidence": 0.8 if correct else 0.3,
                "reasoning_quality": reasoning_quality,
                "reasoning": f"Grid comparison: {'Match' if correct else 'No match'}"
            }

        except Exception as e:
            return {
                "correct": False,
                "confidence": 0.0,
                "reasoning_quality": 0.0,
                "reasoning": f"Evaluation error: {e}"
            }

    def extract_grid_from_response(self, response: str) -> Optional[List[List[int]]]:
        """Extract grid from AGI response"""
        # Look for grid patterns in the response
        lines = response.split('\n')
        grid_lines = []

        for line in lines:
            # Look for emoji patterns or number patterns
            if any(char in line for char in ['⬛', '🔴', '🔵', '🟡', '🟢', '0', '1', '2', '3', '4']):
                grid_lines.append(line.strip())

        if not grid_lines:
            return None

        # Convert to grid format
        grid = []
        for line in grid_lines:
            row = []
            for char in line:
                if char == '⬛' or char == '0':
                    row.append(0)
                elif char == '🔴' or char == '1':
                    row.append(1)
                elif char == '🔵' or char == '2':
                    row.append(2)
                elif char == '🟡' or char == '3':
                    row.append(3)
                elif char == '🟢' or char == '4':
                    row.append(4)
                else:
                    continue
            if row:
                grid.append(row)

        return grid if grid else None

    def compare_grids(self, grid1: List[List[int]], grid2: List[List[int]]) -> bool:
        """Compare two grids for equality"""
        if len(grid1) != len(grid2):
            return False

        for row1, row2 in zip(grid1, grid2):
            if len(row1) != len(row2):
                return False
            if row1 != row2:
                return False

        return True

    def evaluate_reasoning_quality(self, response: str) -> float:
        """Evaluate the quality of AGI's reasoning"""
        score = 0.0

        # Check for key reasoning elements
        response_lower = response.lower()

        if "pattern" in response_lower:
            score += 0.2
        if "rule" in response_lower or "transformation" in response_lower:
            score += 0.2
        if "because" in response_lower or "therefore" in response_lower:
            score += 0.2
        if "step" in response_lower or "logic" in response_lower:
            score += 0.2
        if len(response) > 200:  # Substantial response
            score += 0.2

        return min(score, 1.0)

    async def run_arc_test_suite(self, num_puzzles: int = 10) -> Dict[str, Any]:
        """Run the complete ARC test suite"""
        print("🧩 STARTING ARC-AGI BENCHMARK TEST")
        print("=" * 50)

        self.test_start_time = datetime.now()

        # Initialize AGI system
        if not await self.initialize_agi_system():
            return {"error": "Failed to initialize AGI system"}

        # Try to download ARC data, fallback to samples
        if not self.download_arc_data():
            print("⚠️ Using sample puzzles for testing...")
            self.arc_data = {"sample": self.create_sample_arc_puzzles()}

        # Select puzzles to test
        all_puzzles = []
        for dataset_name, puzzles in self.arc_data.items():
            if isinstance(puzzles, list):
                all_puzzles.extend([(f"{dataset_name}_{i}", puzzle) for i, puzzle in enumerate(puzzles)])
            elif isinstance(puzzles, dict):
                all_puzzles.extend([(puzzle_id, puzzle) for puzzle_id, puzzle in puzzles.items()])

        # Randomly select puzzles
        selected_puzzles = random.sample(all_puzzles, min(num_puzzles, len(all_puzzles)))

        print(f"📊 Testing {len(selected_puzzles)} puzzles...")

        # Run tests
        results = []
        correct_count = 0

        for puzzle_id, puzzle_data in selected_puzzles:
            result = await self.test_puzzle(puzzle_id, puzzle_data)
            results.append(result)

            if result["solved"]:
                correct_count += 1

            print(f"   {'✅' if result['solved'] else '❌'} {puzzle_id}: {result['solved']}")

        # Calculate final score
        accuracy = correct_count / len(results) if results else 0
        avg_confidence = sum(r["confidence"] for r in results) / len(results) if results else 0
        avg_reasoning = sum(r["reasoning_quality"] for r in results) / len(results) if results else 0

        self.test_end_time = datetime.now()
        test_duration = (self.test_end_time - self.test_start_time).total_seconds()

        final_results = {
            "test_metadata": {
                "test_type": "ARC-AGI Benchmark",
                "test_duration_seconds": test_duration,
                "puzzles_tested": len(results),
                "agi_system": "UnrestrictedAGISystem"
            },
            "performance_metrics": {
                "accuracy": accuracy,
                "average_confidence": avg_confidence,
                "average_reasoning_quality": avg_reasoning,
                "correct_solutions": correct_count,
                "total_solutions": len(results)
            },
            "detailed_results": results,
            "arc_capability_assessment": self.assess_arc_capabilities(accuracy, avg_reasoning)
        }

        # Save results
        self.save_test_results(final_results)

        return final_results

    def assess_arc_capabilities(self, accuracy: float, reasoning_quality: float) -> Dict[str, Any]:
        """Assess AGI capabilities based on ARC performance"""
        overall_score = (accuracy + reasoning_quality) / 2

        if overall_score >= 0.8:
            level = "EXCEPTIONAL_AGI"
            description = "Demonstrates advanced abstract reasoning and pattern recognition"
        elif overall_score >= 0.6:
            level = "ADVANCED_AGI"
            description = "Shows strong logical reasoning with room for improvement"
        elif overall_score >= 0.4:
            level = "DEVELOPING_AGI"
            description = "Basic pattern recognition present, needs enhancement"
        elif overall_score >= 0.2:
            level = "EMERGING_AGI"
            description = "Early signs of abstract reasoning capabilities"
        else:
            level = "BASIC_AI"
            description = "Limited abstract reasoning, primarily pattern matching"

        return {
            "agi_level": level,
            "overall_score": overall_score,
            "description": description,
            "strengths": self.identify_strengths(accuracy, reasoning_quality),
            "improvement_areas": self.identify_improvements(accuracy, reasoning_quality)
        }

    def identify_strengths(self, accuracy: float, reasoning_quality: float) -> List[str]:
        """Identify AGI strengths based on performance"""
        strengths = []

        if accuracy > 0.5:
            strengths.append("Pattern recognition and completion")
        if reasoning_quality > 0.6:
            strengths.append("Logical reasoning and rule inference")
        if accuracy > 0.3 and reasoning_quality > 0.4:
            strengths.append("Spatial reasoning capabilities")
        if accuracy > 0.7:
            strengths.append("Generalization to novel situations")

        return strengths

    def identify_improvements(self, accuracy: float, reasoning_quality: float) -> List[str]:
        """Identify areas for AGI improvement"""
        improvements = []

        if accuracy < 0.5:
            improvements.append("Enhance pattern recognition algorithms")
        if reasoning_quality < 0.6:
            improvements.append("Improve logical reasoning framework")
        if accuracy < 0.4:
            improvements.append("Develop better spatial reasoning")
        if reasoning_quality < 0.5:
            improvements.append("Strengthen rule inference capabilities")

        return improvements

    def save_test_results(self, results: Dict[str, Any]):
        """Save test results to file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"arc_agi_test_results_{timestamp}.json"

        with open(filename, 'w') as f:
            json.dump(results, f, indent=2, default=str)

        print(f"💾 Test results saved to: {filename}")

        # Generate summary report
        self.generate_summary_report(results)

    def generate_summary_report(self, results: Dict[str, Any]):
        """Generate a human-readable summary report"""
        report = f"""
🧩 ARC-AGI BENCHMARK TEST REPORT
==================================

Test Date: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
AGI System: Unrestricted AGI System

📊 PERFORMANCE METRICS
======================
Accuracy: {results['performance_metrics']['accuracy']:.1%}
Average Confidence: {results['performance_metrics']['average_confidence']:.1%}
Reasoning Quality: {results['performance_metrics']['average_reasoning_quality']:.1%}
Correct Solutions: {results['performance_metrics']['correct_solutions']}/{results['performance_metrics']['total_solutions']}

🎯 AGI CAPABILITY ASSESSMENT
============================
Level: {results['arc_capability_assessment']['agi_level']}
Score: {results['arc_capability_assessment']['overall_score']:.1%}
Description: {results['arc_capability_assessment']['description']}

💪 STRENGTHS
============
"""

        for strength in results['arc_capability_assessment']['strengths']:
            report += f"• {strength}\n"

        report += "\n🔧 IMPROVEMENT AREAS\n"
        report += "=" * 20 + "\n"

        for improvement in results['arc_capability_assessment']['improvement_areas']:
            report += f"• {improvement}\n"

        report += f"\n⏱️ Test Duration: {results['test_metadata']['test_duration_seconds']:.1f} seconds\n"

        # Save report
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_filename = f"arc_agi_test_report_{timestamp}.txt"

        with open(report_filename, 'w') as f:
            f.write(report)

        print(f"📄 Summary report saved to: {report_filename}")

async def main():
    """Main test execution"""
    print("🧩 ARC-AGI BENCHMARK TEST SUITE")
    print("=" * 50)

    # Initialize test
    arc_test = ARCAGITest()

    try:
        # Run the test suite
        results = await arc_test.run_arc_test_suite(num_puzzles=10)

        if "error" in results:
            print(f"❌ Test failed: {results['error']}")
            return

        # Display results
        print("\n🎯 TEST RESULTS SUMMARY")
        print("=" * 30)
        print(f"Accuracy: {results['performance_metrics']['accuracy']:.1%}")
        print(f"AGI Level: {results['arc_capability_assessment']['agi_level']}")
        print(f"Overall Score: {results['arc_capability_assessment']['overall_score']:.1%}")

        print("\n✅ Test completed successfully!")

    except KeyboardInterrupt:
        print("\n⏹️ Test interrupted by user")
    except Exception as e:
        print(f"❌ Test error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())
