import os
import re
import hashlib
from flask import Flask, render_template_string, request

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev_key_for_local_only")

HTML = """
<!DOCTYPE html>
<html>
<head><title>CYB3R TOOLS - John Toolkit</title>
<style>
body{background:#0a0a0a;color:#00ff00;font-family:monospace;padding:20px}
.box{border:1px solid #00ff00;padding:20px;max-width:700px;margin:auto}
input{width:95%;padding:10px;background:#111;color:#0f0;border:1px solid #0f0}
button{padding:10px 20px;background:#00ff00;color:#000;font-weight:bold;border:none;margin-top:10px;cursor:pointer}
.result{background:#111;padding:10px;margin-top:15px;border-left:3px solid #0f0}
</style>
</head>
<body>
<div class="box">
<h2>🔓 CYB3R - John Toolkit [Legal Version]</h2>
<p>Hash Identifier + Generator + Strength Check</p>

<h3>1. Hash Identifier</h3>
<form method="POST"><input name="hash" placeholder="Hash paste karo e.g 5f4dcc3b5aa765d61d8327deb882cf99"><button name="action" value="identify">Identify</button></form>

<h3>2. Hash Generator</h3>
<form method="POST"><input name="text" placeholder="Password likho e.g password123"><button name="action" value="generate">Generate Hashes</button></form>

<h3>3. Password Strength (John Speed Test)</h3>
<form method="POST"><input name="passcheck" placeholder="Password check karo"><button name="action" value="strength">Check Strength</button></form>

{% if result %}<div class="result">{{ result|safe }}</div>{% endif %}
<p style="font-size:12px;color:#888;margin-top:20px">For Educational & Security Auditing Only. Use on your own passwords.</p>
</div>
</body>
</html>
"""

def identify_hash(h):
    h = h.strip()
    if re.match(r'^[a-fA-F0-9]{32}$', h): return "MD5"
    if re.match(r'^[a-fA-F0-9]{40}$', h): return "SHA1"
    if re.match(r'^[a-fA-F0-9]{64}$', h): return "SHA256"
    if h.startswith("$2b$") or h.startswith("$2a$"): return "Bcrypt"
    return "Unknown / Possible Custom Hash"

@app.route('/', methods=['GET','POST'])
def home():
    result = ""
    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'identify':
            h = request.form.get('hash','')
            t = identify_hash(h)
            result = f"<b>Hash:</b> {h}<br><b>Identified Type:</b> {t}"
        elif action == 'generate':
            txt = request.form.get('text','')
            if txt:
                md5 = hashlib.md5(txt.encode()).hexdigest()
                sha1 = hashlib.sha1(txt.encode()).hexdigest()
                sha256 = hashlib.sha256(txt.encode()).hexdigest()
                result = f"<b>Input:</b> {txt}<br><b>MD5:</b> {md5}<br><b>SHA1:</b> {sha1}<br><b>SHA256:</b> {sha256}"
        elif action == 'strength':
            p = request.form.get('passcheck','')
            score = len(p)
            if score < 6: result = f"<b>{p}</b> -> VERY WEAK - John 1 sec me crack kar dega!"
            elif score < 9: result = f"<b>{p}</b> -> MEDIUM - 2-3 hours lagega"
            else: result = f"<b>{p}</b> -> STRONG - Crack karna mushkil hai!"
    return render_template_string(HTML, result=result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
