from flask import Flask, request
import hashlib, base64, random, string, re, html, json
from urllib.parse import quote, unquote

app = Flask(__name__)
visitors = 1301

TOOLS = [
    "MD5 Generator",
    "SHA256 Generator",
    "Base64 Encode",
    "Base64 Decode",
    "Uppercase Text",
    "Lowercase Text",
    "Reverse Text",
    "Word Counter",
    "Password Generator",
    "Name Style - Fancy",
    "UPI QR Generator",
    "Fake Link Checker",
    "Phone Info Lookup",
    "YouTube Thumbnail",
    "Insta Reel Info",
    "URL Encode",
    "URL Decode",
    "Binary Converter",
    "Age Calculator",
    "Email Validator",
    "My IP Info",
    "User Agent"
]

def run_tool(i, text):
    t = text.strip()
    if not t: return "Kuch likh to sahi bhai!"
    try:
        if i==0: return hashlib.md5(t.encode()).hexdigest()
        if i==1: return hashlib.sha256(t.encode()).hexdigest()
        if i==2: return base64.b64encode(t.encode()).decode()
        if i==3:
            try: return base64.b64decode(t.encode()).decode()
            except: return "Galat Base64 hai!"
        if i==4: return t.upper()
        if i==5: return t.lower()
        if i==6: return t[::-1]
        if i==7: return f"Words: {len(t.split())}\nChars: {len(t)}\nLines: {len(t.splitlines())}"
        if i==8: return ''.join(random.choice(string.ascii_letters+string.digits+"@#$%") for _ in range(12))
        if i==9:
            return f"1. Bold: {t.upper()}\n2. Fancy: {' '.join('𝕍𝕀ℂ𝕂𝕐'[ord(c.lower())-97] if c.isalpha() and ord(c.lower())-97<5 else c for c in t)}\n3. Small: {t.lower()}\n4. Reverse Fancy: {t[::-1]}\n5. Leet: {t.replace('a','4').replace('e','3').replace('i','1').replace('o','0')}"
        if i==10:
            # UPI: upi_id|name|amount
            parts = t.split("|")
            upi = parts[0].strip()
            name = parts[1].strip() if len(parts)>1 else "Vicky"
            amt = parts[2].strip() if len(parts)>2 else "100"
            link = f"upi://pay?pa={upi}&pn={quote(name)}&am={amt}&cu=INR"
            return f"UPI ID: {upi}\nName: {name}\nAmount: Rs.{amt}\n\nLINK:\n{link}\n\nIs link ka QR banao Google QR Generator se"
        if i==11:
            bad = ["bit.ly","tinyurl","free-money","lottery","verify-account",".tk","exe"]
            found = [b for b in bad if b in t.lower()]
            if found: return f"⚠️ FAKE LINK! Mila: {found}\nLink: {t}"
            if not t.startswith("https"): return f"⚠️ No HTTPS! Risky: {t}"
            return f"✅ SAFE lag raha hai: {t}"
        if i==12:
            num = re.sub(r'\D','',t)[-10:]
            if len(num)!=10: return "10 digit number dalo"
            return f"Number: +91 {num}\nCountry: India\nOperator: Jio/Airtel/Vi (Indian Series)\nType: Mobile GSM\nCircle: {num[:2]} Series"
        if i==13:
            # youtube
            vid = ""
            if "youtu.be/" in t: vid = t.split("youtu.be/")[1].split("?")[0].split("&")[0]
            elif "v=" in t:
                import urllib.parse
                qs = urllib.parse.parse_qs(urllib.parse.urlparse(t).query)
                vid = qs.get('v',[''])[0]
            elif "/shorts/" in t: vid = t.split("/shorts/")[1].split("?")[0]
            else: vid = t.strip()
            if not vid: return "Link galat hai! Ex: https://youtu.be/dQw4w9WgXcQ"
            return f"Video ID: {vid}\n\n1. MAX HD:\nhttps://img.youtube.com/vi/{vid}/maxresdefault.jpg\n\n2. HQ:\nhttps://img.youtube.com/vi/{vid}/hqdefault.jpg\n\n3. MQ:\nhttps://img.youtube.com/vi/{vid}/mqdefault.jpg"
        if i==14: return f"Reel Link: {t}\n\nSaveInsta.app ya SnapInsta.app pe jao, ye link paste karo, HD download ho jayega."
        if i==15: return quote(t)
        if i==16: return unquote(t)
        if i==17: return ' '.join(format(ord(c),'08b') for c in t)
        if i==18: return "Format: YYYY-MM-DD likho\nEx: 2005-01-01"
        if i==19:
            return "Valid Email ✅" if re.match(r"[^@]+@[^@]+\.[^@]+", t) else "Invalid Email ❌"
        if i==20: return f"IP: {request.remote_addr}\nHost: {request.host}"
        if i==21: return request.headers.get('User-Agent','Not Found')
    except Exception as e:
        return f"Error: {e}"
    return "Done"

