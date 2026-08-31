from flask import Flask, request, render_template_string
import hashlib, base64, random, string, secrets

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
<title>CYB3R TOOLS - Vicky</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
body{background:#0a0a0a;color:#00ff00;font-family:monospace;padding:15px}
h1{text-align:center;color:#00ff00;text-shadow:0 0 10px #00ff00}
.card{border:1px solid #00ff00;padding:15px;margin:15px 0;border-radius:10px;background:#111}
input,button,textarea{width:100%;padding:10px;margin:5px 0;background:#000;color:#0f0;border:1px solid #0f0;border-radius:5px}
button{background:#00ff00;color:#000;font-weight:bold;cursor:pointer}
button:hover{background:#fff}
.result{background:#000;padding:10px;margin-top:10px;border:1px dashed #0f0;word-break:break-all}
</style>
</head>
<body>
<h1>⚡ CYB3R TOOLS BY VICKY ⚡</h1>
<p style="text-align:center">Live: cyb3r-tools.onrender.com</p>

<div class="card">
<h2>1. Password Generator</h2>
<form method="post"><input type="hidden" name="type" value="pass"><button>Generate Strong Password</button></form>
{% if pass_gen %}<div class="result">{{ pass_gen }}</div>{% endif %}
</div>

<div class="card">
<h2>2. Hash Generator</h2>
<form method="post"><input type="hidden" name="type" value="hash"><input name="text" placeholder="Enter text" required><button>Generate MD5 & SHA256</button></form>
{% if hash_res %}<div class="result">MD5: {{ hash_res.md5 }}<br><br>SHA256: {{ hash_res.sha256 }}</div>{% endif %}
</div>

<div class="card">
<h2>3. Base64 Encode/Decode</h2>
<form method="post"><input type="hidden" name="type" value="b64"><input name="text" placeholder="Enter text" required><button>Encode & Decode</button></form>
{% if b64_res %}<div class="result">Encoded: {{ b64_res.enc }}<br><br>Decoded: {{ b64_res.dec }}</div>{% endif %}
</div>

<div class="card">
<h2>4. Your IP & Device Info</h2>
<p>IP: {{ ip }}<br>Browser: {{ ua }}</p>
</div>

<div class="card">
<h2>5. Fake ID Generator</h2>
<form method="post"><input type="hidden" name="type" value="fake"><button>Generate Fake Identity</button></form>
{% if fake %}<div class="result">{{ fake }}</div>{% endif %}
</div>

<p style="text-align:center;margin-top:30px">Made with ❤️ by Vicky Chauhan</p>
</body>
</html>
"""

@app.route('/', methods=['GET','POST'])
def home():
    pass_gen=None; hash_res=None; b64_res=None; fake=None
    if request.method=='POST':
        t=request.form.get('type')
        if t=='pass':
            alphabet = string.ascii_letters + string.digits + "!@#$%^&*"
            pass_gen = ''.join(secrets.choice(alphabet) for _ in range(16))
        elif t=='hash':
            txt=request.form.get('text','')
            hash_res={'md5':hashlib.md5(txt.encode()).hexdigest(),'sha256':hashlib.sha256(txt.encode()).hexdigest()}
        elif t=='b64':
            txt=request.form.get('text','')
            enc=base64.b64encode(txt.encode()).decode()
            try: dec=base64.b64decode(txt.encode()).decode()
            except: dec="Not a valid Base64 - showing encode only"
            b64_res={'enc':enc,'dec':dec}
        elif t=='fake':
            names=["Aarav Sharma","Vicky Chauhan","Raj Patel","John Wick"]
            fake=f"Name: {random.choice(names)}<br>Email: {''.join(random.choices(string.ascii_lowercase,k=8))}@gmail.com<br>Phone: 9{random.randint(100000000,999999999)}<br>Password: {''.join(secrets.choice(string.ascii_letters+string.digits) for _ in range(10))}"

    return render_template_string(HTML, pass_gen=pass_gen, hash_res=hash_res, b64_res=b64_res, fake=fake, ip=request.headers.get('X-Forwarded-For', request.remote_addr), ua=request.headers.get('User-Agent'))

if __name__=='__main__':
    app.run()
