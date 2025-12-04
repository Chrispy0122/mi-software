import requests
import json

API_BASE_URL = "http://127.0.0.1:8000/v1/crm"

def test_create_project():
    print("--- Testing Create Project ---")
    
    # 1. Get existing clients to find a valid ID
    try:
        response = requests.get(f"{API_BASE_URL}/clients")
        clients = response.json()
        print(f"Found {len(clients)} clients.")
        if not clients:
            print("No clients found. Creating one...")
            client_data = {"name": "Test Client", "status": "Active"}
            res = requests.post(f"{API_BASE_URL}/clients", json=client_data)
            client_id = res.json()["id"]
            print(f"Created client with ID: {client_id}")
        else:
            client_id = clients[0]["id"]
            print(f"Using existing client ID: {client_id}")
            
    except Exception as e:
        print(f"Error fetching/creating client: {e}")
        return

    # 2. Try to create a project with VALID client_id
    project_data = {
        "client_id": client_id,
        "name": "Test Project",
        "status": "Planned",
        "monthly_fee": 100.0,
        "currency": "USD"
    }
    print(f"\nSending project data: {project_data}")
    res = requests.post(f"{API_BASE_URL}/projects", json=project_data)
    print(f"Status: {res.status_code}")
    print(f"Response: {res.text}")

    # 3. Try to create a project with INVALID client_id
    print("\n--- Testing Invalid Client ID ---")
    project_data["client_id"] = 999999
    print(f"Sending project data: {project_data}")
    res = requests.post(f"{API_BASE_URL}/projects", json=project_data)
    print(f"Status: {res.status_code}")
    print(f"Response: {res.text}")

if __name__ == "__main__":
    test_create_project()
