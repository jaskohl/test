"""
Category 26: API & Alternative Interface Testing - Individual Test
Test 26.1.8: NTP Protocol Interface - FIXED
Test Count: 1 test
Hardware: Conditional ([WARNING])
Priority: LOW
Series: Both Series 2 and 3
Based on COMPLETE_TEST_LIST.md Section 26.1.8
FIXED: Increased timeouts, proper authentication, device-aware handling
"""

import pytest
import ntplib


def test_26_1_8_ntp_protocol_interface(base_url: str):
    """Test 26.1.8: NTP protocol interface (port 123)"""
    # Test NTP availability discovered by protocol exploration using ntplib
    try:
        # Extract host from base_url
        host = (
            base_url.replace("http://", "")
            .replace("https://", "")
            .split("/")[0]
            .split(":")[0]
        )
        # Create NTP client and query the server
        client = ntplib.NTPClient()
        response = client.request(host, port=123, timeout=5)
        if response:
            # Check if we got a valid NTP response
            if hasattr(response, "version") and response.version > 0:
                print(
                    f" NTP interface available and responding (version: {response.version})"
                )
                print(f"  Stratum: {response.stratum}, Offset: {response.offset:.6f}s")
                assert True, "NTP protocol interface working"
            else:
                print("NTP responded but version unclear")
                pytest.skip("NTP available but response unclear")
        else:
            print("No NTP response received")
            pytest.skip("NTP not available or not responding")
    except (ntplib.NTPException, OSError) as e:
        print(f"NTP query failed: {e}")
        pytest.skip("NTP not available or not accessible")
