from flask import Flask, request, render_template_string
import string, secrets, hashlib, urllib.parse

app=Flask(__name__)
HTML="""<!DOCTYPE html><html><head><meta name='viewport' content='width=device-width,initial-scale=1'><style>
body{background:#0a0a0a;color:#fff;font-family:Arial;padding:15px}
h1{color:#FFD60A;text-align:center}
.card{background:#1a1a1a;border:1px solid #FFD60A;border-radius:12px;padding:15px;margin:12px 0}
input,button{width:100%;padding:12px;margin:6px 0;border-radius:8px;border:none}
button{background:#FFD60A;color:#000;font-weight:bold}
.result{background:#000;border:1px dashed #FFD60A;padding:10px;margin-top:10px;border-radius:8px;word-break:break-all}
.safe{color:#00ff88}.danger{color:#ff4444}
.footer{text-align:center;color:#888;margin-top:20px;font-size:12px}
</style></head><body>
<h1>⚡ CYB3R TOOLS - VICKY</h1>

<div class='card'><h3>1. UPI QR Generator</h3><form method='POST'><input type='hidden' name='type' value='upi'><input name='upi_id' placeholder='UPI ID'><input name='name' placeholder='Name'><input name='amount' placeholder='Amount'><button>Generate UPI QR</button></form>{% if upi_qr %}<div class='result'><img src='{{upi_qr}}' style='width:200px'></div>{% endif %}</div>

<div class='card'><h3>2. Link Checker</h3><form method='POST'><input type='hidden' name='type' value='linkcheck'><input name='text' placeholder='Paste Link'><button>Check</button></form>{% if link_res %}<div class='result'>{{link_res|safe}}</div>{% endif %}</div>

<div class='card'><h3>3. Strong Password</h3><form method='POST'><input type='hidden' name='type' value='pass'><button>Generate Password</button></form>{% if pass_gen %}<div class='result'>{{pass_gen}}</div>{% endif %}</div>

<div class='card'><h3>4. Hash Generator</h3><form method='POST'><input type='hidden' name='type' value='hash'><input name='text' placeholder='Enter text'><button>Generate Hash</button></form>{% if hash_res %}<div class='result'>MD5: {{hash_res.md5}}</div>{% endif %}</div>

<div class='card'><h3>5. Text to QR</h3><form method='POST'><input type='hidden' name='type' value='qr'><input name='text' placeholder='Enter text/link'><button>Make QR</button></form>{% if qr %}<div class='result'><img src='{{qr}}' style='width:200px'></div>{% endif %}</div>

<div class='card'><h3>6. WiFi QR</h3><form method='POST'><input type='hidden' name='type' value='wifi'><input name='ssid' placeholder='WiFi Name'><input name='wpass' placeholder='Password'><button>Generate WiFi QR</button></form>{% if wifi_qr %}<div class='result'><img src='{{wifi_qr}}' style='width:200px'></div>{% endif %}</div>

<div class='card'><h3>7. YT Thumbnail</h3><form method='POST'><input type='hidden' name='type' value='yt'><input name='text' placeholder='YouTube Link'><button>Get Thumbnail</button></form>{% if yt %}<div class='result'><img src='{{yt}}' style='width:100%'></div>{% endif %}</div>

<div class='card'><h3>8. Insta DP Viewer</h3><form method='POST'><input type='hidden' name='type' value='insta'><input name='text' placeholder='Insta Username'><button>View DP</button></form>{% if insta %}<div class='result'><img src='{{insta}}' style='width:200px'></div>{% endif %}</div>

<div class='card'><h3>9. Fake Chat Maker</h3><form method='POST'><input type='hidden' name='type' value='fakechat'><input name='cname' placeholder='Name'><input name='msg' placeholder='Message'><button>Make Chat</button></form>{% if chat %}<div class='result'>{{chat|safe}}</div>{% endif %}</div>

<div class='card'><h3>10. Stylish Name Maker</h3><form method='POST'><input type='hidden' name='type' value='font'><input name='text' placeholder='Enter name e.g. vicky'><button>Make Stylish</button></form>{% if fonts %}<div class='result'>{{fonts|safe}}</div>{% endif %}</div>

<div class='footer'>MADE BY VICKY CHAUHAN | VADODARA, GUJARAT</div>
</body></html>"""

