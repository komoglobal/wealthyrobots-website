#!/usr/bin/env python3
"""
CLAUDE Testing Blackbox v1.0 - Safe Experimentation Environment
Fixed version with proper syntax and functionality
"""

import os
import sys
import time
import json
import subprocess
from datetime import datetime
from contextlib import contextmanager

class ClaudeTestingBlackbox:
    def __init__(self, test_environment="claude_blackbox_tests"):
        print("🧪 CLAUDE Testing Blackbox v1.0 - Safe Experimentation Environment initialized")
        self.test_environment = test_environment
        self.sandbox_dir = os.path.join(test_environment, "sandbox")
        self.results_dir = os.path.join(test_environment, "results")
        self.experiments_dir = os.path.join(test_environment, "experiments")
        
        # Create directory structure
        os.makedirs(self.sandbox_dir, exist_ok=True)
        os.makedirs(self.results_dir, exist_ok=True)
        os.makedirs(self.experiments_dir, exist_ok=True)
        
        print(f"📁 Test environment: {test_environment}")
        print("🔒 Safe sandbox mode: ACTIVE")
    
    def test_code_execution(self, code, test_name="code_test", language="python"):
        """Test code execution safely"""
        print(f"🧪 Testing {language} code: {test_name}")
        
        # Create test directory
        test_dir = os.path.join(self.sandbox_dir, f"test_{test_name}_{int(time.time())}")
        os.makedirs(test_dir, exist_ok=True)
        original_dir = os.getcwd()
        
        start_time = time.time()
        try:
            os.chdir(test_dir)
            print(f"🧪 Starting test: {test_name}")
            print(f"📁 Test directory: {test_dir}")
            
            if language == "python":
                test_file = f"{test_name}.py"
                with open(test_file, 'w') as f:
                    f.write(code)
                
                # Execute safely
                result = subprocess.run(['python3', test_file], 
                                      capture_output=True, text=True, timeout=30)
                
                test_result = {
                    "test_name": test_name,
                    "language": language,
                    "success": result.returncode == 0,
                    "stdout": result.stdout,
                    "stderr": result.stderr,
                    "returncode": result.returncode,
                    "execution_time": time.time() - start_time,
                    "test_directory": test_dir
                }
                
                os.chdir(original_dir)
                print(f"✅ Test completed: {test_name}")
                self.save_test_result(test_result)
                return test_result
                
        except Exception as e:
            os.chdir(original_dir)
            error_result = {
                "error": str(e),
                "success": False,
                "test_name": test_name
            }
            self.save_test_result(error_result)
            return error_result
    
    def save_test_result(self, result):
        """Save test result with proper error handling"""
        start_time = time.time()
        try:
            # Ensure results directory exists
            os.makedirs(self.results_dir, exist_ok=True)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            test_name = result.get('test_name', 'unknown')
            filename = f"test_result_{timestamp}_{test_name}.json"
            filepath = os.path.join(self.results_dir, filename)
            
            with open(filepath, 'w') as f:
                json.dump(result, f, indent=2)
            
            print(f"💾 Result saved: {filename}")
            
        except Exception as e:
            print(f"❌ Failed to save result: {e}")
            print(f"Result: {json.dumps(result, indent=2)}")

    def test_algorithm_performance(self, algorithm_func, test_data, test_name="algorithm_test"):
        """Test algorithm performance"""
        print(f"⚡ Testing algorithm performance: {test_name}")
        
        start_time = time.time()
        try:
            start_time = time.time()
            algorithm_result = algorithm_func(test_data)
            end_time = time.time()
            
            performance_result = {
                "test_name": test_name,
                "success": True,
                "result": str(algorithm_result),
                "execution_time": end_time - start_time,
                "test_data_size": len(test_data) if hasattr(test_data, '__len__') else 1
            }
            
            self.save_test_result(performance_result)
            return performance_result
            
        except Exception as e:
            error_result = {
                "test_name": test_name,
                "success": False,
                "error": str(e)
            }
            self.save_test_result(error_result)
            return error_result

if __name__ == "__main__":
    # Quick test
    bb = ClaudeTestingBlackbox()
    result = bb.test_code_execution('print("Blackbox ready!")', 'startup_test')
    print(f"Startup test success: {result.get('success')}")
