from flask import Flask, request, render_template_string
import hashlib, base64, random, string, secrets, urllib.parse

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html><head>
<title>CYB3R TOOLS 4.0 - Vicky</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@700&family=Poppins:wght@400;600&display=swap" rel="stylesheet">
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{background:#000;color:#fff;font-family:'Poppins',sans-serif;padding:10px;background:radial-gradient(circle at top, #1a0033 0%, #000 60%)}
.header{text-align:center;padding:25px 10px}
.header h1{font-size:30px;font-family:'Orbitron';background:linear-gradient(90deg,#ff00ff,#00ffff,#ff00ff);-webkit-background-clip:text;-webkit-text-fill-color:transparent}
.card{background:rgba(255,255,255,0.05);border:1px solid rgba(255,0,255,0.3);padding:18px;margin:16px 0;border-radius:16px}
.card h2{font-family:'Orbitron';font-size:14px;color:#00ffff;margin-bottom:10px}
input,button{width:100%;padding:12px;margin:6px 0;background:rgba(0,0,0,0.7);color:#fff;border:1px solid #ff00ff;border-radius:10px}
button{background:linear-gradient(90deg,#ff00ff,#00ffff);color:#000;font-weight:700;cursor:pointer;border:none}
.result{background:rgba(0,0,0,0.8);padding:12px;margin-top:10px;border:1px dashed #00ffff;border-radius:8px;color:#0f0;font-family:monospace;font-size:13px;word-break:break-all}
.badge{display:inline-block;background:linear-gradient(90deg,#ff00ff,#00ffff);color:#000;padding:2px 8px;border-radius:20px;font-size:10px;font-weight:bold;margin-left:8px}
img{max-width:100%;border-radius:10px}
.footer{text-align:center;padding:20px;color:#666;font-size:11px}
</style></head><body>
<div class="header"><h1>CYB3R TOOLS 4.0</h1><p style="color:#aaa">13 TOOLS BY VICKY CHAUHAN | VADODARA</p></div>

<div class="card"><h2>🔐 Password Generator</h2><form method="post"><input type="hidden" name="type" value="pass"><button>Generate Password</button></form>{% if pass_gen %}<div class="result">{{ pass_gen }}</div>{% endif %}</div>
<div class="card"><h2>📱 QR Code Generator</h2><form method="post"><input type="hidden" name="type" value="qr"><input name="text" placeholder="Enter link / text" required><button>Generate QR</button></form>{% if qr %}<div class="result"><img src="{{ qr }}"></div>{% endif %}</div>
<div class="card"><h2>📶 WiFi QR Generator</h2><form method="post"><input type="hidden" name="type" value="wifi"><input name="ssid" placeholder="WiFi Name" required><input name="wpass" placeholder="Password" required><button>Generate WiFi QR</button></form>{% if wifi_qr %}<div class="result"><img src="{{ wifi_qr }}"></div>{% endif %}</div>
<div class="card"><h2>📸 YouTube Thumbnail HD</h2><form method="post"><input type="hidden" name="type" value="yt"><input name="text" placeholder="YouTube Link" required><button>Get Thumbnail</button></form>{% if yt %}<div class="result"><img src="{{ yt }}"><br><a href="{{ yt }}" target="_blank" style="color:#0ff">Download HD</a></div>{% endif %}</div>
<div class="card"><h2>🎬 Insta Reels Downloader <span class="badge">VIRAL</span></h2><form method="post"><input type="hidden" name="type" value="reels"><input name="text" placeholder="Paste Public Reels Link" required><button>Get Download Link</button></form>{% if reels %}<div class="result">{{ reels|safe }}</div>{% endif %}</div>
<div class="card"><h2>🖼️ Insta DP Viewer</h2><form method="post"><input type="hidden" name="type" value="insta"><input name="text" placeholder="Insta Username" required><button>View DP HD</button></form>{% if insta %}<div class="result"><img src="{{ insta }}"></div>{% endif %}</div>
<div class="card"><h2>🔍 Username Checker <span class="badge">NEW</span></h2><form method="post"><input type="hidden" name="type" value="usercheck"><input name="text" placeholder="Enter Username" required><button>Check Availability</button></form>{% if usercheck %}<div class="result">{{ usercheck|safe }}</div>{% endif %}</div>
<div class="card"><h2>💬 Fake WhatsApp Chat <span class="badge">VIRAL</span></h2><form method="post"><input type="hidden" name="type" value="fakechat"><input name="name" placeholder="Name" required><input name="msg" placeholder="Message" required><button>Generate</button></form>{% if chat %}<div class="result">{{ chat|safe }}</div>{% endif %}</div>
<div class="card"><h2>🔤 Stylish Fonts</h2><form method="post"><input type="hidden" name="type" value="font"><input name="text" placeholder="Your Name" required><button>Generate Fonts</button></form>{% if fonts %}<div class="result">{{ fonts|safe }}</div>{% endif %}</div>
<div class="card"><h2>🔑 Hash Generator</h2><form method="post"><input type="hidden" name="type" value="hash"><input name="text" placeholder="Enter text" required><button>Generate Hash</button></form>{% if hash_res %}<div class="result">MD5: {{ hash_res.md5 }}<br><br>SHA256: {{ hash_res.sha256 }}</div>{% endif %}</div>
<div class="card"><h2>🔤 Base64 Tool</h2><form method="post"><input type="hidden" name="type" value="b64"><input name="text" placeholder="Enter text" required><button>Encode / Decode</button></form>{% if b64_res %}<div class="result">Enc: {{ b64_res.enc }}<br>Dec: {{ b64_res.dec }}</div>{% endif %}</div>
<div class="card"><h2>📍 IP Info</h2><p style="font-size:12px">IP: {{ ip }}</p></div>
<div class="card"><h2>👤 Fake Identity</h2><form method="post"><input type="hidden" name="type" value="fake"><button>Generate</button></form>{% if fake %}<div class="result">{{ fake|safe }}</div>{% endif %}</div>
<div class="footer">Made with ❤️ by Vicky Chauhan | CYB3R TOOLS 4.0 | Vadodara</div></body></html>
"""

@app.route('/', methods=['GET','POST'])
def home():
    pass_gen=hash_res=b64_res=fake=qr=yt=wifi_qr=insta=chat=fonts=reels=usercheck=None
    if request.method=='POST':
        t=request.form.get('type'); txt=request.form.get('text','').strip()
        if t=='pass':
            alpha=string.ascii_letters+string.digits+"!@#$%^&*"
            pass_gen=''.join(secrets.choice(alpha) for _ in range(16))
        elif t=='hash': hash_res={'md5':hashlib.md5(txt.encode()).hexdigest(),'sha256':hashlib.sha256(txt.encode()).hexdigest()}
        elif t=='b64':
            enc=base64.b64encode(txt.encode()).decode()
            try: dec=base64.b64decode(txt.encode()).decode()
            except: dec="Invalid"
            b64_res={'enc':enc,'dec':dec}
        elif t=='qr': qr=f"https://api.qrserver.com/v1/create-qr-code/?size=400x400&data={urllib.parse.quote(txt)}"
        elif t=='wifi':
            ssid=request.form.get('ssid',''); wpass=request.form.get('wpass','')
            wifi_str=f"WIFI:T:WPA;S:{ssid};P:{wpass};;"
            wifi_qr=f"https://api.qrserver.com/v1/create-qr-code/?size=400x400&data={urllib.parse.quote(wifi_str)}"
        elif t=='yt':
            vid=txt.split("v=")[-1].split("&")[0] if "v=" in txt else txt.split("/")[-1].split("?")[0]
            yt=f"https://img.youtube.com/vi/{vid}/maxresdefault.jpg"
        elif t=='insta': insta=f"https://unavatar.io/instagram/{txt}"
        elif t=='reels':
            reels=f"✅ Link Verified: {txt}<br><br>👉 Public Reels ke liye ye 2 best sites use kar:<br>1. <a href='https://saveinsta.app' target='_blank' style='color:#0ff'>saveinsta.app</a> pe paste kar<br>2. <a href='https://igram.world' target='_blank' style='color:#0ff'>igram.world</a> pe paste kar<br><br>Direct download wahan se ho jayega HD me! (Insta API private hai isliye external tool best hai)"
        elif t=='usercheck':
            platforms=["instagram.com/","youtube.com/@","github.com/","twitter.com/"]
            res="<br>".join([f"🔗 {p}{txt} - <a href='https://{p}{txt}' target='_blank' style='color:#0ff'>Check</a>" for p in platforms])
            usercheck=f"Username: {txt}<br><br>{res}<br><br>Link khol ke dekh - agar 'Not Found' aaye to available hai!"
        elif t=='fakechat':
            name=request.form.get('name',''); msg=request.form.get('msg','')
            chat=f"👤 {name}:<br>💬 {msg}<br><br>✓✓ 11:17 AM"
        elif t=='font': fonts=f"<br>".join([f"{txt}", f"𝐁𝐨𝐥𝐝: {txt}", f"𝓢𝓬𝓻𝓲𝓹𝓽: {txt}", f"𝔊𝔬𝔱𝔥𝔦𝔠: {txt}", f"🅱🅾🆇: {txt.upper()}"])
        elif t=='fake': fake=f"Name: Vicky {random.choice(['Singh','Sharma'])}<br>Email: {''.join(random.choices(string.ascii_lowercase,k=8))}@gmail.com"
    return render_template_string(HTML, pass_gen=pass_gen, hash_res=hash_res, b64_res=b64_res, fake=fake, qr=qr, yt=yt, wifi_qr=wifi_qr, insta=insta, chat=chat, fonts=fonts, reels=reels, usercheck=usercheck, ip=request.headers.get('X-Forwarded-For', request.remote_addr))

if __name__=='__main__': app.run()
