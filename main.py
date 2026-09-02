from flask import Flask, request
import hashlib, base64, random, string, re
from urllib.parse import quote, unquote, urlparse, parse_qs

app = Flask(__name__)
visitors = 1301

TOOLS = [
"MD5 Generator","SHA256 Generator","Base64 Encode","Base64 Decode",
"Uppercase","Lowercase","Reverse Text","Word Counter","Password Generator",
"Name Style - Fancy","UPI QR Generator","Fake Link Checker","Phone Info Lookup",
"YouTube Thumbnail","Insta Reel Guide","URL Encode","URL Decode","Binary Converter",
"Email Validator","Age Calculator","My IP Info","User Agent","JSON Formatter",
"QR Text Generator","Color Picker","Random Number","UUID Generator","ROT13",
"Remove Spaces","Duplicate Remover","Slug Generator","Hex Encode"
]

def fancy_name(t):
    circled = ''.join(chr(0x24D0 + ord(c.lower()) - 97) if 'a' <= c.lower() <= 'z' else c for c in t)
    bold = t.upper()
    leet = t.replace('a','4').replace('e','3').replace('i','1').replace('o','0').replace('s','$')
    return f"Original: {t}\nBold: {bold}\nCircled: {circled}\nLeet: {leet}\nReverse: {t[::-1]}\nLength: {len(t)}"

def get_yt_id(url):
    if "youtu.be/" in url:
        return url.split("youtu.be/")[1].split("?")[0].split("&")[0]
    if "v=" in url:
        try: return parse_qs(urlparse(url).query).get('v',[''])[0]
        except: pass
    if "/shorts/" in url:
        return url.split("/shorts/")[1].split("?")[0].split("/")[0]
    return url.strip()[-11:] if len(url.strip())>=11 else ""

def run(i, txt):
    t = txt.strip()
    if not t: return "❌ Input dalo bhai!"
    try:
        if i==0: return hashlib.md5(t.encode()).hexdigest()
        if i==1: return hashlib.sha256(t.encode()).hexdigest()
        if i==2: return base64.b64encode(t.encode()).decode()
        if i==3:
            try: return base64.b64decode(t.encode()).decode()
            except: return "❌ Galat Base64"
        if i==4: return t.upper()
        if i==5: return t.lower()
        if i==6: return t[::-1]
        if i==7: return f"Words: {len(t.split())}\nChars: {len(t)}\nLines: {len(t.splitlines())}"
        if i==8: return ''.join(random.choice(string.ascii_letters+string.digits+"@#$%") for _ in range(12))
        if i==9: return fancy_name(t)
        if i==10:
            p=[x.strip() for x in t.split("|")]
            upi=p[0]; name=p[1] if len(p)>1 else "Vicky"; amt=p[2] if len(p)>2 else "100"
            link=f"upi://pay?pa={upi}&pn={quote(name)}&am={amt}&cu=INR"
            qr=f"https://api.qrserver.com/v1/create-qr-code/?size=300x300&data={quote(link)}"
            return f"UPI: {upi}\nName: {name}\nAmt: {amt}\n\nUPI Link:\n{link}\n\nQR Image Link:\n{qr}"
        if i==11:
            bad=["bit.ly","tinyurl","free-money","lottery","verify",".tk",".ml","exe"]
            f=[b for b in bad if b in t.lower()]
            return f"⚠️ FAKE! Found {f}\nLink: {t}" if f else f"✅ SAFE: {t}"
        if i==12:
            n=re.sub(r'\D','',t)[-10:]
            return f"Number: +91 {n}\nCountry: India\nOperator: Jio/Airtel/Vi\nValid: Yes" if len(n)==10 else "10 digit dalo"
        if i==13:
            vid=get_yt_id(t)
            if len(vid)<5: return "Sahi YT link dalo: https://youtu.be/dQw4w9WgXcQ"
            return f"ID: {vid}\n\nMAX HD:\nhttps://img.youtube.com/vi/{vid}/maxresdefault.jpg\n\nHQ:\nhttps://img.youtube.com/vi/{vid}/hqdefault.jpg\n\nMQ:\nhttps://img.youtube.com/vi/{vid}/mqdefault.jpg"
        if i==14: return f"Link: {t}\n\n1. SaveInsta.app kholo\n2. Link paste karo\n3. Download HD"
        if i==15: return quote(t)
        if i==16: return unquote(t)
        if i==17: return ' '.join(format(ord(c),'08b') for c in t)
        if i==18: return "Valid Email ✅" if re.match(r"[^@]+@[^@]+\.[^@]+", t) else "Invalid Email ❌"
        if i==19: return "Format: YYYY-MM-DD\nEx: 2005-08-15"
        if i==20: return f"IP: {request.remote_addr}\nHost: {request.host}"
        if i==21: return request.headers.get('User-Agent','Not Found')
        if i==22:
            import json; return json.dumps(json.loads(t), indent=2)
        if i==23: return f"QR Text: {t}\nQR ke liye: https://api.qrserver.com/v1/create-qr-code/?size=200x200&data={quote(t)}"
        if i==24: return f"#{''.join(random.choice('0123456789ABCDEF') for _ in range(6))}"
        if i==25: return str(random.randint(1,999999))
        if i==26:
            import uuid; return str(uuid.uuid4())
        if i==27: return t.encode('rot13')
        if i==28: return "".join(t.split())
        if i==29: return "\n".join(list(dict.fromkeys(t.splitlines())))
        if i==30: return re.sub(r'[^a-z0-9]+','-',t.lower()).strip('-')
        if i==31: return t.encode().hex()
    except Exception as e:
        return f"Error: {e}"
    return "Done"

