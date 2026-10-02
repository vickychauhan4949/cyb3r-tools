import requests
from urllib.parse import urljoin

print("=== Website Security Scanner by Vicky ===")
target = input("Enter URL: ")

# XSS Test
payload = "<script>alert(1)</script>"
r = requests.get(f"{target}?q={payload}", timeout=5)
if payload in r.text:
    print(f"[!] XSS Possible: {target}?q={payload}")
else:
    print("[OK] No XSS")

# Open Redirect Test
for p in ["?url=https://evil.com", "?next=https://evil.com"]:
    url = target + p
    try:
        res = requests.get(url, allow_redirects=False, timeout=5)
        if "evil.com" in res.headers.get("Location",""):
            print(f"[!] Open Redirect: {url}")
    except:
        pass

print("Done!")
