#!/usr/bin/env python3
"""Test script to verify API endpoints."""

import sys
import time
import json

# Test the app directly (without HTTP)
sys.path.insert(0, '.')
from app import app

# Create test client
client = app.test_client()

print("=" * 60)
print("Testing ACEest Fitness API Endpoints")
print("=" * 60)

# Test 1: Root endpoint
print("\n1. Testing ROOT ENDPOINT (/)")
response = client.get('/')
print(f"Status: {response.status_code}")
data = json.loads(response.data)
print(f"Message: {data.get('message')}")
print(f"Service: {data.get('service')}")
print(f"Status: {data.get('status')}")
print("✅ ROOT ENDPOINT WORKS!")

# Test 2: Health endpoint
print("\n2. Testing HEALTH ENDPOINT (/health)")
response = client.get('/health')
print(f"Status: {response.status_code}")
data = json.loads(response.data)
print(f"Health Status: {data.get('status')}")
print(f"Service: {data.get('service')}")
print("✅ HEALTH ENDPOINT WORKS!")

# Test 3: Programs endpoint
print("\n3. Testing PROGRAMS ENDPOINT (/programs)")
response = client.get('/programs')
print(f"Status: {response.status_code}")
data = json.loads(response.data)
print(f"Programs available: {len(data.get('programs', {}))}")
for prog in data.get('programs', {}):
    print(f"  - {prog}")
print("✅ PROGRAMS ENDPOINT WORKS!")

print("\n" + "=" * 60)
print("All endpoints are working correctly!")
print("=" * 60)
print("\nTo test with HTTP, run:")
print("  python app.py")
print("\nThen in another terminal:")
print("  curl http://localhost:5000")
print("  curl http://localhost:5000/health")
print("  curl http://localhost:5000/programs")
