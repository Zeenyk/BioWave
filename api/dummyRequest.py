import requests
from pprint import pprint
from datetime import datetime, timedelta, timezone

BASE_URL = "http://localhost:5000/api"
SHOWCOMPLETELOGS = False

def print_header(title):
    print(f"\n{'='*50}")
    print(f"{title.upper():^50}")
    print(f"{'='*50}")

def test_status():
    print_header("Testing Status Endpoint")
    try:
        response = requests.get(f"{BASE_URL}/status")
        response.raise_for_status()
        print("Current Bioreactor Status:")
        pprint(response.json())
    except Exception as e:
        print(f"Error testing status: {e}")

def test_auth():
    print_header("Testing Authentication")
    try:
        # Test login with correct credentials
        print("\n[1] Testing login with correct credentials")
        response = requests.post(
            f"{BASE_URL}/auth/login",
            json={"username": "admin", "password": "password123"}
        )
        response.raise_for_status()
        token = response.json()["token"]
        headers = {"Authorization": f"Bearer {token}"}
        print("Successfully logged in. Token received.")
        print(f"Token: {token}")

        # Test login with wrong credentials
        print("\n[2] Testing login with wrong credentials")
        try:
            response = requests.post(
                f"{BASE_URL}/auth/login",
                json={"username": "admin", "password": "wrong"}
            )
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            print(f"Expected error received: {e}")

        return headers
    except Exception as e:
        print(f"Error testing auth: {e}")
        return None

def test_control(headers):
    print_header("Testing Control Endpoints")
    if not headers:
        print("No auth headers available - skipping control tests")
        return

    try:
        # Get current status first
        print("\n[1] Current status before changes:")
        response = requests.get(f"{BASE_URL}/status", headers=headers)
        pprint(response.json())

        # Test RPM control
        print("\n[2] Setting RPM to 250")
        response = requests.post(
            f"{BASE_URL}/control",
            json={"command": "set_rpm", "value": 250},
            headers=headers
        )
        response.raise_for_status()
        print("RPM set successfully")

        # Test toggle stirring
        print("\n[3] Toggling stirring")
        response = requests.post(
            f"{BASE_URL}/control",
            json={"command": "toggle_stirring"},
            headers=headers
        )
        response.raise_for_status()
        print("Stirring toggled successfully")

        # Verify changes
        print("\n[4] Current status after changes:")
        response = requests.get(f"{BASE_URL}/status", headers=headers)
        pprint(response.json())

    except Exception as e:
        print(f"Error testing control: {e}")

def test_schedule(headers):
    print_header("Testing Schedule Endpoints")
    if not headers:
        print("No auth headers available - skipping schedule tests")
        return

    try:
        # Get empty schedule
        print("\n[1] Getting current schedule:")
        response = requests.get(f"{BASE_URL}/schedule", headers=headers)
        pprint(response.json())

        # Add a new scheduled operation
        future_time = (datetime.now(timezone.utc) + timedelta(hours=1)).isoformat()
        print(f"\n[2] Adding new schedule for {future_time}")
        response = requests.post(
            f"{BASE_URL}/schedule",
            json={
                "command": "set_rpm",
                "value": 350,
                "time": future_time
            },
            headers=headers
        )
        response.raise_for_status()
        schedule_id = response.json()["id"]
        print(f"Schedule added with ID: {schedule_id}")

        # Verify schedule was added
        print("\n[3] Getting updated schedule:")
        response = requests.get(f"{BASE_URL}/schedule", headers=headers)
        pprint(response.json())

        # Delete the schedule
        print(f"\n[4] Deleting schedule ID {schedule_id}")
        response = requests.delete(
            f"{BASE_URL}/schedule/{schedule_id}",
            headers=headers
        )
        response.raise_for_status()
        print("Schedule deleted successfully")

        # Verify schedule was removed
        print("\n[5] Getting final schedule:")
        response = requests.get(f"{BASE_URL}/schedule", headers=headers)
        pprint(response.json())

    except Exception as e:
        print(f"Error testing schedule: {e}")

def test_logs(headers):
    print_header("Testing Log Endpoints")
    if not headers:
        print("No auth headers available - skipping log tests")
        return

    try:
        # Get recent logs
        print("\n[1] Getting recent logs:")
        response = requests.get(f"{BASE_URL}/logs", headers=headers)
        logs = response.json()
        print(f"Received {len(logs)} log entries")
        print("\nSample log entries:")
        for log in logs[:3]:  # Print first 3 logs as sample
            pprint(log)

        # Test log filtering
        one_hour_ago = (datetime.now(timezone.utc) - timedelta(hours=1)).isoformat()
        print(f"\n[2] Getting logs since {one_hour_ago}:")
        response = requests.get(
            f"{BASE_URL}/logs",
            params={"from": one_hour_ago},
            headers=headers
        )
        filtered_logs = response.json()
        print(f"Received {len(filtered_logs)} filtered log entries")

        # Print the complete logs
        if SHOWCOMPLETELOGS:
            print("\nComplete log entries:")
            pprint(logs)

    except Exception as e:
        print(f"Error testing logs: {e}")

def test_logout(headers):
    print_header("Testing Logout")
    if not headers:
        print("No auth headers available - skipping logout test")
        return

    try:
        print("\n[1] Logging out current token")
        response = requests.post(
            f"{BASE_URL}/auth/logout",
            headers=headers
        )
        response.raise_for_status()
        print("Logout successful")

        print("\n[2] Verifying token is invalid by trying to access protected endpoint")
        try:
            response = requests.get(f"{BASE_URL}/status", headers=headers)
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            print(f"Expected error received: {e} - token is now invalid")

    except Exception as e:
        print(f"Error testing logout: {e}")

if __name__ == '__main__':
    test_status()
    headers = test_auth()
    test_control(headers)
    test_schedule(headers)
    test_logs(headers)
    test_logout(headers)
    print_header("All Tests Completed")