@app.route('/', methods=['GET','POST'])
def home():
    upi_qr=qr=wifi_qr=yt=insta=chat=fonts=pass_gen=hash_res=link_res=None
    if request.method=='POST':
        t=request.form.get('type'); txt=request.form.get('text','').strip()
        if t=='upi':
            upi_id=request.form.get('upi_id',''); name=request.form.get('name',''); amount=request.form.get('amount','')
            upi_str=f"upi://pay?pa={upi_id}&pn={urllib.parse.quote(name)}"
            if amount: upi_str+=f"&am={amount}&cu=INR"
            upi_qr=f"https://api.qrserver.com/v1/create-qr-code/?size=500x500&data={urllib.parse.quote(upi_str)}"
        elif t=='linkcheck':
            low=txt.lower()
            if any(x in low for x in ['bit.ly','tinyurl','free money','lottery']):
                link_res=f"<span class='danger'>❌ RISKY LINK!</span><br>{txt}"
            elif 'https' in low: link_res=f"<span class='safe'>✅ SAFE HAI</span><br>{txt}"
            else: link_res=f"<span class='danger'>⚠️ HTTP Link!</span><br>{txt}"
        elif t=='pass':
            alpha=string.ascii_letters+string.digits+"!@#$%&*"
            pass_gen=''.join(secrets.choice(alpha) for _ in range(16))
        elif t=='hash': hash_res={'md5':hashlib.md5(txt.encode()).hexdigest()}
        elif t=='qr': qr=f"https://api.qrserver.com/v1/create-qr-code/?size=500x500&data={urllib.parse.quote(txt)}"
        elif t=='wifi':
            ssid=request.form.get('ssid',''); wpass=request.form.get('wpass','')
            wifi_str=f"WIFI:T:WPA;S:{ssid};P:{wpass};;"
            wifi_qr=f"https://api.qrserver.com/v1/create-qr-code/?size=500x500&data={urllib.parse.quote(wifi_str)}"
        elif t=='yt':
            vid=txt.split("v=")[-1].split("&")[0] if "v=" in txt else txt.split("/")[-1]
            yt=f"https://img.youtube.com/vi/{vid}/maxresdefault.jpg"
        elif t=='insta': insta=f"https://unavatar.io/instagram/{txt}"
        elif t=='fakechat':
            cname=request.form.get('cname',''); msg=request.form.get('msg','')
            chat=f"WhatsApp Chat Preview:<br><br>👤 {cname}<br>💬 {msg}<br><br>10:35 ✓✓"
        elif t=='font':
            a1={'a':'𝐚','b':'𝐛','c':'𝐜','d':'𝐝','e':'𝐞','f':'𝐟','g':'𝐠','h':'𝐡','i':'𝐢','j':'𝐣','k':'𝐤','l':'𝐥','m':'𝐦','n':'𝐧','o':'𝐨','p':'𝐩','q':'𝐪','r':'𝐫','s':'𝐬','t':'𝐭','u':'𝐮','v':'𝐯','w':'𝐰','x':'𝐱','y':'𝐲','z':'𝐳'}
            a2={'a':'𝓪','b':'𝓫','c':'𝓬','d':'𝓭','e':'𝓮','f':'𝓯','g':'𝓰','h':'𝓱','i':'𝓲','j':'𝓳','k':'𝓴','l':'𝓵','m':'𝓶','n':'𝓷','o':'𝓸','p':'𝓹','q':'𝓺','r':'𝓻','s':'𝓼','t':'𝓽','u':'𝓾','v':'𝓿','w':'𝔀','x':'𝔁','y':'𝔂','z':'𝔃'}
            a3={'a':'𝖆','b':'𝖇','c':'𝖈','d':'𝖉','e':'𝖊','f':'𝖋','g':'𝖌','h':'𝖍','i':'𝖎','j':'𝖏','k':'𝖐','l':'𝖑','m':'𝖒','n':'𝖓','o':'𝖔','p':'𝖕','q':'𝖖','r':'𝖗','s':'𝖘','t':'𝖙','u':'𝖚','v':'𝖛','w':'𝖜','x':'𝖝','y':'𝖞','z':'𝖟'}
            a4={'a':'ⓐ','b':'ⓑ','c':'ⓒ','d':'ⓓ','e':'ⓔ','f':'ⓕ','g':'ⓖ','h':'ⓗ','i':'ⓘ','j':'ⓙ','k':'ⓚ','l':'ⓛ','m':'ⓜ','n':'ⓝ','o':'ⓞ','p':'ⓟ','q':'ⓠ','r':'ⓡ','s':'ⓢ','t':'ⓣ','u':'ⓤ','v':'ⓥ','w':'ⓦ','x':'ⓧ','y':'ⓨ','z':'ⓩ'}
            def st(t,m): return ''.join(m.get(ch.lower(), ch) for ch in t)
            fonts=f"1. Bold: {st(txt,a1)}<br>2. Script: {st(txt,a2)}<br>3. Black: {st(txt,a3)}<br>4. Circle: {st(txt,a4)}<br>5. Upper: {txt.upper()}<br>6. Reverse: {txt[::-1]}"
    return render_template_string(HTML, upi_qr=upi_qr, qr=qr, wifi_qr=wifi_qr, yt=yt, insta=insta, chat=chat, fonts=fonts, pass_gen=pass_gen, hash_res=hash_res, link_res=link_res)

if __name__=='__main__': app.run()
