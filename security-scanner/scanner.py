import requests

print("=== Website Security Scanner by Vicky ===")
target = input("Enter website URL: ")

# XSS Check
payload = "<script>alert(1)</script>"
try:
    r = requests.get(target + f"?q={payload}", timeout=5)
    if payload in r.text:
        print(f"[!] XSS Possible: {target}?q={payload}")
    else:
        print("[OK] No XSS found")
except:
    print("[Error] Could not connect")

# Open Redirect Check
test_url = target + "?next=https://evil.com"
try:
    res = requests.get(test_url, allow_redirects=False, timeout=5)
    if "evil.com" in res.headers.get("Location", ""):
        print(f"[!] Open Redirect Possible: {test_url}")
    else:
        print("[OK] No Open Redirect")
except:
    pass

print("Scan Done!")
