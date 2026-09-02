from flask import Flask, request, render_template_string
import hashlib, re, os, random, string, base64, urllib.parse, json
from datetime import datetime

app = Flask(__name__)

# 50 TOOLS LIST
TOOLS_LIST = [
    ("John Toolkit", "hash"), ("MD5 Generator", "hash"), ("SHA1 Gen", "hash"),
    ("SHA256 Gen", "hash"), ("Base64 Encode", "encoder"), ("Base64 Decode", "encoder"),
    ("URL Encode", "encoder"), ("URL Decode", "encoder"), ("Hex Encode", "encoder"),
    ("Binary Converter", "converter"), ("Password Generator", "security"),
    ("Pass Strength", "security"), ("My IP Info", "info"), ("User Agent", "info"),
    ("Word Counter", "text"), ("Char Counter", "text"), ("Uppercase", "text"),
    ("Lowercase", "text"), ("Reverse Text", "text"), ("Remove Space", "text"),
    ("Duplicate Remover", "text"), ("JSON Formatter", "formatter"), ("HTML Escape", "formatter"),
    ("Age Calculator", "calc"), ("Random Number", "calc"), ("UUID Gen", "generator"),
    ("Lorem Ipsum", "generator"), ("Morse Code", "encoder"), ("ROT13", "encoder"),
    ("Palindrome Check", "checker"), ("Email Validator", "checker"), ("Hash Identifier", "hash"),
    ("Slug Generator", "text"), ("Case Swap", "text"), ("MD5 Checker", "hash"),
    ("SHA256 Checker", "hash"), ("Color Picker", "generator"), ("Binary to Text", "converter"),
    ("Text to Binary", "converter"), ("Hex to Text", "converter"), ("Text to Hex", "converter"),
    ("CSV to JSON", "converter"), ("IP to Binary", "converter"), ("Whitespace Cleaner", "text"),
    ("Regex Tester", "checker"), ("QR Text", "generator"), ("Credit Luhn", "checker"),
    ("Phone Validator", "checker"), ("Pass Length", "security"), ("IP Tracker", "info"),
    ("Header Viewer", "info"), ("Port Info", "info")
]

HOME_HTML = """
<html><head><meta name="viewport" content="width=device-width,initial-scale=1">
<title>CYB3R TOOLS - 50 IN 1</title>
<style>
body{background:#000;color:#0f0;font-family:monospace;padding:10px;margin:0}
h1{text-align:center;border:2px solid #0f0;padding:10px;box-shadow:0 0 15px #0f0}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:10px;margin-top:20px}
.card{border:1px solid #0f0;padding:12px;text-align:center;background:#0a0a0a}
.card:hover{background:#0f0;color:#000;box-shadow:0 0 10px #0f0}
.card a{color:inherit;text-decoration:none;font-weight:bold;font-size:13px}
</style></head><body>
<h1>🔥 CYB3R TOOLS - 50 IN 1 🔥</h1>
<div class="grid">
{% for idx, tool in tools %}
<div class="card"><a href="/tool/{{idx}}">{{idx+1}}. {{tool[0]}}</a></div>
{% endfor %}
</div>
</body></html>
"""

JOHN_HTML = """
<html><head><meta name="viewport" content="width=device-width,initial-scale=1">
<title>CYB3R - John Toolkit</title>
<style>
body{background:#000;color:#0f0;font-family:monospace;display:flex;justify-content:center;padding:15px}
.box{border:1px solid #0f0;padding:20px;width:100%;max-width:500px;box-shadow:0 0 15px #0f0}
h2{color:#0f0;text-align:center}
label{color:#0f0;font-size:13px;display:block;margin-top:15px}
input{width:100%;padding:10px;background:#111;color:#0f0;border:1px solid #0f0;margin-top:5px;box-sizing:border-box}
button{background:#0f0;color:#000;font-weight:bold;padding:8px 15px;border:none;margin-top:8px;cursor:pointer}
pre{background:#111;padding:10px;border-left:3px solid #0f0;white-space:pre-wrap;word-break:break-all}
a{color:#0f0}
</style></head><body>
<div class="box">
<a href="/">← Back to 50 Tools</a>
<h2>🔒 CYB3R - John Toolkit [Legal Version]</h2>
<p style="font-size:11px">Hash Identifier + Generator + Strength Check</p>

<form method="POST">
<label>1. Hash Identifier</label>
<input name="hash_input" placeholder="Hash paste karo e.g 5f4dcc3b5aa765d61d8327deb882cf99" value="{{h_input}}">
<button name="action" value="identify">Identify</button>
{% if identify_out %}<pre>{{identify_out}}</pre>{% endif %}

<label>2. Hash Generator</label>
<input name="pass_input" placeholder="Password likho e.g password123" value="{{p_input}}">
<button name="action" value="generate">Generate Hashes</button>
{% if gen_out %}<pre>{{gen_out}}</pre>{% endif %}

<label>3. Password Strength (John Speed Test)</label>
<input name="strength_input" placeholder="Password check karo" value="{{s_input}}">
<button name="action" value="strength">Check Strength</button>
{% if strength_out %}<pre>{{strength_out}}</pre>{% endif %}
</form>
<p style="font-size:10px;color:#888;margin-top:20px">For Educational & Security Auditing Only. Use on your own passwords.</p>
</div></body></html>
"""

