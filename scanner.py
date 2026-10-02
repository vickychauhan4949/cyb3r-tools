import requests
from urllib.parse import urljoin, urlparse, parse_qs

print("=== Website Security Scanner by You ===")
print("Checks: XSS & Open Redirect\n")

target = input("Enter website URL (e.g. https://example.com): ")

# --- XSS Check ---
print("\n[1] Checking for XSS...")
xss_payload = "<script>alert('XSS')</script>"
test_url = target + "?q=" + xss_payload

try:
    r = requests.get(test_url, timeout=5)
    if xss_payload in r.text:
        print(f" [!] POTENTIAL XSS FOUND at: {test_url}")
    else:
        print(" [OK] No XSS reflection found.")
except Exception as e:
    print(f" [Error] {e}")

# --- Open Redirect Check ---
print("\n[2] Checking for Open Redirect...")
payloads = ["/redirect?url=https://evil.com", "?next=https://evil.com", "?url=https://evil.com"]
found = False
for p in payloads:
    check_url = urljoin(target, p)
    try:
        res = requests.get(check_url, allow_redirects=False, timeout=5)
        if res.status_code in [301, 302] and "evil.com" in res.headers.get("Location", ""):
            print(f" [!] POTENTIAL OPEN REDIRECT at: {check_url}")
            found = True
    except:
        pass

if not found:
    print(" [OK] No Open Redirect found.")

print("\n--- Scan Complete ---")
print("This is a basic scan for educational purposes.")
