# -*- coding: utf-8 -*-
"""
Test client for I Ching Divination API
"""

import requests
import time
import json

API_URL = "http://localhost:8000/api/v1"

def test_api_health():
    """Test the API health endpoint"""
    response = requests.get(f"{API_URL}/health")
    print(f"Health check status code: {response.status_code}")
    if response.status_code == 200:
        print("API is healthy!")
        return True
    else:
        print("API health check failed!")
        return False

def test_divination():
    """Test the divination endpoint"""
    start_time = time.time()
    
    payload = {
        "question": "Tôi có nên thay đổi sự nghiệp trong năm nay không?",
    }
    
    print(f"Sending request with question: {payload['question']}")
    response = requests.post(f"{API_URL}/divination", json=payload)
    
    elapsed_time = time.time() - start_time
    print(f"Request completed in {elapsed_time:.2f} seconds")
    
    if response.status_code == 200:
        result = response.json()
        print(f"Status Code: {response.status_code}")
        print(f"Hexagram: {result['hexagram']['number']} - {result['hexagram']['name']}")
        print(f"Topic: {result['topic']}")
        print("\nInterpretation preview:")
        print(result['interpretation'][:200] + "...")
        return True
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        return False

if __name__ == "__main__":
    print("=== I CHING DIVINATION API TEST CLIENT ===")
    
    # Wait for API to start
    print("Waiting for API to start (5 seconds)...")
    time.sleep(5)
    
    # Test health endpoint
    if not test_api_health():
        print("API is not responsive. Make sure it's running.")
        exit(1)
    
    print("\n=== TESTING DIVINATION ENDPOINT ===")
    test_divination()
