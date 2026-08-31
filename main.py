from flask import Flask, request, render_template_string
import hashlib, base64, random, string, secrets, re, urllib.parse

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
<title>CYB3R TOOLS 2.0 - Vicky</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@700&family=Poppins:wght@400;600&display=swap" rel="stylesheet">
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{background:#000;color:#fff;font-family:'Poppins',sans-serif;padding:10px;min-height:100vh;background:radial-gradient(circle at top, #1a0033 0%, #000 60%)}
.header{text-align:center;padding:25px 10px;background:linear-gradient(90deg,#ff00ff,#00ffff,#ff00ff);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;font-family:'Orbitron',sans-serif}
.header h1{font-size:32px;text-shadow:0 0 20px #ff00ff;letter-spacing:2px}
.header p{color:#aaa;font-size:14px;margin-top:5px;-webkit-text-fill-color:#aaa}
.card{background:rgba(255,255,255,0.05);border:1px solid rgba(255,0,255,0.3);padding:18px;margin:16px 0;border-radius:16px;backdrop-filter:blur(10px);box-shadow:0 0 20px rgba(255,0,255,0.1);transition:0.3s}
.card:hover{box-shadow:0 0 30px rgba(0,255,255,0.3);border-color:#00ffff;transform:translateY(-2px)}
.card h2{font-family:'Orbitron';font-size:16px;color:#00ffff;margin-bottom:10px}
input,button{width:100%;padding:12px;margin:6px 0;background:rgba(0,0,0,0.7);color:#fff;border:1px solid #ff00ff;border-radius:10px;font-family:'Poppins'}
button{background:linear-gradient(90deg,#ff00ff,#00ffff);color:#000;font-weight:700;cursor:pointer;font-size:15px;border:none;letter-spacing:1px}
button:hover{transform:scale(1.02);box-shadow:0 0 15px #ff00ff}
.result{background:rgba(0,0,0,0.8);padding:12px;margin-top:10px;border:1px dashed #00ffff;word-break:break-all;border-radius:8px;color:#0f0;font-family:monospace;font-size:13px}
.badge{display:inline-block;background:linear-gradient(90deg,#ff00ff,#00ffff);color:#000;padding:2px 8px;border-radius:20px;font-size:10px;font-weight:bold;margin-left:8px}
img{max-width:100%;border-radius:10px}
.footer{text-align:center;padding:20px;color:#666;font-size:12px;margin-top:20px;border-top:1px solid #222}
.footer span{color:#ff00ff}
</style>
</head>
<body>
<div class="header">
<h1>CYB3R TOOLS 2.0</h1>
<p>10 PREMIUM TOOLS BY VICKY CHAUHAN | VADODARA</p>
</div>

<div class="card"><h2>🔐 Password Generator <span class="badge">POPULAR</span></h2>
<form method="post"><input type="hidden" name="type" value="pass"><button>Generate 16-char Password</button></form>
{% if pass_gen %}<div class="result">{{ pass_gen }}</div>{% endif %}</div>

<div class="card"><h2>🛡️ Strength Checker</h2>
<form method="post"><input type="hidden" name="type" value="strength"><input name="text" placeholder="Enter password" required><button>Check Strength</button></form>
{% if strength %}<div class="result">{{ strength|safe }}</div>{% endif %}</div>

<div class="card"><h2>📱 QR Code Generator <span class="badge">NEW</span></h2>
<form method="post"><input type="hidden" name="type" value="qr"><input name="text" placeholder="Enter link / UPI / text" required><button>Generate QR</button></form>
{% if qr %}<div class="result"><img src="{{ qr }}"><br>Scan Me</div>{% endif %}</div>

<div class="card"><h2>📶 WiFi QR Generator <span class="badge">NEW</span></h2>
<form method="post"><input type="hidden" name="type" value="wifi"><input name="ssid" placeholder="WiFi Name" required><input name="wpass" placeholder="WiFi Password" required><button>Generate WiFi QR</button></form>
{% if wifi_qr %}<div class="result"><img src="{{ wifi_qr }}"><br>Connect directly by scanning</div>{% endif %}</div>

<div class="card"><h2>📸 YouTube Thumbnail</h2>
<form method="post"><input type="hidden" name="type" value="yt"><input name="text" placeholder="Paste YouTube Link" required><button>Get Thumbnail HD</button></form>
{% if yt %}<div class="result"><img src="{{ yt }}"><br><a href="{{ yt }}" target="_blank" style="color:#0ff">Download HD</a></div>{% endif %}</div>

<div class="card"><h2>🖼️ Insta DP Viewer <span class="badge">VIRAL</span></h2>
<form method="post"><input type="hidden" name="type" value="insta"><input name="text" placeholder="Enter Instagram Username" required><button>View DP in HD</button></form>
{% if insta %}<div class="result"><img src="{{ insta }}"><br><a href="{{ insta }}" target="_blank" style="color:#0ff">Open Full Size</a></div>{% endif %}</div>

<div class="card"><h2>🔑 Hash Generator</h2>
<form method="post"><input type="hidden" name="type" value="hash"><input name="text" placeholder="Enter text" required><button>Generate Hash</button></form>
{% if hash_res %}<div class="result">MD5: {{ hash_res.md5 }}<br><br>SHA256: {{ hash_res.sha256 }}</div>{% endif %}</div>

<div class="card"><h2>🔤 Base64 Tool</h2>
<form method="post"><input type="hidden" name="type" value="b64"><input name="text" placeholder="Enter text" required><button>Encode / Decode</button></form>
{% if b64_res %}<div class="result">Enc: {{ b64_res.enc }}<br><br>Dec: {{ b64_res.dec }}</div>{% endif %}</div>

<div class="card"><h2>📍 IP & Device</h2><p style="font-size:12px;color:#aaa">IP: {{ ip }}<br>{{ ua[:100] }}...</p></div>

<div class="card"><h2>👤 Fake Identity</h2>
<form method="post"><input type="hidden" name="type" value="fake"><button>Generate Identity</button></form>
{% if fake %}<div class="result">{{ fake|safe }}</div>{% endif %}</div>

<div class="footer">Made with <span>❤️</span> by Vicky Chauhan | Vadodara, Gujarat<br>Instagram: @vickychauhan | cyb3r-tools.onrender.com<br>2.0 INSTA EDITION</div>
</body>
</html>
"""

def check_strength(pwd):
    score=0
    if len(pwd)>=8: score+=1
    if re.search(r"[A-Z]",pwd): score+=1
    if re.search(r"[0-9]",pwd): score+=1
    if re.search(r"[!@#$%^&*]",pwd): score+=1
    if len(pwd)>=12: score+=1
    levels=["Very Weak ❌","Weak ⚠️","Medium 😐","Strong ✅","Very Strong 🔥","Ultra 💀"]
    return f"{levels[score]} - {score}/5"

@app.route('/', methods=['GET','POST'])
def home():
    pass_gen=hash_res=b64_res=fake=qr=yt=strength=wifi_qr=insta=None
    if request.method=='POST':
        t=request.form.get('type')
        txt=request.form.get('text','').strip()
        if t=='pass':
            alpha=string.ascii_letters+string.digits+"!@#$%^&*"
            pass_gen=''.join(secrets.choice(alpha) for _ in range(16))
        elif t=='strength': strength=check_strength(txt)
        elif t=='hash': hash_res={'md5':hashlib.md5(txt.encode()).hexdigest(),'sha256':hashlib.sha256(txt.encode()).hexdigest()}
        elif t=='b64':
            enc=base64.b64encode(txt.encode()).decode()
            try: dec=base64.b64decode(txt.encode()).decode()
            except: dec="Invalid Base64"
            b64_res={'enc':enc,'dec':dec}
        elif t=='qr': qr=f"https://api.qrserver.com/v1/create-qr-code/?size=400x400&data={urllib.parse.quote(txt)}"
        elif t=='wifi':
            ssid=request.form.get('ssid',''); wpass=request.form.get('wpass','')
            wifi_str=f"WIFI:T:WPA;S:{ssid};P:{wpass};;"
            wifi_qr=f"https://api.qrserver.com/v1/create-qr-code/?size=400x400&data={urllib.parse.quote(wifi_str)}"
        elif t=='yt':
            vid=txt.split("v=")[-1].split("&")[0] if "v=" in txt else txt.split("/")[-1].split("?")[0]
            yt=f"https://img.youtube.com/vi/{vid}/maxresdefault.jpg"
        elif t=='insta':
            insta=f"https://instagram.com/{txt}/" # placeholder logic - real HD needs API, but we show profile link preview
            # Using unavatar for quick HD
            insta=f"https://unavatar.io/instagram/{txt}"
        elif t=='fake':
            fake=f"Name: {random.choice(['Aarav','Vicky','John'])} {random.choice(['Sharma','Singh'])}<br>Email: {''.join(random.choices(string.ascii_lowercase,k=8))}@gmail.com<br>Phone: 9{random.randint(100000000,999999999)}"
    return render_template_string(HTML, pass_gen=pass_gen, hash_res=hash_res, b64_res=b64_res, fake=fake, qr=qr, yt=yt, strength=strength, wifi_qr=wifi_qr, insta=insta, ip=request.headers.get('X-Forwarded-For', request.remote_addr), ua=request.headers.get('User-Agent',''))

if __name__=='__main__': app.run()
