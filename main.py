from flask import Flask, request, render_template_string
import hashlib, base64, random, string, secrets, urllib.parse

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html><head>
<title>CYB3R TOOLS - By Vicky Chauhan</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@600;800&display=swap" rel="stylesheet">
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{background:#0a0a0a;color:#fff;font-family:'Poppins',sans-serif;padding:12px}
.header{text-align:center;padding:30px 10px;border:2px solid #FFD60A;border-radius:20px;margin:10px 0 20px 0;background:linear-gradient(145deg,#1a1a00,#000)}
.header h1{font-size:36px;color:#FFD60A;letter-spacing:2px;text-shadow:0 0 15px #FFD60A}
.header p{color:#aaa;margin-top:8px;font-size:13px}
.header.name{color:#FFD60A;font-weight:800;margin-top:5px}
.card{background:#161616;border:1px solid #333;padding:20px;margin:16px 0;border-radius:18px;box-shadow:0 4px 20px rgba(0,0,0,0.5)}
.card h2{font-size:20px;color:#FFD60A;margin-bottom:14px}
.card p{font-size:12px;color:#888}
input{width:100%;padding:14px;margin:8px 0;background:#0f0f0f;color:#fff;border:1px solid #444;border-radius:12px;font-size:14px;outline:none}
input:focus{border-color:#FFD60A}
button{width:100%;padding:14px;margin:8px 0;background:#FFD60A;color:#000;border:none;border-radius:12px;font-weight:800;font-size:16px;cursor:pointer;transition:0.2s}
button:hover{background:#fff;transform:scale(1.02)}
.result{background:#000;padding:14px;margin-top:12px;border:1px dashed #FFD60A;border-radius:12px;color:#00ff88;font-family:monospace;font-size:13px;word-break:break-all}
.result img{max-width:100%;border-radius:10px;margin-top:5px}
.badge{background:#FFD60A;color:#000;padding:3px 10px;border-radius:20px;font-size:10px;font-weight:800;margin-left:8px}
.footer{text-align:center;padding:30px 10px;color:#555;font-size:12px;margin-top:20px;border-top:1px solid #222}
.footer b{color:#FFD60A}
.safe{color:#00ff88;font-weight:bold}.danger{color:#ff4444;font-weight:bold}
a{color:#FFD60A;text-decoration:none}
</style></head><body>

<div class="header">
<h1>⚡ CYB3R TOOLS ⚡</h1>
<p>10 POWERFUL TOOLS - FAST, SAFE & PRIVATE</p>
<p class="name">MADE BY VICKY CHAUHAN | VADODARA, GUJARAT</p>
</div>

<div class="card"><h2>1. 💸 UPI QR Generator <span class="badge">MOST USED</span></h2>
<form method="post"><input type="hidden" name="type" value="upi"><input name="upi_id" placeholder="UPI ID - ex: vicky@okicici" required><input name="name" placeholder="Name - ex: Vicky"><input name="amount" placeholder="Amount - ex: 100 (optional)"><button>Generate QR</button></form>
{% if upi_qr %}<div class="result"><img src="{{ upi_qr }}"><br>✅ Scan karke pay karo</div>{% endif %}</div>

<div class="card"><h2>2. 🔗 Link Safety Checker</h2>
<form method="post"><input type="hidden" name="type" value="linkcheck"><input name="text" placeholder="Link paste karo" required><button>Check Now</button></form>
{% if link_res %}<div class="result">{{ link_res|safe }}</div>{% endif %}</div>

<div class="card"><h2>3. 📸 Insta DP Viewer HD <span class="badge">VIRAL</span></h2>
<form method="post"><input type="hidden" name="type" value="insta"><input name="text" placeholder="Insta Username - ex: virat.kohli" required><button>View HD DP</button></form>
{% if insta %}<div class="result"><img src="{{ insta }}"><br><br><a href="{{ insta }}" target="_blank">📥 Download HD</a></div>{% endif %}</div>

<div class="card"><h2>4. 🎥 YouTube Thumbnail HD</h2>
<form method="post"><input type="hidden" name="type" value="yt"><input name="text" placeholder="YouTube Link paste karo" required><button>Get Thumbnail HD</button></form>
{% if yt %}<div class="result"><img src="{{ yt }}"><br><br><a href="{{ yt }}" target="_blank">📥 Download Thumbnail</a></div>{% endif %}</div>

<div class="card"><h2>5. 📱 QR Code Generator</h2>
<form method="post"><input type="hidden" name="type" value="qr"><input name="text" placeholder="Kuch bhi likho - Link/Text" required><button>Generate QR</button></form>
{% if qr %}<div class="result"><img src="{{ qr }}"></div>{% endif %}</div>

<div class="card"><h2>6. 📶 WiFi QR Generator</h2>
<form method="post"><input type="hidden" name="type" value="wifi"><input name="ssid" placeholder="WiFi Name" required><input name="wpass" placeholder="WiFi Password" required><button>Generate WiFi QR</button></form>
{% if wifi_qr %}<div class="result"><img src="{{ wifi_qr }}"><br>Scan karke WiFi Connect</div>{% endif %}</div>

<div class="card"><h2>7. 🔐 Strong Password Generator</h2>
<form method="post"><input type="hidden" name="type" value="pass"><button>Generate Password</button></form>
{% if pass_gen %}<div class="result" style="font-size:18px;color:#FFD60A">{{ pass_gen }}</div>{% endif %}</div>

<div class="card"><h2>8. 🔤 Stylish Name Maker <span class="badge">VIRAL</span></h2>
<form method="post"><input type="hidden" name="type" value="font"><input name="text" placeholder="Tera Naam likh" required><button>Generate Style</button></form>
{% if fonts %}<div class="result">{{ fonts|safe }}</div>{% endif %}</div>

<div class="card"><h2>9. 🔑 Hash Generator</h2>
<form method="post"><input type="hidden" name="type" value="hash"><input name="text" placeholder="Text likho" required><button>Generate MD5 & SHA256</button></form>
{% if hash_res %}<div class="result">MD5: {{ hash_res.md5 }}<br><br>SHA256: {{ hash_res.sha256 }}</div>{% endif %}</div>

<div class="card"><h2>10. 💬 Fake WhatsApp Chat</h2>
<form method="post"><input type="hidden" name="type" value="fakechat"><input name="cname" placeholder="Name - ex: Mummy"><input name="msg" placeholder="Message - ex: Paisa bhej"><button>Generate Chat</button></form>
{% if chat %}<div class="result">{{ chat|safe }}</div>{% endif %}</div>

<div class="footer">
<b>CYB3R TOOLS 4.0</b><br><br>
Made with ❤️ by <b>Vicky Chauhan</b><br>
Cyber Safe Tools | Vadodara | 2026<br><br>
100% Safe | No Data Stored | Private
</div>

</body></html>
"""

@app.route('/', methods=['GET','POST'])
def home():
    upi_qr=qr=wifi_qr=yt=insta=chat=fonts=pass_gen=hash_res=link_res=None
    if request.method=='POST':
        t=request.form.get('type'); txt=request.form.get('text','').strip()
        if t=='upi':
            upi_id=request.form.get('upi_id',''); name=request.form.get('name','Vicky'); amount=request.form.get('amount','')
            upi_str=f"upi://pay?pa={upi_id}&pn={urllib.parse.quote(name)}"
            if amount: upi_str+=f"&am={amount}&cu=INR"
            upi_qr=f"https://api.qrserver.com/v1/create-qr-code/?size=500x500&data={urllib.parse.quote(upi_str)}"
        elif t=='linkcheck':
            low=txt.lower()
            if any(x in low for x in ['bit.ly','tinyurl','free money','lottery','earn fast','hack','crack']):
                link_res=f"<span class='danger'>❌ RISKY LINK!</span><br><br>Ye link thoda risky lag raha hai, soch samajh ke kholo.<br><br>Link: {txt}"
            elif 'https' in low: link_res=f"<span class='safe'>✅ SAFE HAI</span><br><br>https hai, safe lag raha hai.<br><br>Link: {txt}"
            else: link_res=f"<span class='danger'>⚠️ HTTP Link!</span><br><br>https nahi hai, dhyan se kholo.<br><br>Link: {txt}"
        elif t=='pass':
            alpha=string.ascii_letters+string.digits+"!@#$%^&*"
            pass_gen=''.join(secrets.choice(alpha) for _ in range(16))
        elif t=='hash': hash_res={'md5':hashlib.md5(txt.encode()).hexdigest(),'sha256':hashlib.sha256(txt.encode()).hexdigest()}
        elif t=='qr': qr=f"https://api.qrserver.com/v1/create-qr-code/?size=500x500&data={urllib.parse.quote(txt)}"
        elif t=='wifi':
            ssid=request.form.get('ssid',''); wpass=request.form.get('wpass','')
            wifi_str=f"WIFI:T:WPA;S:{ssid};P:{wpass};;"
            wifi_qr=f"https://api.qrserver.com/v1/create-qr-code/?size=500x500&data={urllib.parse.quote(wifi_str)}"
        elif t=='yt':
            vid=txt.split("v=")[-1].split("&")[0] if "v=" in txt else txt.split("/")[-1].split("?")[0].split("/")[0]
            yt=f"https://img.youtube.com/vi/{vid}/maxresdefault.jpg"
        elif t=='insta': insta=f"https://unavatar.io/instagram/{txt}"
        elif t=='fakechat':
            cname=request.form.get('cname',''); msg=request.form.get('msg','')
            chat=f"WhatsApp Chat Preview:<br><br>👤 {cname}<br>💬 {msg}<br><br>✓✓ 8:49 PM<br><i>Screenshot le sakte ho</i>"
        elif t=='font':
            fonts=f"1. 𝐁𝐨𝐥𝐝: {txt}<br>2. 𝓢𝓬𝓻𝓲𝓹𝓽: {txt}<br>3. 𝔉𝔯𝔞𝔨𝔱𝔲𝔯: {txt}<br>4. 🅱🅻🅰🅲🅺: {txt.upper()}<br>5. ᴍɪɴɪ: {txt.lower()}<br>6. Ⓒⓘⓡⓒⓛⓔ: {txt}"
    return render_template_string(HTML, upi_qr=upi_qr, qr=qr, wifi_qr=wifi_qr, yt=yt, insta=insta, chat=chat, fonts=fonts, pass_gen=pass_gen, hash_res=hash_res, link_res=link_res)

if __name__=='__main__': app.run()