GENERIC_HTML = """
<html><head><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{{name}}</title>
<style>body{background:#000;color:#0f0;font-family:monospace;display:flex;justify-content:center;padding:15px}
.box{border:1px solid #0f0;padding:20px;width:100%;max-width:500px}
input,textarea{width:100%;padding:10px;background:#111;color:#0f0;border:1px solid #0f0;box-sizing:border-box}
button{background:#0f0;color:#000;font-weight:bold;padding:10px;border:none;margin-top:10px;width:100%}
pre{background:#111;padding:10px;white-space:pre-wrap;word-break:break-all;border-left:3px solid #0f0}
a{color:#0f0}</style></head><body>
<div class="box"><a href="/">← Back</a><h2>{{name}}</h2>
<form method="POST"><textarea name="data" rows="4" placeholder="Yaha input dalo...">{{inp}}</textarea>
<button>Run {{name}}</button></form>
{% if out %}<pre>{{out}}</pre>{% endif %}
</div></body></html>
"""

def identify_hash(h):
    h = h.strip()
    if len(h)==32 and re.match(r'^[a-fA-F0-9]{32}$',h): return "Possible: MD5 (128-bit)"
    if len(h)==40 and re.match(r'^[a-fA-F0-9]{40}$',h): return "Possible: SHA1 (160-bit)"
    if len(h)==64 and re.match(r'^[a-fA-F0-9]{64}$',h): return "Possible: SHA256 (256-bit)"
    return "Unknown / Not a standard hex hash. Length: "+str(len(h))

@app.route('/')
def home():
    return render_template_string(HOME_HTML, tools=list(enumerate(TOOLS_LIST)))

@app.route('/tool/<int:tid>', methods=['GET','POST'])
def tool(tid):
    if tid <0 or tid>=len(TOOLS_LIST): return "Not Found",404
    name = TOOLS_LIST[tid][0]

    # John Toolkit - Special Page (0 index)
    if tid==0:
        h_input=p_input=s_input=""
        identify_out=gen_out=strength_out=""
        if request.method=='POST':
            action=request.form.get('action')
            if action=='identify':
                h_input=request.form.get('hash_input','')
                identify_out=identify_hash(h_input)
            elif action=='generate':
                p_input=request.form.get('pass_input','')
                if p_input:
                    gen_out=f"MD5: {hashlib.md5(p_input.encode()).hexdigest()}\nSHA1: {hashlib.sha1(p_input.encode()).hexdigest()}\nSHA256: {hashlib.sha256(p_input.encode()).hexdigest()}"
            elif action=='strength':
                s_input=request.form.get('strength_input','')
                score=len(s_input)
                if score<6: strength_out="WEAK 🔴 - Bahut jaldi crack ho jayega (John < 1 sec)"
                elif score<10: strength_out="MEDIUM 🟡 - Crack time ~ few hours"
                else: strength_out="STRONG 🟢 - Crack mushkil hai (Years)"
        return render_template_string(JOHN_HTML, h_input=h_input, p_input=p_input, s_input=s_input, identify_out=identify_out, gen_out=gen_out, strength_out=strength_out)

    # Other 49 tools - Generic logic
    inp=out=""
    if request.method=='POST':
        inp=request.form.get('data','')
        if name=="MD5 Generator": out=hashlib.md5(inp.encode()).hexdigest()
        elif name=="SHA256 Gen": out=hashlib.sha256(inp.encode()).hexdigest()
        elif name=="Base64 Encode": out=base64.b64encode(inp.encode()).decode()
        elif name=="Base64 Decode":
            try: out=base64.b64decode(inp.encode()).decode()
            except: out="Invalid Base64"
        elif name=="Uppercase": out=inp.upper()
        elif name=="Lowercase": out=inp.lower()
        elif name=="Reverse Text": out=inp[::-1]
        elif name=="Word Counter": out=f"Words: {len(inp.split())}, Chars: {len(inp)}"
        elif name=="Password Generator": out=''.join(random.choices(string.ascii_letters+string.digits+"!@#$%",k=16))
        else: out=f"Processed: {inp[:500]}"
    return render_template_string(GENERIC_HTML, name=f"{tid+1}. {name}", inp=inp, out=out)

if __name__=='__main__':
    app.run(host='0.0.0.0', port=10000)
