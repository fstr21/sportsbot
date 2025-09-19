#!/usr/bin/env python3
"""Check SportsGameOdds API usage for keys in .env.local (including commented ones)."""

import json
import os
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Tuple

import requests

# Configuration
DEFAULT_BASE_URL = "https://api.sportsgameodds.com/v2"
ENV_FILE = Path(".env.local")
USER_AGENT = "sportsbot-local-usage-check/1.0"


class UsageError(RuntimeError):
    """Custom error for usage script issues."""


def parse_env_file() -> List[Tuple[str, str, str, bool]]:
    """Parse .env.local for all SPORTSGAMEODDS_API_KEY entries (commented and uncommented).

    Returns list of tuples: (email, status, api_key, is_active)
    """
    if not ENV_FILE.exists():
        raise UsageError(f"{ENV_FILE} not found")

    api_keys = []

    for line_num, raw_line in enumerate(ENV_FILE.read_text(encoding="utf-8").splitlines(), 1):
        line = raw_line.strip()

        # Skip empty lines and non-API key lines
        if not line or "SPORTSGAMEODDS_API_KEY" not in line:
            continue

        # Parse commented lines like: #email@domain.com STATUS SPORTSGAMEODDS_API_KEY=key
        # Parse active lines like: SPORTSGAMEODDS_API_KEY=key

        is_active = not line.startswith("#")

        if line.startswith("#"):
            # Parse commented line
            # Pattern: #email STATUS SPORTSGAMEODDS_API_KEY=key
            match = re.match(r'#([^@\s]+@[^@\s]+)\s+(\w+)\s+SPORTSGAMEODDS_API_KEY=([a-f0-9]+)', line)
            if match:
                email, status, api_key = match.groups()
                api_keys.append((email, status, api_key, is_active))
        else:
            # Parse active line
            if "=" in line:
                key, value = line.split("=", 1)
                if key.strip() == "SPORTSGAMEODDS_API_KEY":
                    api_key = value.strip()
                    # Try to find associated comment above
                    email = "unknown"
                    status = "ACTIVE"
                    api_keys.append((email, status, api_key, is_active))

    return api_keys


def fetch_usage_data(base_url: str, api_key: str) -> Dict[str, Any]:
    """Fetch usage data from the SportsGameOdds API."""
    headers = {
        "X-API-Key": api_key,
        "Accept": "application/json",
        "User-Agent": USER_AGENT,
    }

    try:
        response = requests.get(
            f"{base_url.rstrip('/')}/account/usage",
            headers=headers,
            timeout=30,
        )
    except requests.RequestException as exc:
        raise UsageError(f"Failed to contact API: {exc}")

    if response.status_code == 401:
        return {"error": "Invalid API key", "status_code": 401}
    elif response.status_code == 403:
        return {"error": "Access forbidden", "status_code": 403}
    elif response.status_code == 404:
        return {"error": "Usage endpoint not found", "status_code": 404}
    elif response.status_code == 429:
        return {"error": "Rate limited", "status_code": 429}
    elif response.status_code != 200:
        return {"error": f"HTTP {response.status_code}", "status_code": response.status_code}

    try:
        return response.json()
    except ValueError:
        return {"error": "Invalid JSON response", "status_code": response.status_code}


def get_usage_summary(data: Dict[str, Any]) -> Dict[str, Any]:
    """Extract key usage info from API response."""
    if "error" in data:
        return {"status": "ERROR", "message": data["error"]}

    if not data.get("success"):
        return {"status": "ERROR", "message": "API request failed"}

    account_data = data.get("data", {})
    rate_limits = account_data.get("rateLimits", {})
    monthly = rate_limits.get("per-month", {})

    email = account_data.get("email", "unknown")
    tier = account_data.get("tier", "unknown")
    is_active = account_data.get("isActive", False)

    max_entities = monthly.get("max-entities")
    current_entities = monthly.get("current-entities", 0)

    if max_entities == "unlimited":
        usage_pct = 0
        remaining = "unlimited"
        status = "UNLIMITED"
    else:
        max_entities = int(max_entities)
        remaining = max_entities - current_entities
        usage_pct = (current_entities / max_entities * 100) if max_entities > 0 else 0

        if current_entities > max_entities:
            status = "OVER_QUOTA"
        elif usage_pct > 80:
            status = "HIGH_USAGE"
        else:
            status = "GOOD"

    return {
        "status": status,
        "email": email,
        "tier": tier,
        "is_active": is_active,
        "current": current_entities,
        "max": max_entities,
        "remaining": remaining,
        "usage_pct": usage_pct
    }


