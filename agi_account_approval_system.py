#!/usr/bin/env python3
"""
AGI ACCOUNT APPROVAL SYSTEM
Allows review and approval of AGI external account requests
"""

import os
import json
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any, Optional
import logging

class AGIAccountApprovalSystem:
    """System for reviewing and approving AGI account requests"""

    def __init__(self, workspace_path: str = "/home/ubuntu/wealthyrobot"):
        self.workspace_path = Path(workspace_path)

        # Import account creation system
        from autonomous_account_creation_system import AutonomousAccountCreationSystem
        self.account_system = AutonomousAccountCreationSystem(workspace_path)

        # Setup logging
        self.setup_logging()

        print("🔍 AGI ACCOUNT APPROVAL SYSTEM")
        print("=" * 50)
        print("📋 Ready to review pending AGI account requests")

    def setup_logging(self):
        """Setup logging"""
        log_file = self.workspace_path / "account_approval_system.log"
        logging.basicConfig(
            filename=log_file,
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger("account_approval")

    def review_pending_requests(self) -> Dict[str, Any]:
        """Review all pending account requests"""

        print("\\n📋 PENDING AGI ACCOUNT REQUESTS")
        print("=" * 40)

        pending_file = self.workspace_path / "pending_account_requests.json"

        if not pending_file.exists():
            print("✅ No pending requests found.")
            return {"pending_requests": []}

        try:
            with open(pending_file, 'r') as f:
                pending_requests = json.load(f)
        except:
            print("❌ Error loading pending requests.")
            return {"pending_requests": []}

        if not pending_requests:
            print("✅ No pending requests found.")
            return {"pending_requests": []}

        reviewed_requests = []

        for request_id, request in pending_requests.items():
            print(f"\\n🔍 REQUEST ID: {request_id}")
            print("-" * 30)
            print(f"📅 Requested: {request.get('timestamp', 'Unknown')}")
            print(f"🏷️  Account Type: {request.get('account_type', 'Unknown')}")
            print(f"🌐 Service: {request.get('service_name', 'Unknown')}")
            print(f"🎯 Purpose: {request.get('purpose', 'Unknown')}")
            print(f"⚠️  Risk Level: {request.get('risk_level', 'Unknown').upper()}")

            print("\\n🛡️  SECURITY MEASURES:")
            security = request.get('security_measures', {})
            for measure, value in security.items():
                print(f"  • {measure}: {value}")

            print("\\n📊 RISK ASSESSMENT:")
            risk_assessment = request.get('risk_assessment', {})
            for factor, level in risk_assessment.items():
                print(f"  • {factor}: {level}")

            reviewed_requests.append({
                "request_id": request_id,
                "request": request
            })

        return {
            "pending_requests": reviewed_requests,
            "total_pending": len(reviewed_requests)
        }

    def approve_request(self, request_id: str, reason: str = "Manual approval") -> Dict[str, Any]:
        """Approve a pending account request"""

        print(f"\\n✅ APPROVING REQUEST: {request_id}")
        print(f"📝 Reason: {reason}")

        result = self.account_system.approve_pending_request(request_id)

        if result["status"] == "approved":
            print("✅ Account approved and created successfully!")
            print(f"🔐 Username: {result['account_details']['username']}")
            print(f"🌐 Service: {result['account_details']['service_url']}")

            # Log approval
            self.logger.info(f"Account request {request_id} approved: {reason}")

            return result
        else:
            print(f"❌ Approval failed: {result.get('message', 'Unknown error')}")
            return result

    def deny_request(self, request_id: str, reason: str) -> Dict[str, Any]:
        """Deny a pending account request"""

        print(f"\\n❌ DENYING REQUEST: {request_id}")
        print(f"📝 Reason: {reason}")

        result = self.account_system.deny_request(request_id, reason)

        if result["status"] == "denied":
            print("✅ Account request denied.")
            print(f"📝 Reason: {result.get('reason', reason)}")

            # Log denial
            self.logger.info(f"Account request {request_id} denied: {reason}")

            return result
        else:
            print(f"❌ Denial failed: {result.get('message', 'Unknown error')}")
            return result

    def batch_approve_high_value(self) -> Dict[str, Any]:
        """Batch approve high-value, lower-risk requests"""

        print("\\n📦 BATCH APPROVAL OF HIGH-VALUE REQUESTS")
        print("=" * 45)

        pending_file = self.workspace_path / "pending_account_requests.json"

        if not pending_file.exists():
            print("❌ No pending requests file found.")
            return {"status": "error", "message": "No pending requests"}

        try:
            with open(pending_file, 'r') as f:
                pending_requests = json.load(f)
        except:
            print("❌ Error loading pending requests.")
            return {"status": "error", "message": "Load error"}

        # Define criteria for batch approval
        batch_criteria = {
            "allowed_types": ["api_service", "data_source", "communication"],
            "max_risk_level": "high",  # Approve up to high risk, but not critical
            "required_security": ["encryption", "authentication", "monitoring"]
        }

        approved_requests = []
        remaining_requests = {}

        for request_id, request in pending_requests.items():
            # Check if meets batch approval criteria
            account_type = request.get("account_type", "")
            risk_level = request.get("risk_level", "critical")
            security_measures = request.get("security_measures", {})

            meets_criteria = (
                account_type in batch_criteria["allowed_types"] and
                risk_level != "critical" and  # Don't auto-approve critical
                all(measure in security_measures for measure in batch_criteria["required_security"])
            )

            if meets_criteria:
                print(f"📋 Auto-approving: {request_id} ({request.get('service_name', 'Unknown')})")

                approval_result = self.approve_request(
                    request_id,
                    "Batch approval - meets security criteria"
                )

                if approval_result["status"] == "approved":
                    approved_requests.append(approval_result)
                else:
                    remaining_requests[request_id] = request
            else:
                remaining_requests[request_id] = request
                print(f"⏳ Keeping pending: {request_id} (Risk: {risk_level})")

        # Save remaining requests
        with open(pending_file, 'w') as f:
            json.dump(remaining_requests, f, indent=2, default=str)

        print(f"\\n📊 BATCH APPROVAL COMPLETE:")
        print(f"  ✅ Approved: {len(approved_requests)}")
        print(f"  ⏳ Still Pending: {len(remaining_requests)}")

        return {
            "status": "success",
            "approved": approved_requests,
            "remaining": len(remaining_requests)
        }

    def get_system_status(self) -> Dict[str, Any]:
        """Get comprehensive system status"""

        # Get account system status
        account_status = self.account_system.get_system_status()

        # Get pending requests
        pending_file = self.workspace_path / "pending_account_requests.json"
        pending_count = 0
        if pending_file.exists():
            try:
                with open(pending_file, 'r') as f:
                    pending_requests = json.load(f)
                    pending_count = len(pending_requests)
            except:
                pending_count = 0

        return {
            "account_system": account_status,
            "pending_requests": pending_count,
            "approval_system_status": "active"
        }

def interactive_approval():
    """Interactive approval interface"""

    approval_system = AGIAccountApprovalSystem()

    print("\\n🎮 AGI ACCOUNT APPROVAL INTERFACE")
    print("=" * 45)

    while True:
        print("\\n📋 MENU:")
        print("1. Review pending requests")
        print("2. Approve specific request")
        print("3. Deny specific request")
        print("4. Batch approve safe requests")
        print("5. Show system status")
        print("6. Exit")

        choice = input("\\n👤 Enter choice (1-6): ").strip()

        if choice == "1":
            approval_system.review_pending_requests()

        elif choice == "2":
            request_id = input("🔍 Enter request ID to approve: ").strip()
            if request_id:
                reason = input("📝 Approval reason: ").strip() or "Manual approval"
                approval_system.approve_request(request_id, reason)

        elif choice == "3":
            request_id = input("🔍 Enter request ID to deny: ").strip()
            if request_id:
                reason = input("📝 Denial reason: ").strip() or "Manual denial"
                approval_system.deny_request(request_id, reason)

        elif choice == "4":
            confirm = input("⚠️  Batch approve safe requests? (y/N): ").strip().lower()
            if confirm == "y":
                approval_system.batch_approve_high_value()

        elif choice == "5":
            status = approval_system.get_system_status()
            print("\\n📊 SYSTEM STATUS:")
            for key, value in status.items():
                if isinstance(value, dict):
                    print(f"  {key}:")
                    for sub_key, sub_value in value.items():
                        print(f"    {sub_key}: {sub_value}")
                else:
                    print(f"  {key}: {value}")

        elif choice == "6":
            print("\\n👋 Goodbye!")
            break

        else:
            print("❌ Invalid choice. Please try again.")

def main():
    """Main execution function"""
    print("🔍 AGI ACCOUNT APPROVAL SYSTEM")
    print("=" * 50)

    # Check if running interactively
    if len(os.sys.argv) > 1 and os.sys.argv[1] == "--interactive":
        interactive_approval()
    else:
        # Non-interactive mode - just show status
        approval_system = AGIAccountApprovalSystem()
        status = approval_system.get_system_status()

        print("\\n📊 ACCOUNT APPROVAL SYSTEM STATUS:")
        print(f"  Pending Requests: {status['pending_requests']}")
        print(f"  Total Accounts: {status['account_system']['total_accounts']}")
        print(f"  System Status: {status['approval_system_status'].upper()}")

        if status['pending_requests'] > 0:
            print("\\n🔍 Run with --interactive to review and approve requests:")
            print("  python3 agi_account_approval_system.py --interactive")

if __name__ == "__main__":
    main()
