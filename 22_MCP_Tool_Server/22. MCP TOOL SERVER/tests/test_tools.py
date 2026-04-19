import httpx
import json
import time

BASE_URL = "http://localhost:8000/api/v1"
API_KEY = "mcp_test_key_123"

def test_health():
    print("\n[TEST] Health checking...")
    try:
        response = httpx.get("http://localhost:8000/")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Failed to connect: {e}")

def test_tool_discovery():
    print("\n[TEST] Tool Discovery...")
    headers = {"X-API-Key": API_KEY}
    response = httpx.get(f"{BASE_URL}/tools", headers=headers)
    print(f"Status: {response.status_code}")
    print(f"Tools found: {len(response.json()['tools'])}")
    print(json.dumps(response.json(), indent=2))

def test_execute_crm_tool():
    print("\n[TEST] Executing CRM Tool...")
    headers = {"X-API-Key": API_KEY}
    payload = {
        "parameters": {"customer_id": "CUST-001"}
    }
    response = httpx.post(f"{BASE_URL}/tools/get_customer_info", headers=headers, json=payload)
    print(f"Status: {response.status_code}")
    print(f"Result: {response.json()}")

def test_execute_db_tool():
    print("\n[TEST] Executing DB Tool...")
    headers = {"X-API-Key": API_KEY}
    payload = {
        "parameters": {"query": "Check inventory for laptops"}
    }
    response = httpx.post(f"{BASE_URL}/tools/query_internal_db", headers=headers, json=payload)
    print(f"Status: {response.status_code}")
    print(f"Result: {response.json()}")

def test_invalid_auth():
    print("\n[TEST] Invalid Auth...")
    headers = {"X-API-Key": "wrong_key"}
    response = httpx.get(f"{BASE_URL}/tools", headers=headers)
    print(f"Status: {response.status_code} (Expected 403)")
    print(f"Detail: {response.json()}")

if __name__ == "__main__":
    print("Starting MCP Tool Server Integration Tests...")
    print("Note: Ensure the server is running on http://localhost:8000")
    
    test_health()
    test_tool_discovery()
    test_execute_crm_tool()
    test_execute_db_tool()
    test_invalid_auth()
    
    print("\nTests completed.")
