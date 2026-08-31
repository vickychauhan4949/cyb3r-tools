from flask import Flask, request, render_template_string
import hashlib, base64, random, string, secrets, re

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
<title>CYB3R TOOLS - Vicky</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
body{background:#0a0a0a;color:#00ff00;font-family:monospace;padding:15px}
h1{text-align:center;color:#00ff00;text-shadow:0 0 15px #00ff00}
.card{border:1px solid #00ff00;padding:15px;margin:15px 0;border-radius:10px;background:#111;box-shadow:0 0 10px #003300}
input,button,textarea{width:100%;padding:12px;margin:6px 0;background:#000;color:#0f0;border:1px solid #0f0;border-radius:6px;font-family:monospace}
button{background:#00ff00;color:#000;font-weight:bold;cursor:pointer;font-size:16px}
button:hover{background:#fff}
.result{background:#000;padding:12px;margin-top:10px;border:1px dashed #0f0;word-break:break-all;border-radius:5px}
img{max-width:100%}
</style>
</head>
<body>
<h1>⚡ CYB3R TOOLS BY VICKY ⚡</h1>
<p style="text-align:center">cyb3r-tools.onrender.com | Total Tools: 8</p>

<div class="card">
<h2>1. Password Generator</h2>
<form method="post"><input type="hidden" name="type" value="pass"><button>Generate 16-char Password</button></form>
{% if pass_gen %}<div class="result">{{ pass_gen }}</div>{% endif %}
</div>

<div class="card">
<h2>2. Password Strength Checker</h2>
<form method="post"><input type="hidden" name="type" value="strength"><input name="text" placeholder="Enter password to check" required><button>Check Strength</button></form>
{% if strength %}<div class="result">{{ strength|safe }}</div>{% endif %}
</div>

<div class="card">
<h2>3. Hash Generator</h2>
<form method="post"><input type="hidden" name="type" value="hash"><input name="text" placeholder="Enter text" required><button>Generate MD5 & SHA256</button></form>
{% if hash_res %}<div class="result">MD5: {{ hash_res.md5 }}<br><br>SHA256: {{ hash_res.sha256 }}</div>{% endif %}
</div>

<div class="card">
<h2>4. Base64 Encode/Decode</h2>
<form method="post"><input type="hidden" name="type" value="b64"><input name="text" placeholder="Enter text" required><button>Encode & Decode</button></form>
{% if b64_res %}<div class="result">Encoded: {{ b64_res.enc }}<br><br>Decoded: {{ b64_res.dec }}</div>{% endif %}
</div>

<div class="card">
<h2>5. QR Code Generator</h2>
<form method="post"><input type="hidden" name="type" value="qr"><input name="text" placeholder="Enter link or text" required><button>Generate QR Code</button></form>
{% if qr %}<div class="result"><img src="{{ qr }}"><br><br>Scan this QR</div>{% endif %}
</div>

<div class="card">
<h2>6. YouTube Thumbnail Downloader</h2>
<form method="post"><input type="hidden" name="type" value="yt"><input name="text" placeholder="Paste YouTube Link" required><button>Get Thumbnail</button></form>
{% if yt %}<div class="result"><img src="{{ yt }}"><br><br><a href="{{ yt }}" target="_blank" style="color:#0f0">Open Full HD Image</a></div>{% endif %}
</div>

<div class="card">
<h2>7. Your IP & Device Info</h2>
<p>IP: {{ ip }}<br>Device: {{ ua[:120] }}...</p>
</div>

<div class="card">
<h2>8. Fake ID Generator</h2>
<form method="post"><input type="hidden" name="type" value="fake"><button>Generate Fake Identity</button></form>
{% if fake %}<div class="result">{{ fake|safe }}</div>{% endif %}
</div>

<p style="text-align:center;margin-top:30px">Made with ❤️ by Vicky Chauhan | Vadodara</p>
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
    levels=["Very Weak ❌","Weak ⚠️","Medium 😐","Strong ✅","Very Strong 🔥","Ultra Strong 💀"]
    return f"{levels[score]} - Score {score}/5<br>Length: {len(pwd)}"

@app.route('/', methods=['GET','POST'])
def home():
    pass_gen=None; hash_res=None; b64_res=None; fake=None; qr=None; yt=None; strength=None
    if request.method=='POST':
        t=request.form.get('type')
        txt=request.form.get('text','').strip()
        if t=='pass':
            alphabet = string.ascii_letters + string.digits + "!@#$%^&*"
            pass_gen = ''.join(secrets.choice(alphabet) for _ in range(16))
        elif t=='strength':
            strength=check_strength(txt)
        elif t=='hash':
            hash_res={'md5':hashlib.md5(txt.encode()).hexdigest(),'sha256':hashlib.sha256(txt.encode()).hexdigest()}
        elif t=='b64':
            enc=base64.b64encode(txt.encode()).decode()
            try: dec=base64.b64decode(txt.encode()).decode()
            except: dec="Not valid Base64"
            b64_res={'enc':enc,'dec':dec}
        elif t=='qr':
            qr=f"https://api.qrserver.com/v1/create-qr-code/?size=300x300&data={txt}"
        elif t=='yt':
            vid_id=None
            if "v=" in txt: vid_id=txt.split("v=")[1].split("&")[0]
            elif "youtu.be/" in txt: vid_id=txt.split("youtu.be/")[1].split("?")[0]
            else: vid_id=txt
            yt=f"https://img.youtube.com/vi/{vid_id}/maxresdefault.jpg"
        elif t=='fake':
            fake=f"Name: {random.choice(['Aarav','Vicky','John','Raj'])} {random.choice(['Sharma','Patel','Singh'])}<br>Email: {''.join(random.choices(string.ascii_lowercase,k=8))}@gmail.com<br>Phone: 9{random.randint(100000000,999999999)}"

    return render_template_string(HTML, pass_gen=pass_gen, hash_res=hash_res, b64_res=b64_res, fake=fake, qr=qr, yt=yt, strength=strength, ip=request.headers.get('X-Forwarded-For', request.remote_addr), ua=request.headers.get('User-Agent',''))

if __name__=='__main__':
    app.run()
