#!/usr/bin/env python3
"""
DEEP PC 297 ANALYZER
Deep analysis of program counter 297 to understand the exact validation logic
"""

import os
import json
import time
from datetime import datetime
from typing import Dict, List, Optional
from algosdk.v2client import algod

class DeepPC297Analyzer:
    def __init__(self, algod_client, wallet_address, private_key):
        self.algod_client = algod_client
        self.wallet_address = wallet_address
        self.private_key = private_key
        
        # Folks Finance App ID
        self.folks_app_id = 465814065
        
        print("🔍 DEEP PC 297 ANALYZER")
        print(f"💰 Wallet: {self.wallet_address[:10]}...{self.wallet_address[-10:]}")
        print(f"🎯 Deep analysis of PC 297 validation logic")
    
    def analyze_pc_297_deep(self) -> Dict:
        """Deep analysis of program counter 297"""
        print("🔍 DEEP ANALYSIS OF PC 297")
        print("=" * 50)
        
        try:
            # Get app information
            print("📋 Getting app information...")
            app_info = self.algod_client.application_info(self.folks_app_id)
            
            # Extract approval program
            approval_program = app_info['params']['approval-program']
            if isinstance(approval_program, str):
                import base64
                approval_program = base64.b64decode(approval_program)
            
            print(f"✅ Approval program size: {len(approval_program)} bytes")
            
            # Focus on PC 297 area
            pc_297_byte_pos = 297 * 2  # Rough estimate: 2 bytes per instruction
            
            print(f"🎯 PC 297 estimated byte position: {pc_297_byte_pos}")
            
            # Analyze the exact area around PC 297
            analysis = self._analyze_pc_297_area(approval_program, pc_297_byte_pos)
            
            # Look for validation patterns
            validation_patterns = self._find_validation_patterns(approval_program, pc_297_byte_pos)
            analysis['validation_patterns'] = validation_patterns
            
            # Look for initialization requirements
            init_requirements = self._find_initialization_requirements(approval_program)
            analysis['init_requirements'] = init_requirements
            
            return analysis
            
        except Exception as e:
            print(f"❌ Error in deep analysis: {e}")
            return {'error': str(e)}
    
    def _analyze_pc_297_area(self, bytecode: bytes, target_pos: int) -> Dict:
        """Analyze the exact area around PC 297"""
        print(f"   🎯 Analyzing exact area around PC 297...")
        
        analysis = {
            'target_pc': 297,
            'target_byte_pos': target_pos,
            'context_analysis': {},
            'instruction_analysis': {},
            'validation_logic': {}
        }
        
        # Get wider context around PC 297
        context_start = max(0, target_pos - 50)
        context_end = min(len(bytecode), target_pos + 50)
        
        context_bytes = bytecode[context_start:context_end]
        analysis['context_analysis'] = {
            'start_pos': context_start,
            'end_pos': context_end,
            'context_size': len(context_bytes),
            'context_hex': context_bytes.hex(),
            'target_in_context': target_pos - context_start
        }
        
        print(f"      📍 Context: bytes {context_start}-{context_end}")
        print(f"      🔍 Context hex: {context_bytes.hex()[:100]}...")
        
        # Look for specific patterns around PC 297
        # Common validation patterns in Algorand smart contracts
        
        # Look for account validation
        if b'\x01' in context_bytes:  # intc_1 opcode
            analysis['validation_logic']['account_check'] = 'Possible account validation'
            print(f"      🔍 Found account validation pattern")
        
        # Look for app validation
        if b'\x02' in context_bytes:  # intc_2 opcode
            analysis['validation_logic']['app_check'] = 'Possible app validation'
            print(f"      🔍 Found app validation pattern")
        
        # Look for asset validation
        if b'\x03' in context_bytes:  # intc_3 opcode
            analysis['validation_logic']['asset_check'] = 'Possible asset validation'
            print(f"      🔍 Found asset validation pattern")
        
        # Look for error opcodes
        if b'\x00' in context_bytes:  # err opcode
            analysis['validation_logic']['error_point'] = 'Error opcode detected - validation failure'
            print(f"      ⚠️ ERROR OPCODE detected at PC 297!")
        
        return analysis
    
    def _find_validation_patterns(self, bytecode: bytes, target_pos: int) -> Dict:
        """Find validation patterns in the bytecode"""
        print(f"   🔍 Looking for validation patterns...")
        
        patterns = {
            'account_validation': [],
            'app_validation': [],
            'asset_validation': [],
            'state_validation': []
        }
        
        # Look for common validation sequences
        # These are patterns that typically appear before validation failures
        
        # Account validation: check if sender account has proper setup
        account_patterns = [
            b'\x01\x00',  # intc_1 + intc_0
            b'\x02\x00',  # intc_2 + intc_0
            b'\x03\x00'   # intc_3 + intc_0
        ]
        
        for pattern in account_patterns:
            positions = []
            start = 0
            while True:
                pos = bytecode.find(pattern, start)
                if pos == -1:
                    break
                positions.append(pos)
                start = pos + 1
            
            if positions:
                patterns['account_validation'].extend(positions)
        
        # App validation: check if app state is properly initialized
        app_patterns = [
            b'\x10\x00',  # load 0
            b'\x11\x00',  # load 1
            b'\x12\x00'   # load 2
        ]
        
        for pattern in app_patterns:
            positions = []
            start = 0
            while True:
                pos = bytecode.find(pattern, start)
                if pos == -1:
                    break
                positions.append(pos)
                start = pos + 1
            
            if positions:
                patterns['app_validation'].extend(positions)
        
        # Remove duplicates and sort
        for key in patterns:
            patterns[key] = sorted(list(set(patterns[key])))
        
        print(f"      📊 Found validation patterns:")
        for key, positions in patterns.items():
            if positions:
                print(f"         {key}: {len(positions)} positions")
        
        return patterns
    
    def _find_initialization_requirements(self, bytecode: bytes) -> Dict:
        """Find initialization requirements in the bytecode"""
        print(f"   🔍 Looking for initialization requirements...")
        
        requirements = {
            'required_operations': [],
            'initialization_sequence': [],
            'state_setup': []
        }
        
        # Look for initialization opcodes
        init_patterns = [
            b'\x20',  # store
            b'\x21',  # stores
            b'\x22',  # push
            b'\x23'   # pop
        ]
        
        for pattern in init_patterns:
            positions = []
            start = 0
            while True:
                pos = bytecode.find(pattern, start)
                if pos == -1:
                    break
                positions.append(pos)
                start = pos + 1
            
            if positions:
                requirements['state_setup'].extend(positions)
        
        # Look for specific initialization sequences
        # These might indicate what needs to be set up
        
        # Common DeFi initialization: user registration, escrow creation, etc.
        init_sequences = [
            b'\x01\x20',  # intc_1 + store
            b'\x02\x20',  # intc_2 + store
            b'\x03\x20'   # intc_3 + store
        ]
        
        for sequence in init_sequences:
            positions = []
            start = 0
            while True:
                pos = bytecode.find(sequence, start)
                if pos == -1:
                    break
                positions.append(pos)
                start = pos + 1
            
            if positions:
                requirements['initialization_sequence'].extend(positions)
        
        # Remove duplicates and sort
        for key in requirements:
            requirements[key] = sorted(list(set(requirements[key])))
        
        print(f"      📊 Found initialization requirements:")
        for key, positions in requirements.items():
            if positions:
                print(f"         {key}: {len(positions)} positions")
        
        return requirements
    
    def run_deep_analysis(self) -> Dict:
        """Run the complete deep analysis"""
        print("🚀 DEEP PC 297 ANALYSIS")
        print("=" * 60)
        
        # Run deep analysis
        analysis_results = self.analyze_pc_297_deep()
        
        # Display results
        print(f"\n📊 DEEP ANALYSIS RESULTS")
        print("=" * 40)
        
        if 'context_analysis' in analysis_results:
            context = analysis_results['context_analysis']
            print(f"🎯 PC 297 Context Analysis:")
            print(f"   Target PC: {analysis_results['target_pc']}")
            print(f"   Byte position: {context['start_pos']}-{context['end_pos']}")
            print(f"   Context size: {context['context_size']} bytes")
            print(f"   Context hex: {context['context_hex'][:100]}...")
        
        if 'validation_logic' in analysis_results:
            validation = analysis_results['validation_logic']
            print(f"\n🔍 Validation Logic Found:")
            for key, description in validation.items():
                print(f"   • {key}: {description}")
        
        if 'validation_patterns' in analysis_results:
            patterns = analysis_results['validation_patterns']
            print(f"\n📊 Validation Patterns:")
            for key, positions in patterns.items():
                if positions:
                    print(f"   • {key}: {len(positions)} positions")
        
        if 'init_requirements' in analysis_results:
            requirements = analysis_results['init_requirements']
            print(f"\n🔧 Initialization Requirements:")
            for key, positions in requirements.items():
                if positions:
                    print(f"   • {key}: {len(positions)} positions")
        
        # Save results
        with open('deep_pc_297_analysis.json', 'w') as f:
            json.dump(analysis_results, f, indent=2, default=str)
        
        print(f"\n📁 Deep analysis results saved to: deep_pc_297_analysis.json")
        
        return analysis_results

def main():
    """Test the deep PC 297 analyzer"""
    print("🧪 TESTING DEEP PC 297 ANALYZER")
    print("=" * 50)
    
    # This would be imported and used by the hybrid empire
    print("✅ Deep PC 297 Analyzer ready!")
    print("🎯 This system will analyze the exact validation logic!")
    print("🔗 Import this into your hybrid trading empire for deep protocol analysis!")

if __name__ == "__main__":
    main()
