# test_phase1.py
"""Test Phase 1 components"""

print("="*50)
print("PHASE 1 VERIFICATION")
print("="*50)

# Test 1: Settings
print("\n1. Testing Settings...")
try:
    from config.settings import get_settings
    settings = get_settings()
    print(f"✅ Settings loaded successfully")
    print(f"   - API Key: {settings.groq_api_key[:10]}... (hidden)")
    print(f"   - Model: {settings.groq_model}")
except Exception as e:
    print(f"❌ Settings failed: {e}")
    import traceback
    traceback.print_exc()
    exit(1)

# Test 2: Groq Client
print("\n2. Testing Groq Client...")
try:
    from services.groq_client import GroqClient
    client = GroqClient()
    print(f"✅ Groq client initialized")
except Exception as e:
    print(f"❌ Groq client failed: {e}")
    import traceback
    traceback.print_exc()
    exit(1)

# Test 3: Make a real API call
print("\n3. Testing API Connection...")
try:
    response = client.generate(
        messages=[{"role": "user", "content": "Say 'Hello' in one word"}],
        temperature=0.7,
        max_tokens=10
    )
    print(f"✅ API call successful")
    print(f"   Response: {response}")
except Exception as e:
    print(f"❌ API call failed: {e}")
    import traceback
    traceback.print_exc()
    exit(1)

# Test 4: State Schema
print("\n4. Testing State Schema...")
try:
    from orchestration.state import AgentState, AgentType
    print(f"✅ State schema imported")
    print(f"   Available agents: {[a.value for a in AgentType]}")
except Exception as e:
    print(f"❌ State schema failed: {e}")
    import traceback
    traceback.print_exc()
    exit(1)

# Test 5: Planner Agent
print("\n5. Testing Planner Agent...")
try:
    from agents.planner import PlannerAgent
    planner = PlannerAgent()
    print(f"✅ Planner agent initialized")
except Exception as e:
    print(f"❌ Planner agent failed: {e}")
    import traceback
    traceback.print_exc()
    exit(1)

# Test 6: Orchestrator
print("\n6. Testing Orchestrator...")
try:
    from orchestration.graph import AgentOrchestrator
    orchestrator = AgentOrchestrator()
    print(f"✅ Orchestrator initialized")
except Exception as e:
    print(f"❌ Orchestrator failed: {e}")
    import traceback
    traceback.print_exc()
    exit(1)

print("\n" + "="*50)
print("✅ ALL PHASE 1 TESTS PASSED!")
print("="*50)
print("\nReady to test with CLI? Run: python main.py")