def main():
    """Main entry point."""
    base_url = os.getenv("SPORTSGAMEODDS_BASE_URL", DEFAULT_BASE_URL)

    print("=== SportsGameOdds API Key Status Check (.env.local) ===")
    print()

    try:
        # Parse all API keys from .env.local
        api_keys = parse_env_file()

        if not api_keys:
            print("No SPORTSGAMEODDS_API_KEY entries found in .env.local")
            return

        print(f"Found {len(api_keys)} API key(s) in {ENV_FILE}")
        print()

        # Test each API key
        results = []
        for i, (email, noted_status, api_key, is_active) in enumerate(api_keys, 1):
            print(f"[{i}] Testing {email} ({noted_status}) - {api_key[:8]}...{api_key[-4:]}")

            if is_active:
                print("    STATUS: Currently ACTIVE in .env.local")
            else:
                print("    STATUS: Currently commented out")

            # Test the API key
            response = fetch_usage_data(base_url, api_key)
            usage = get_usage_summary(response)

            if usage["status"] == "ERROR":
                print(f"    RESULT: {usage['message']}")
                actual_status = "DEAD"
            else:
                print(f"    RESULT: {usage['email']} ({usage['tier']}) - {usage['current']}/{usage['max']} entities")
                if usage["status"] == "OVER_QUOTA":
                    print(f"    WARNING: OVER QUOTA! ({usage['current']} > {usage['max']})")
                    actual_status = "OVER_QUOTA"
                elif usage["status"] == "HIGH_USAGE":
                    print(f"    WARNING: High usage ({usage['usage_pct']:.1f}%)")
                    actual_status = "HIGH"
                else:
                    print(f"    GOOD: {usage['remaining']} entities remaining ({usage['usage_pct']:.1f}% used)")
                    actual_status = "GOOD"

            # Compare noted vs actual status
            if noted_status != actual_status:
                print(f"    NOTE: .env.local says '{noted_status}' but actual status is '{actual_status}'")

            results.append({
                "email": email,
                "noted_status": noted_status,
                "actual_status": actual_status,
                "is_active": is_active,
                "usage": usage,
                "api_key": api_key
            })

            print()

        # Summary
        print("=== SUMMARY ===")
        good_keys = [r for r in results if r["actual_status"] == "GOOD"]
        dead_keys = [r for r in results if r["actual_status"] == "DEAD"]
        over_quota_keys = [r for r in results if r["actual_status"] == "OVER_QUOTA"]
        high_usage_keys = [r for r in results if r["actual_status"] == "HIGH"]

        print(f"GOOD keys: {len(good_keys)}")
        print(f"DEAD keys: {len(dead_keys)}")
        print(f"OVER QUOTA keys: {len(over_quota_keys)}")
        print(f"HIGH USAGE keys: {len(high_usage_keys)}")

        if good_keys:
            print("\nRECOMMENDED KEYS TO USE:")
            for r in good_keys:
                usage = r["usage"]
                print(f"  {r['email']}: {usage['remaining']} entities remaining")

        active_key = next((r for r in results if r["is_active"]), None)
        if active_key:
            print(f"\nCURRENTLY ACTIVE: {active_key['email']} ({active_key['actual_status']})")

    except UsageError as err:
        print(f"ERROR: {err}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nCancelled by user")
        sys.exit(0)


if __name__ == "__main__":
    main()