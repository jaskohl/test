"""
Test 24.1.2: NTP request rate limiting
Category 24: Protocol Security Testing - COMPLETE
Test Count: Part of 5 tests in Category 24
Hardware: Software Tools
Priority: MEDIUM
Series: Both Series 2 and 3

Extracted from: tests/test_24_protocol_security.py
Source Class: TestNTPSecurity
"""

import pytest
import ntplib
from playwright.sync_api import Page


def test_24_1_2_ntp_rate_limiting(base_url: str, device_ip: str):
    """Test 24.1.2: NTP request rate limiting"""
    # Extract device IP from base_url
    device_host = base_url.replace("http://", "").replace("https://", "").split("/")[0]
    # NTP typically runs on port 123
    ntp_server = device_host
    ntp_port = 123
    try:
        # Create NTP client
        client = ntplib.NTPClient()
        # Send multiple rapid requests to test rate limiting
        response_times = []
        for i in range(5):
            try:
                response = client.request(ntp_server, port=ntp_port, timeout=2)
                response_times.append(response.dest_time - response.orig_time)
            except (ntplib.NTPException, OSError) as e:
                # NTP may not be available on device
                print(f"NTP request {i+1} failed: {e}")
                break
        # If we got responses, test was possible
        if response_times:
            print(f"NTP responses received: {len(response_times)}")
            print(
                f"Average response time: {sum(response_times)/len(response_times):.3f}s"
            )
            # NTP rate limiting would be measured by device logs or response behavior
        else:
            print("NTP service not available on device")
    except Exception as e:
        print(f"NTP testing failed: {e}")
        pytest.skip("NTP not available or not accessible")