@app.route('/', methods=['GET'])
def home():
    global visitors
    visitors += 1
    html_page = f"""
<html><head><meta name="viewport" content="width=device-width,initial-scale=1">
<style>
body{{margin:0;padding:10px;background:#0a0a0a;color:#fff;font-family:Arial}}
.top{{border:2px solid #ffcc00;border-radius:20px;padding:15px;text-align:center;background:#111}}
.top h1{{color:#ffcc00;margin:0;font-size:20px}}
.grid{{display:grid;grid-template-columns:repeat(2,1fr);gap:8px;margin-top:12px}}
.card{{border:1px solid #333;padding:12px;text-align:center;background:#151515;border-radius:12px}}
.card a{{color:#ffcc00;text-decoration:none;font-weight:bold;font-size:12px}}
.footer{{margin-top:20px;border:2px solid #ffcc00;border-radius:15px;padding:15px;text-align:center;background:#111}}
.badge{{border:1px solid #ffcc00;border-radius:15px;padding:5px 10px;margin:3px;display:inline-block;font-size:11px;color:#ffcc00}}
</style></head><body>
<div class="top"><h1>⚡ CYB3R TOOLS - 22 IN 1 ⚡</h1><p style="color:#888;font-size:11px">MADE BY VICKY CHAUHAN</p></div>
<div class="grid">
"""
    for idx, name in enumerate(TOOLS):
        html_page += f'<div class="card"><a href="/tool/{idx}">{idx+1}. {name}</a></div>'
    html_page += f"""
</div>
<div class="footer">
<h3 style="color:#ffcc00;margin:0">⚡ MADE BY VICKY CHAUHAN ⚡</h3>
<span class="badge">👁️ Visitors: {visitors}</span>
<span class="badge">🟢 ONLINE</span><br>
<span class="badge">© 2026 CYB3R TOOLS</span>
</div>
</body></html>
"""
    return html_page

@app.route('/tool/<int:tid>', methods=['GET','POST'])
def tool(tid):
    if tid<0 or tid>=len(TOOLS): return "Not Found",404
    name = TOOLS[tid]
    inp = ""
    out = ""
    if request.method == 'POST':
        inp = request.form.get('data','')
        out = run_tool(tid, inp)

    return f"""
<html><head><meta name="viewport" content="width=device-width,initial-scale=1">
<style>
body{{background:#0a0a0a;color:#fff;font-family:Arial;display:flex;justify-content:center;padding:10px;margin:0}}
.box{{border:2px solid #ffcc00;padding:15px;width:100%;max-width:500px;border-radius:15px;background:#111}}
textarea{{width:100%;padding:10px;background:#000;color:#fff;border:1px solid #333;border-radius:10px;box-sizing:border-box}}
button{{background:#ffcc00;color:#000;font-weight:bold;padding:12px;width:100%;border:none;border-radius:10px;margin-top:10px}}
pre{{background:#000;color:#ffcc00;padding:10px;border-left:3px solid #ffcc00;border-radius:8px;white-space:pre-wrap;word-break:break-all;margin-top:10px}}
a{{color:#ffcc00;text-decoration:none}}
.hint{{color:#888;font-size:11px;margin:5px 0}}
</style></head><body>
<div class="box">
<a href="/">← Back</a>
<h2 style="color:#ffcc00">{name}</h2>
<div class="hint">Input niche dalo aur RUN dabao</div>
<form method="POST">
<textarea name="data" rows="4" placeholder="Yaha likho...">{inp}</textarea>
<button type="submit">RUN {name}</button>
</form>
<pre>{out if out else 'Result yaha ayega...'}</pre>
</div>
</body></html>
"""

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