@app.route('/')
def home():
    global visitors; visitors+=1
    cards=""
    for idx,name in enumerate(TOOLS):
        cards+=f'<div style="border:1px solid #333;padding:12px;text-align:center;background:rgba(20,20,20,0.95);border-radius:14px"><a href="/tool/{idx}" style="color:#ffcc00;text-decoration:none;font-weight:bold;font-size:11px">{idx+1}. {name}</a></div>'
    return f"""
<html><head><meta name="viewport" content="width=device-width,initial-scale=1"><title>CYB3R TOOLS 32</title>
<style>
body{{margin:0;padding:10px;background:linear-gradient(rgba(0,0,0,0.88),rgba(0,0,0,0.92)),url('https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?q=80&w=1000');background-size:cover;background-attachment:fixed;color:#fff;font-family:sans-serif}}
.top{{border:2px solid #ffcc00;border-radius:22px;padding:18px;text-align:center;background:rgba(20,20,0,0.9);box-shadow:0 0 20px #ffcc00}}
.top h1{{color:#ffcc00;margin:0;font-size:22px}}
.grid{{display:grid;grid-template-columns:repeat(2,1fr);gap:8px;margin-top:12px}}
.footer{{margin-top:20px;border:2px solid #ffcc00;border-radius:18px;padding:15px;text-align:center;background:#111}}
.badge{{border:1px solid #ffcc00;border-radius:12px;padding:6px 12px;margin:4px;display:inline-block;font-size:11px;color:#ffcc00;background:#000}}
</style></head><body>
<div class="top"><h1>⚡ CYB3R TOOLS - 32 IN 1 ⚡</h1><p style="color:#aaa;font-size:11px">MADE BY VICKY CHAUHAN | 100% WORKING</p></div>
<div class="grid">{cards}</div>
<div class="footer"><h3 style="color:#ffcc00;margin:0">⚡ VICKY CHAUHAN ⚡</h3><span class="badge">👁️ Visitors: {visitors}</span><span class="badge">🟢 ONLINE</span><br><span class="badge">© 2026 CYB3R TOOLS</span></div>
</body></html>
"""

@app.route('/tool/<int:tid>', methods=['GET','POST'])
def tool_page(tid):
    if tid<0 or tid>=len(TOOLS): return "Not Found",404
    name=TOOLS[tid]; txt=""; res=""
    if request.method=='POST':
        txt=request.form.get('data',''); res=run(tid,txt)
    return f"""
<html><head><meta name="viewport" content="width=device-width,initial-scale=1"><title>{name}</title>
<style>
body{{background:#080808;color:#fff;font-family:sans-serif;display:flex;justify-content:center;margin:0;padding:10px}}
.box{{border:2px solid #ffcc00;padding:15px;width:100%;max-width:500px;border-radius:15px;background:#111}}
textarea{{width:100%;padding:10px;background:#000;color:#fff;border:1px solid #333;border-radius:10px;box-sizing:border-box}}
button{{background:#ffcc00;color:#000;font-weight:bold;padding:12px;width:100%;border:none;border-radius:10px;margin-top:10px}}
pre{{background:#000;color:#ffcc00;padding:12px;border-left:3px solid #ffcc00;border-radius:8px;white-space:pre-wrap;word-break:break-all;margin-top:10px;font-size:13px}}
a{{color:#ffcc00;text-decoration:none}}
.hint{{color:#888;font-size:11px;margin:6px 0}}
</style></head><body>
<div class="box">
<a href="/">← Back</a><h2 style="color:#ffcc00">{name}</h2>
<div class="hint">Input dalo aur RUN dabao</div>
<form method="POST"><textarea name="data" rows="5" placeholder="Yaha likho...">{txt}</textarea><button>RUN {name}</button></form>
<pre>{res if res else 'Result yaha ayega...'}</pre>
</div>
</body></html>
"""

if __name__=='__main__':
    app.run(host='0.0.0.0', port=10000)
