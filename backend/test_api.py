#!/usr/bin/env python
"""
Quick API test script to verify backend is working
Run: python test_api.py
"""

import requests
import json

BASE_URL = "http://localhost:8000/api"

def print_response(response):
    """Pretty print response"""
    print(f"Status: {response.status_code}")
    try:
        print(json.dumps(response.json(), indent=2))
    except:
        print(response.text)
    print("-" * 50)

def test_api():
    print("🧪 Testing SmartCommerce API")
    print("=" * 50)
    
    # Test 1: Register user
    print("\n1️⃣  Testing user registration...")
    response = requests.post(f"{BASE_URL}/auth/register/", json={
        "email": "test@example.com",
        "password": "testpass123",
        "password_confirm": "testpass123",
        "first_name": "Test",
        "last_name": "User"
    })
    print_response(response)
    
    if response.status_code == 201:
        data = response.json()
        access_token = data.get('access')
        print(f"✅ Registration successful! Token: {access_token[:20]}...")
    else:
        print("❌ Registration failed")
        return
    
    # Test 2: Get profile
    print("\n2️⃣  Testing get profile...")
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(f"{BASE_URL}/account/profile/", headers=headers)
    print_response(response)
    
    # Test 3: List products
    print("\n3️⃣  Testing list products...")
    response = requests.get(f"{BASE_URL}/products/")
    print_response(response)
    
    # Test 4: Get cart
    print("\n4️⃣  Testing get cart...")
    response = requests.get(f"{BASE_URL}/cart/", headers=headers)
    print_response(response)
    
    # Test 5: Get wishlist
    print("\n5️⃣  Testing get wishlist...")
    response = requests.get(f"{BASE_URL}/wishlist/", headers=headers)
    print_response(response)
    
    print("\n✅ All tests completed!")
    print("\n📝 Note: Some tests may fail if database is empty.")
    print("   Login to admin panel to add categories and products.")

if __name__ == "__main__":
    try:
        test_api()
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to API. Make sure the server is running:")
        print("   docker-compose up -d")
    except Exception as e:
        print(f"❌ Error: {e}")
