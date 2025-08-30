#!/usr/bin/env python3
"""
SMART CONTRACT ANALYZER
Analyzes DeFi smart contracts to discover correct parameters
"""

import base64
from algosdk.v2client import algod

def analyze_smart_contract(app_id: int):
    """Analyze a smart contract to understand its structure"""
    print(f"🔍 Analyzing smart contract App ID: {app_id}")
    
    try:
        # Connect to Algorand
        algod_client = algod.AlgodClient("", "https://mainnet-api.algonode.cloud")
        
        # Get application info
        app_info = algod_client.application_info(app_id)
        
        if not app_info:
            print(f"❌ App ID {app_id} not found")
            return None
        
        print(f"✅ App found: {app_id}")
        print(f"   Creator: {app_info['params']['creator']}")
        
        # Analyze approval program
        approval_program = app_info['params']['approval-program']
        approval_program_bytes = base64.b64decode(approval_program)
        
        print(f"   Approval Program: {len(approval_program_bytes)} bytes")
        
        # Look for common patterns in the bytecode
        analyze_bytecode(approval_program_bytes, f"App {app_id}")
        
        return app_info
        
    except Exception as e:
        print(f"❌ Error analyzing app {app_id}: {e}")
        return None

def analyze_bytecode(bytecode: bytes, app_name: str):
    """Analyze bytecode for common patterns"""
    print(f"🔍 Analyzing bytecode for {app_name}")
    
    # Convert to hex for analysis
    hex_code = bytecode.hex()
    
    # Look for common opcodes and patterns
    print("   Looking for common patterns...")
    
    # Check for bootstrap pattern
    if b"bootstrap" in bytecode:
        print("   ✅ Found 'bootstrap' pattern")
    
    # Check for swap pattern
    if b"swap" in bytecode:
        print("   ✅ Found 'swap' pattern")
    
    # Check for supply pattern
    if b"supply" in bytecode:
        print("   ✅ Found 'supply' pattern")
    
    # Check for common AVM opcodes
    common_opcodes = {
        0x01: "err",
        0x02: "sha256",
        0x03: "keccak256",
        0x04: "sha512_256",
        0x05: "ed25519verify",
        0x06: "ecdsa_verify",
        0x07: "ecdsa_pk_decompress",
        0x08: "ecdsa_pk_recover",
        0x09: "+",
        0x0a: "-",
        0x0b: "*",
        0x0c: "/",
        0x0d: "<",
        0x0e: ">",
        0x0f: "<=",
        0x10: ">=",
        0x11: "&&",
        0x12: "||",
        0x13: "==",
        0x14: "!=",
        0x15: "!",
        0x16: "len",
        0x17: "itob",
        0x18: "btoi",
        0x19: "%",
        0x1a: "|",
        0x1b: "&",
        0x1c: "^",
        0x1d: "~",
        0x1e: "sqrt",
        0x1f: "log",
        0x20: "exp",
        0x21: "expw",
        0x22: "b+",
        0x23: "b-",
        0x24: "b/",
        0x25: "b*",
        0x26: "b<",
        0x27: "b>",
        0x28: "b<=",
        0x29: "b>=",
        0x2a: "b==",
        0x2b: "b!=",
        0x2c: "b%",
        0x2d: "b|",
        0x2e: "b&",
        0x2f: "b^",
        0x30: "b~",
        0x31: "bzero",
        0x32: "btoi",
        0x33: "itob",
        0x34: "b+",
        0x35: "b-",
        0x36: "b/",
        0x37: "b*",
        0x38: "b<",
        0x39: "b>",
        0x3a: "b<=",
        0x3b: "b>=",
        0x3c: "b==",
        0x3d: "b!=",
        0x3e: "b%",
        0x3f: "b|",
        0x40: "b&",
        0x41: "b^",
        0x42: "b~",
        0x43: "bzero",
        0x44: "btoi",
        0x45: "itob",
        0x46: "b+",
        0x47: "b-",
        0x48: "b/",
        0x49: "b*",
        0x4a: "b<",
        0x4b: "b>",
        0x4c: "b<=",
        0x4d: "b>=",
        0x4e: "b==",
        0x4f: "b!=",
        0x50: "b%",
        0x51: "b|",
        0x52: "b&",
        0x53: "b^",
        0x54: "b~",
        0x55: "bzero",
        0x56: "btoi",
        0x57: "itob",
        0x58: "b+",
        0x59: "b-",
        0x5a: "b/",
        0x5b: "b*",
        0x5c: "b<",
        0x5d: "b>",
        0x5e: "b<=",
        0x5f: "b>=",
        0x60: "b==",
        0x61: "b!=",
        0x62: "b%",
        0x63: "b|",
        0x64: "b&",
        0x65: "b^",
        0x66: "b~",
        0x67: "bzero",
        0x68: "btoi",
        0x69: "itob",
        0x6a: "b+",
        0x6b: "b-",
        0x6c: "b/",
        0x6d: "b*",
        0x6e: "b<",
        0x6f: "b>",
        0x70: "b<=",
        0x71: "b>=",
        0x72: "b==",
        0x73: "b!=",
        0x74: "b%",
        0x75: "b|",
        0x76: "b&",
        0x77: "b^",
        0x78: "b~",
        0x79: "bzero",
        0x7a: "btoi",
        0x7b: "itob",
        0x7c: "b+",
        0x7d: "b-",
        0x7e: "b/",
        0x7f: "b*",
        0x80: "b<",
        0x81: "b>",
        0x82: "b<=",
        0x83: "b>=",
        0x84: "b==",
        0x85: "b!=",
        0x86: "b%",
        0x87: "b|",
        0x88: "b&",
        0x89: "b^",
        0x8a: "b~",
        0x8b: "bzero",
        0x8c: "btoi",
        0x8d: "itob",
        0x8e: "b+",
        0x8f: "b-",
        0x90: "b/",
        0x91: "b*",
        0x92: "b<",
        0x93: "b>",
        0x94: "b<=",
        0x95: "b>=",
        0x96: "b==",
        0x97: "b!=",
        0x98: "b%",
        0x99: "b|",
        0x9a: "b&",
        0x9b: "b^",
        0x9c: "b~",
        0x9d: "bzero",
        0x9e: "btoi",
        0x9f: "itob",
        0xa0: "b+",
        0xa1: "b-",
        0xa2: "b/",
        0xa3: "b*",
        0xa4: "b<",
        0xa5: "b>",
        0xa6: "b<=",
        0xa7: "b>=",
        0xa8: "b==",
        0xa9: "b!=",
        0xaa: "b%",
        0xab: "b|",
        0xac: "b&",
        0xad: "b^",
        0xae: "b~",
        0xaf: "bzero",
        0xb0: "btoi",
        0xb1: "itob",
        0xb2: "b+",
        0xb3: "b-",
        0xb4: "b/",
        0xb5: "b*",
        0xb6: "b<",
        0xb7: "b>",
        0xb8: "b<=",
        0xb9: "b>=",
        0xba: "b==",
        0xbb: "b!=",
        0xbc: "b%",
        0xbd: "b|",
        0xbe: "b&",
        0xbf: "b^",
        0xc0: "b~",
        0xc1: "bzero",
        0xc2: "btoi",
        0xc3: "itob",
        0xc4: "b+",
        0xc5: "b-",
        0xc6: "b/",
        0xc7: "b*",
        0xc8: "b<",
        0xc9: "b>",
        0xca: "b<=",
        0xcb: "b>=",
        0xcc: "b==",
        0xcd: "b!=",
        0xce: "b%",
        0xcf: "b|",
        0xd0: "b&",
        0xd1: "b^",
        0xd2: "b~",
        0xd3: "bzero",
        0xd4: "btoi",
        0xd5: "itob",
        0xd6: "b+",
        0xd7: "b-",
        0xd8: "b/",
        0xd9: "b*",
        0xda: "b<",
        0xdb: "b>",
        0xdc: "b<=",
        0xdd: "b>=",
        0xde: "b==",
        0xdf: "b!=",
        0xe0: "b%",
        0xe1: "b|",
        0xe2: "b&",
        0xe3: "b^",
        0xe4: "b~",
        0xe5: "bzero",
        0xe6: "btoi",
        0xe7: "itob",
        0xe8: "b+",
        0xe9: "b-",
        0xea: "b/",
        0xeb: "b*",
        0xec: "b<",
        0xed: "b>",
        0xee: "b<=",
        0xef: "b>=",
        0xf0: "b==",
        0xf1: "b!=",
        0xf2: "b%",
        0xf3: "b|",
        0xf4: "b&",
        0xf5: "b^",
        0xf6: "b~",
        0xf7: "bzero",
        0xf8: "btoi",
        0xf9: "itob",
        0xfa: "b+",
        0xfb: "b-",
        0xfc: "b/",
        0xfd: "b*",
        0xfe: "b<",
        0xff: "b>"
    }
    
    # Look for specific opcodes
    for i, byte in enumerate(bytecode):
        if byte in common_opcodes:
            opcode_name = common_opcodes[byte]
            if opcode_name in ["err", "bzero", "btoi", "itob"]:
                print(f"   Found {opcode_name} at position {i}")
    
    print("   Bytecode analysis complete")

def main():
    """Analyze DeFi smart contracts"""
    print("🔍 SMART CONTRACT ANALYZER")
    print("=" * 50)
    
    # Analyze known DeFi protocols
    protocols = [
        ("Tinyman V2", 1002541853),
        ("Folks Finance", 465814065)
    ]
    
    for name, app_id in protocols:
        print(f"\n🔍 Analyzing {name}...")
        analyze_smart_contract(app_id)
        print("-" * 30)

if __name__ == "__main__":
    main()
