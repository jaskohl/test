
# Category 20: Security & Penetration Testing

**Test Count**: 7 tests  
**Hardware**: Device Only  
**Priority**: HIGH  
**Series**: Both Series 2 and 3  

Based on COMPLETE_TEST_LIST.md Section 20. This file contains basic security and penetration tests.

---

## 20.1-20.2: Authentication Security

### 20.1.1: Password not stored in DOM
- **Purpose**: To verify that the user's password is not stored in the page's DOM (Document Object Model) in plain text.
- **Test Steps**:
    1. Enters the password into the password field.
    2. Checks that the input field's type is `password`.
    3. Scans the page's HTML content to ensure the password string is not present.

### 20.1.2: Brute force protection (rate limiting)
- **Purpose**: To test if the device implements rate limiting or other protections against brute-force login attacks.
- **Test Steps**: Attempts to log in with an incorrect password multiple times in a loop.
- **Note**: This test is skipped and requires manual verification, as the specific rate-limiting mechanism (e.g., account lockout, CAPTCHA) can vary.

---

## 20.3-20.4: Session Security

### 20.3.1: Session expires after 5 minutes
- **Purpose**: To verify that user sessions automatically time out after a period of inactivity (e.g., 5 minutes).
- **Test Steps**: Logs in, waits for 5.5 minutes, and then attempts to access a protected page.
- **Note**: This test is slow and is skipped in automated runs. It expects a redirect to the login page after the timeout.

### 20.3.2: Session ID changes after login
- **Purpose**: To verify that the session ID is regenerated upon successful login to prevent session fixation attacks.
- **Test Steps**:
    1. Captures the browser cookies before logging in.
    2. Logs in.
    3. Captures the browser cookies again after logging in.
- **Assertion**: The test expects the session cookie's value to be different before and after login.

---

## 20.4-20.5: Input Validation Security

### 20.4.1: SQL injection attempts rejected
- **Purpose**: To test if the application is vulnerable to basic SQL injection attacks.
- **Test Steps**: Enters a common SQL injection payload (e.g., `'; DROP TABLE users; --`) into a text field and saves the form.
- **Assertion**: The test asserts that the device continues to function normally, implying the input was properly sanitized.

### 20.4.2: XSS attempts rejected
- **Purpose**: To test if the application is vulnerable to basic Cross-Site Scripting (XSS) attacks.
- **Test Steps**: Enters a common XSS payload (e.g., `<script>alert('XSS')</script>`) into a text field and saves the form.
- **Assertion**: The test expects that no JavaScript alert is triggered, implying the input was properly sanitized.

---

## 20.6: HTTPS Security

### 20.6.1: HTTPS connection available
- **Purpose**: To check if the device offers a secure HTTPS connection.
- **Test Steps**: Attempts to connect to the device's base URL using the `https://` protocol.
- **Note**: This test is skipped if an HTTPS connection cannot be established, as it may not be configured on the device.

---

## 20.7: Directory Traversal Prevention

### 20.7.1: Directory traversal attempts blocked
- **Purpose**: To test if the web server is vulnerable to directory traversal attacks.
- **Test Steps**: Attempts to navigate to URLs containing directory traversal payloads (e.g., `../../../etc/passwd`).
- **Assertion**: The test expects that these attempts will be blocked, resulting in a redirect or an error page rather than exposing sensitive files.
