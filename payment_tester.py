from payment_integration_agent import PaymentIntegrationAgent

def test_payment_system():
    print("🧪 TESTING AUTONOMOUS PAYMENT SYSTEM")
    print("=" * 45)
    
    # Initialize payment agent
    payment_agent = PaymentIntegrationAgent()
    payment_agent.setup_payment_methods()
    
    print("\n🧪 RUNNING PAYMENT TESTS:")
    print("=" * 30)
    
    # Test 1: Small profitable ad spend
    print("\n1️⃣ Testing small ad spend ($20)...")
    result1 = payment_agent.process_autonomous_payment(
        amount=20,
        purpose="Facebook ad campaign - high ROI content",
        expected_roi=250
    )
    print(f"Result: {result1['status']}")
    
    # Test 2: Medium tool subscription
    print("\n2️⃣ Testing tool subscription ($49)...")
    result2 = payment_agent.process_autonomous_payment(
        amount=49,
        purpose="Canva Pro subscription for visual content",
        expected_roi=300
    )
    print(f"Result: {result2['status']}")
    
    # Test 3: Large campaign (should require approval)
    print("\n3️⃣ Testing large campaign ($150)...")
    result3 = payment_agent.process_autonomous_payment(
        amount=150,
        purpose="Major Google Ads campaign",
        expected_roi=180
    )
    print(f"Result: {result3['status']}")
    
    # Test 4: Low ROI (should be declined)
    print("\n4️⃣ Testing low ROI spend ($30)...")
    result4 = payment_agent.process_autonomous_payment(
        amount=30,
        purpose="Experimental campaign",
        expected_roi=100  # Below 150% requirement
    )
    print(f"Result: {result4['status']}")
    
    print("\n✅ Payment testing complete!")
    print("📊 Check autonomous_transactions.json for logs")

if __name__ == "__main__":
    test_payment_system()
