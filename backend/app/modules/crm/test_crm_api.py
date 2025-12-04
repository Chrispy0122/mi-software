import requests
import json

BASE_URL = "http://127.0.0.1:8000/v1/crm"

def test_api():
    print("Testing CRM API...")
    
    # 1. Create Client
    new_client = {
        "name": "Test Client",
        "business_name": "Test Corp",
        "email": "test@example.com",
        "status": "Active"
    }
    try:
        response = requests.post(f"{BASE_URL}/clients", json=new_client)
        if response.status_code == 200:
            print("✅ Create Client: Success")
            client_id = response.json()["id"]
        else:
            print(f"❌ Create Client: Failed ({response.status_code}) - {response.text}")
            return
    except Exception as e:
        print(f"❌ Create Client: Error - {e}")
        return

    # 2. List Clients
    try:
        response = requests.get(f"{BASE_URL}/clients")
        if response.status_code == 200:
            print(f"✅ List Clients: Success (Found {len(response.json())} clients)")
        else:
            print(f"❌ List Clients: Failed ({response.status_code})")
    except Exception as e:
        print(f"❌ List Clients: Error - {e}")

    # 3. Create Project
    new_project = {
        "client_id": client_id,
        "name": "Test Project",
        "status": "Planned",
        "monthly_fee": 1000.00
    }
    try:
        response = requests.post(f"{BASE_URL}/projects", json=new_project)
        if response.status_code == 200:
            print("✅ Create Project: Success")
        else:
            print(f"❌ Create Project: Failed ({response.status_code}) - {response.text}")
    except Exception as e:
        print(f"❌ Create Project: Error - {e}")

if __name__ == "__main__":
    test_api()
