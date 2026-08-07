#!/usr/bin/env python3
"""
Rolex Price API - End-to-End Endpoint Smoke Test Script

Validates status codes and payload schema fields against a target base URL
(local Docker container or deployed AWS API Gateway endpoint).
"""

import sys
import time
import argparse
import urllib.request
import urllib.error
import json


def test_endpoint(url: str, check_type: str, timeout: int = 120) -> bool:
    print(f"Testing GET {url} (Timeout: {timeout}s)...")
    start_time = time.time()
    
    while time.time() - start_time < timeout:
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "SmokeTest/1.0"})
            with urllib.request.urlopen(req, timeout=10) as response:
                status_code = response.getcode()
                if status_code == 200:
                    body_bytes = response.read()
                    data = json.loads(body_bytes.decode("utf-8"))
                    
                    is_valid = False
                    if check_type == "health":
                        is_valid = (
                            data.get("status") == "healthy"
                            and data.get("watches_loaded", 0) > 0
                        )
                    elif check_type == "watches":
                        is_valid = (
                            data.get("total", 0) > 0
                            and len(data.get("items", [])) > 0
                        )
                    elif check_type == "collections":
                        is_valid = (
                            data.get("total_collections", 0) > 0
                            and len(data.get("collections", [])) > 0
                        )
                    elif check_type == "statistics":
                        is_valid = (
                            data.get("total_watches", 0) > 0
                            and "price_stats" in data
                        )
                        
                    if is_valid:
                        elapsed = round(time.time() - start_time, 2)
                        print(f"  ✅ SUCCESS: HTTP 200 - Payload validation passed ({elapsed}s)")
                        return True
                    else:
                        print(f"  ⏳ HTTP 200 received but payload validation failed: {data}")
                else:
                    print(f"  ⏳ Unexpected status code: {status_code}")
        except Exception as err:
            print(f"  ⏳ Connection/HTTP error: {err}")
            
        time.sleep(5)
        
    print(f"  ❌ FAILED: Endpoint {url} did not pass smoke test within {timeout}s.")
    return False


def test_docs_site(docs_url: str, timeout: int = 60) -> bool:
    print(f"Testing S3 Documentation Website {docs_url} (Timeout: {timeout}s)...")
    start_time = time.time()
    
    while time.time() - start_time < timeout:
        try:
            # 1. Test index.html
            index_target = docs_url.rstrip("/") + "/index.html"
            req = urllib.request.Request(index_target, headers={"User-Agent": "SmokeTest/1.0"})
            with urllib.request.urlopen(req, timeout=10) as resp:
                if resp.getcode() == 200:
                    html_content = resp.read().decode("utf-8")
                    if "SwaggerUIBundle" in html_content and "openapi.json" in html_content:
                        # 2. Test openapi.json
                        spec_target = docs_url.rstrip("/") + "/openapi.json"
                        spec_req = urllib.request.Request(spec_target, headers={"User-Agent": "SmokeTest/1.0"})
                        with urllib.request.urlopen(spec_req, timeout=10) as spec_resp:
                            if spec_resp.getcode() == 200:
                                spec_data = json.loads(spec_resp.read().decode("utf-8"))
                                if "openapi" in spec_data and "paths" in spec_data:
                                    elapsed = round(time.time() - start_time, 2)
                                    print(f"  ✅ SUCCESS: S3 Docs Website & Swagger UI validated ({elapsed}s)")
                                    return True
        except Exception as err:
            print(f"  ⏳ Docs site connection/validation error: {err}")
            
        time.sleep(5)
        
    print(f"  ❌ FAILED: S3 Docs Website {docs_url} did not pass smoke test within {timeout}s.")
    return False


def main():
    parser = argparse.ArgumentParser(description="Rolex Price API Smoke Test")
    parser.add_argument("--base-url", required=True, help="Base API URL (e.g. http://localhost:8000 or https://xyz.execute-api.us-east-1.amazonaws.com)")
    parser.add_argument("--docs-url", help="S3 Documentation Website URL to validate")
    parser.add_argument("--timeout", type=int, default=120, help="Per-endpoint timeout in seconds")
    args = parser.parse_args()

    base_url = args.base_url.rstrip("/")
    endpoints = [
        (f"{base_url}/health", "health"),
        (f"{base_url}/watches", "watches"),
        (f"{base_url}/collections", "collections"),
        (f"{base_url}/statistics", "statistics"),
    ]

    print(f"=== STARTING SMOKE TESTS TARGETING {base_url} ===")
    failed_count = 0
    for url, check_type in endpoints:
        if not test_endpoint(url, check_type, timeout=args.timeout):
            failed_count += 1

    if args.docs_url:
        if not test_docs_site(args.docs_url, timeout=args.timeout):
            failed_count += 1

    if failed_count > 0:
        print(f"\n❌ ERROR: {failed_count} smoke test(s) failed.")
        sys.exit(1)
    else:
        print("\n✅ ALL SMOKE TESTS PASSED SUCCESSFULLY.")
        sys.exit(0)


if __name__ == "__main__":
    main()
