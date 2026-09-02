from flask import Flask, request, render_template_string
import hashlib, re, random, string, base64, json, os, uuid, html, csv, io
from urllib.parse import quote, unquote, urlparse, parse_qs
from datetime import datetime

app = Flask(__name__)

VISITOR_FILE = "count.txt"
if not os.path.exists(VISITOR_FILE):
    with open(VISITOR_FILE, "w") as f: f.write("1301")
def get_visitors():
    try:
        with open(VISITOR_FILE, "r") as f: c = int(f.read())
    except: c = 1301
    c += 1
    with open(VISITOR_FILE, "w") as f: f.write(str(c))
    return c

TOOLS_LIST = [
    "John Toolkit","MD5 Generator","SHA1 Gen","SHA256 Gen","Base64 Encode","Base64 Decode",
    "URL Encode","URL Decode","Hex Encode","Binary Converter","Password Generator",
    "Pass Strength","My IP Info","User Agent","Word Counter","Char Counter","Uppercase",
    "Lowercase","Reverse Text","Remove Space","Duplicate Remover","JSON Formatter","HTML Escape",
    "Age Calculator","Random Number","UUID Gen","Lorem Ipsum","Morse Code","ROT13",
    "Palindrome Check","Email Validator","Hash Identifier","Slug Generator","Case Swap",
    "MD5 Checker","SHA256 Checker","Color Picker","Binary to Text","Text to Binary",
    "Hex to Text","Text to Hex","CSV to JSON","IP to Binary","Whitespace Cleaner",
    "Regex Tester","QR Text","Credit Luhn","Phone Validator","Pass Length","IP Tracker",
    "Header Viewer","Port Info",
    "Name Style - Fancy Text","UPI QR Generator","Fake Link Checker","Insta Reel Downloader",
    "Phone Info Lookup","YouTube Thumbnail Downloader"
]

def get_youtube_id(url):
    # youtube.com/watch?v=ID, youtu.be/ID, shorts/ID
    try:
        if "youtu.be/" in url:
            return url.split("youtu.be/")[1].split("?")[0].split("&")[0]
        if "v=" in url:
            return parse_qs(urlparse(url).query).get('v',[None])[0]
        if "/shorts/" in url:
            return url.split("/shorts/")[1].split("?")[0]
    except:
        pass
    return None

def phone_info(num):
    num = re.sub(r'\D','',num)
    if len(num) < 10: return "Invalid number, 10 digit dalo"
    # last 10 digit
    last10 = num[-10:]
    # Indian operator logic
    operators = {
        "9": "Jio/Airtel/Vi (Indian)",
        "8": "Jio/Airtel",
        "7": "Jio/Airtel",
        "6": "Jio (New Series)"
    }
    circle_map = {"98":"Delhi","99":"Mumbai","97":"UP","96":"Bihar","95":"Rajasthan","94":"MP","93":"Gujarat","90":"Kolkata"}
    circle = circle_map.get(last10[:2], "India (Approx)")
    op = operators.get(last10[0], "Unknown Indian Operator")
    return f"""📱 Number: +91 {last10}
🌐 Country: India
📡 Operator: {op}
🗺️ Circle/State: {circle}
🔢 Length: {len(num)} digits
✅ Type: Mobile / GSM
⚠️ Note: Ye offline database se hai, 100% accurate ke liye API lagta hai
"""

def process_tool(tid, data):
    data = data.strip()
    if not data: return "Input dalo bhai!"
    try:
        if tid == 0: return "John Ready Format: " + data
        elif tid == 1: return hashlib.md5(data.encode()).hexdigest()
        elif tid == 2: return hashlib.sha1(data.encode()).hexdigest()
        elif tid == 3: return hashlib.sha256(data.encode()).hexdigest()
        elif tid == 4: return base64.b64encode(data.encode()).decode()
        elif tid == 5: return base64.b64decode(data.encode()).decode()
        elif tid == 6: return quote(data)
        elif tid == 7: return unquote(data)
        elif tid == 8: return data.encode().hex()
        elif tid == 9: return ' '.join(format(ord(c), '08b') for c in data)
        elif tid == 10: return ''.join(random.choice(string.ascii_letters+string.digits+"!@#$%") for _ in range(16))
        elif tid == 11:
            s=0
            if len(data)>=8: s+=1
            if re.search(r"[A-Z]",data): s+=1
            if re.search(r"[0-9]",data): s+=1
            if re.search(r"[^A-Za-z0-9]",data): s+=1
            return ["Very Weak","Weak","Medium","Strong","Very Strong"][s]
        elif tid == 12: return f"IP: {request.remote_addr}\nHost: {request.host}"
        elif tid == 13: return request.headers.get('User-Agent','Not Found')
        elif tid == 14: return f"Words: {len(data.split())}"
        elif tid == 15: return f"Chars: {len(data)}"
        elif tid == 16: return data.upper()
        elif tid == 17: return data.lower()
        elif tid == 18: return data[::-1]
        elif tid == 19: return "".join(data.split())
        elif tid == 20: return "\n".join(list(dict.fromkeys(data.splitlines())))
        elif tid == 21: return json.dumps(json.loads(data), indent=2)
        elif tid == 22: return html.escape(data)
        elif tid == 23:
            try:
                d=datetime.strptime(data, "%Y-%m-%d"); today=datetime.now()
                return f"Age: {today.year - d.year} years"
            except: return "Format: YYYY-MM-DD (ex: 2005-08-15)"
        elif tid == 24: return str(random.randint(1, 1000000))
        elif tid == 25: return str(uuid.uuid4())
        elif tid == 26: return "Lorem ipsum dolor sit amet..."
        elif tid == 27: return "Morse:... ---..."
        elif tid == 28: return data.encode('rot13')
        elif tid == 29: return "Palindrome" if data.lower()==data.lower()[::-1] else "Not Palindrome"
        elif tid == 30: return "Valid Email" if re.match(r"[^@]+@[^@]+\.[^@]+", data) else "Invalid Email"
        elif tid == 31: return f"Length {len(data)} - Possible Hash"
        elif tid == 32: return re.sub(r'[^a-z0-9]+', '-', data.lower()).strip('-')
        elif tid == 33: return data.swapcase()
        elif tid in (34,35): return "Demo Checker"
        elif tid == 36: return f"#{''.join(random.choice('0123456789ABCDEF') for _ in range(6))}"
        elif tid == 37: return ''.join(chr(int(b,2)) for b in data.split() if b)
        elif tid == 38: return ' '.join(format(ord(c),'08b') for c in data)
        elif tid == 39: return bytes.fromhex(data).decode(errors='ignore')
        elif tid == 40: return data.encode().hex()
        elif tid == 41:
            f=io.StringIO(data); reader=csv.DictReader(f); return json.dumps(list(reader), indent=2)
        elif tid == 42: return '.'.join(format(int(x),'08b') for x in data.split('.'))
        elif tid == 43: return re.sub(r'\s+',' ',data).strip()
        elif tid == 44: return "Regex Tester - format: pattern|||text"
        elif tid == 45: return f"QR Text: {data}"
        elif tid == 46: return "Valid Card" if len(re.sub(r'\D','',data))>=13 else "Invalid Card"
        elif tid == 47: return "Valid Phone" if len(re.sub(r'\D','',data))==10 else "Invalid Phone"
        elif tid == 48: return f"Length: {len(data)}"
        elif tid == 49: return
