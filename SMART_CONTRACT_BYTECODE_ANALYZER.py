#!/usr/bin/env python3
"""
SMART CONTRACT BYTECODE ANALYZER
Analyze Folks Finance smart contract bytecode to understand validation logic
"""

import os
import json
import time
from typing import Dict, List, Optional
from algosdk.v2client import algod

class SmartContractBytecodeAnalyzer:
    def __init__(self, algod_client, wallet_address, private_key):
        self.algod_client = algod_client
        self.wallet_address = wallet_address
        self.private_key = private_key
        
        # Folks Finance App ID
        self.folks_app_id = 465814065
        
        print("🔍 SMART CONTRACT BYTECODE ANALYZER Initialized")
        print(f"💰 Wallet: {self.wallet_address[:10]}...{self.wallet_address[-10:]}")
        print(f"🎯 Analyzing Folks Finance smart contract (App ID: {self.folks_app_id})")
    
    def analyze_smart_contract_bytecode(self) -> Dict:
        """Analyze the smart contract bytecode in detail"""
        print("🔍 ANALYZING SMART CONTRACT BYTECODE")
        print("=" * 50)
        
        analysis_results = {}
        
        try:
            # Get detailed app information
            print("📋 Getting detailed app information...")
            app_info = self.algod_client.application_info(self.folks_app_id)
            
            # Extract approval program bytecode
            approval_program = app_info['params']['approval-program']
            clear_state_program = app_info['params']['clear-state-program']
            
            # Convert to bytes if they're strings
            if isinstance(approval_program, str):
                import base64
                approval_program = base64.b64decode(approval_program)
            if isinstance(clear_state_program, str):
                import base64
                clear_state_program = base64.b64decode(clear_state_program)
            
            print(f"✅ Approval program size: {len(approval_program)} bytes")
            print(f"✅ Clear state program size: {len(clear_state_program)} bytes")
            
            # Analyze the approval program bytecode
            print("🔍 Analyzing approval program bytecode...")
            approval_analysis = self._analyze_bytecode(approval_program, "approval")
            analysis_results['approval_program'] = approval_analysis
            
            # Analyze the clear state program bytecode
            print("🔍 Analyzing clear state program bytecode...")
            clear_state_analysis = self._analyze_bytecode(clear_state_program, "clear_state")
            analysis_results['clear_state_program'] = clear_state_analysis
            
            # Analyze the specific area around program counter 297
            print("🎯 Analyzing area around program counter 297...")
            pc_297_analysis = self._analyze_program_counter_area(approval_program, 297)
            analysis_results['pc_297_analysis'] = pc_297_analysis
            
            # Get app creator and global state
            print("👤 Getting app creator and global state...")
            creator_analysis = self._analyze_app_creator(app_info)
            analysis_results['creator_analysis'] = creator_analysis
            
            # Analyze local state schema
            print("📊 Analyzing local state schema...")
            schema_analysis = self._analyze_state_schemas(app_info)
            analysis_results['schema_analysis'] = schema_analysis
            
        except Exception as e:
            print(f"❌ Error analyzing smart contract: {e}")
            analysis_results['error'] = str(e)
        
        return analysis_results
    
    def _analyze_bytecode(self, bytecode: bytes, program_type: str) -> Dict:
        """Analyze bytecode for patterns and structure"""
        analysis = {
            'program_type': program_type,
            'total_size': len(bytecode),
            'byte_patterns': {},
            'opcode_frequency': {},
            'structure_analysis': {}
        }
        
        # Analyze byte patterns
        print(f"   📊 Analyzing {program_type} bytecode patterns...")
        
        # Look for common patterns
        common_patterns = [
            b'\x00',  # Zero bytes
            b'\xff',  # All ones
            b'\x01',  # Single byte
            b'\x02',  # Two byte
            b'\x03',  # Three byte
        ]
        
        for pattern in common_patterns:
            count = bytecode.count(pattern)
            if count > 0:
                analysis['byte_patterns'][pattern.hex()] = count
        
        # Analyze opcode frequency (first byte of each instruction)
        opcode_counts = {}
        for i in range(0, len(bytecode), 2):  # Most Algorand opcodes are 2 bytes
            if i < len(bytecode):
                opcode = bytecode[i]
                opcode_counts[opcode] = opcode_counts.get(opcode, 0) + 1
        
        # Get top 10 most common opcodes
        sorted_opcodes = sorted(opcode_counts.items(), key=lambda x: x[1], reverse=True)[:10]
        analysis['opcode_frequency'] = {f"0x{opcode:02x}": count for opcode, count in sorted_opcodes}
        
        # Analyze structure
        analysis['structure_analysis'] = {
            'start_bytes': bytecode[:20].hex(),
            'end_bytes': bytecode[-20:].hex(),
            'middle_bytes': bytecode[len(bytecode)//2-10:len(bytecode)//2+10].hex() if len(bytecode) > 20 else bytecode.hex()
        }
        
        return analysis
    
    def _analyze_program_counter_area(self, bytecode: bytes, target_pc: int) -> Dict:
        """Analyze the specific area around a program counter"""
        print(f"   🎯 Analyzing area around PC {target_pc}...")
        
        analysis = {
            'target_pc': target_pc,
            'area_analysis': {},
            'context_bytes': {},
            'validation_patterns': {}
        }
        
        # Calculate approximate byte position (rough estimate: 2 bytes per instruction)
        estimated_byte_pos = target_pc * 2
        
        if estimated_byte_pos < len(bytecode):
            # Get context around the target PC
            start_pos = max(0, estimated_byte_pos - 20)
            end_pos = min(len(bytecode), estimated_byte_pos + 20)
            
            context_bytes = bytecode[start_pos:end_pos]
            analysis['context_bytes'] = {
                'start_position': start_pos,
                'end_position': end_pos,
                'target_byte_position': estimated_byte_pos,
                'context_hex': context_bytes.hex(),
                'context_size': len(context_bytes)
            }
            
            # Look for validation patterns around this area
            print(f"      📍 Target area: bytes {start_pos}-{end_pos}")
            print(f"      🔍 Context: {context_bytes.hex()[:50]}...")
            
            # Analyze what might be happening at this point
            if b'\x00' in context_bytes:
                analysis['validation_patterns']['zero_bytes'] = 'Possible null check or initialization'
            
            if b'\x01' in context_bytes:
                analysis['validation_patterns']['single_byte'] = 'Possible boolean check or flag validation'
            
            # Look for error opcodes
            if b'\x00' in context_bytes:  # err opcode is typically 0x00
                analysis['validation_patterns']['error_opcode'] = 'Error opcode detected - validation failure point'
                print(f"      ⚠️ ERROR OPCODE detected at PC {target_pc}!")
        
        return analysis
    
    def _analyze_app_creator(self, app_info: Dict) -> Dict:
        """Analyze the app creator and related information"""
        analysis = {
            'creator': app_info['params']['creator'],
            'app_id': app_info['id'],
            'global_state_schema': app_info['params']['global-state-schema'],
            'local_state_schema': app_info['params']['local-state-schema']
        }
        
        # Get creator account info
        try:
            creator_info = self.algod_client.account_info(app_info['params']['creator'])
            analysis['creator_account'] = {
                'balance': creator_info.get('amount', 0),
                'total_apps': len(creator_info.get('apps-local-state', [])),
                'total_assets': len(creator_info.get('assets', [])),
                'created_apps': len(creator_info.get('created-apps', []))
            }
        except Exception as e:
            analysis['creator_account'] = {'error': str(e)}
        
        return analysis
    
    def _analyze_state_schemas(self, app_info: Dict) -> Dict:
        """Analyze the state schemas for the app"""
        analysis = {}
        
        # Global state schema
        global_schema = app_info['params']['global-state-schema']
        if global_schema:
            analysis['global_state'] = {
                'num_uints': global_schema.get('num-uint', 0),
                'num_byte_slices': global_schema.get('num-byte-slice', 0)
            }
        
        # Local state schema
        local_schema = app_info['params']['local-state-schema']
        if local_schema:
            analysis['local_state'] = {
                'num_uints': local_schema.get('num-uint', 0),
                'num_byte_slices': local_schema.get('num-byte-slice', 0)
            }
        
        return analysis
    
    def run_comprehensive_analysis(self) -> Dict:
        """Run comprehensive smart contract analysis"""
        print("🚀 COMPREHENSIVE SMART CONTRACT ANALYSIS")
        print("=" * 60)
        
        # Run analysis
        analysis_results = self.analyze_smart_contract_bytecode()
        
        # Display results
        print(f"\n📊 ANALYSIS RESULTS")
        print("=" * 40)
        
        # Display approval program analysis
        if 'approval_program' in analysis_results:
            approval = analysis_results['approval_program']
            print(f"📋 Approval Program:")
            print(f"   Size: {approval['total_size']} bytes")
            print(f"   Top opcodes: {dict(list(approval['opcode_frequency'].items())[:5])}")
        
        # Display PC 297 analysis
        if 'pc_297_analysis' in analysis_results:
            pc_analysis = analysis_results['pc_297_analysis']
            print(f"\n🎯 Program Counter 297 Analysis:")
            print(f"   Target PC: {pc_analysis['target_pc']}")
            
            if 'context_bytes' in pc_analysis:
                context = pc_analysis['context_bytes']
                print(f"   Context bytes: {context['start_position']}-{context['end_position']}")
                print(f"   Context hex: {context['context_hex'][:50]}...")
            
            if 'validation_patterns' in pc_analysis:
                patterns = pc_analysis['validation_patterns']
                for pattern, description in patterns.items():
                    print(f"   Pattern: {pattern} - {description}")
        
        # Display creator analysis
        if 'creator_analysis' in analysis_results:
            creator = analysis_results['creator_analysis']
            print(f"\n👤 App Creator Analysis:")
            print(f"   Creator: {creator['creator'][:20]}...")
            print(f"   Global state: {creator['global_state_schema']}")
            print(f"   Local state: {creator['local_state_schema']}")
        
        # Save analysis results
        with open('smart_contract_analysis_results.json', 'w') as f:
            # Convert bytes to strings for JSON serialization
            json_safe_results = json.loads(json.dumps(analysis_results, default=str))
            json.dump(json_safe_results, f, indent=2)
        
        print(f"\n📁 Analysis results saved to: smart_contract_analysis_results.json")
        
        return analysis_results

def main():
    """Test the smart contract bytecode analyzer"""
    print("🧪 TESTING SMART CONTRACT BYTECODE ANALYZER")
    print("=" * 50)
    
    # This would be imported and used by the hybrid empire
    print("✅ Smart Contract Bytecode Analyzer ready!")
    print("🎯 This system will analyze smart contract bytecode!")
    print("🔗 Import this into your hybrid trading empire for deep protocol analysis!")

if __name__ == "__main__":
    main()

