from flask import Flask, request, render_template_string
import hashlib, re, os, random, string, base64, urllib.parse

app = Flask(__name__)

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
:root{ --main:#ffcc00; }
body{background:#0a0a0a;color:#fff;font-family:sans-serif;margin:0;padding:12px;transition:0.3s}
.top{border:2px solid var(--main);border-radius:25px;padding:22px;text-align:center;background:linear-gradient(180deg,#1a1a00,#000);box-shadow:0 0 20px var(--main)}
.top h1{color:var(--main);margin:0;font-size:26px}
.top p{color:#aaa;font-size:12px;margin-top:5px}
.theme-bar{display:flex;gap:8px;justify-content:center;margin:15px 0;flex-wrap:wrap}
.tbtn{padding:8px 16px;border-radius:20px;border:none;font-weight:bold;cursor:pointer}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(140px,1fr));gap:10px;margin-top:10px}
.card{border:1px solid #333;padding:12px;text-align:center;background:#141414;border-radius:18px}
.card a{color:var(--main);text-decoration:none;font-weight:bold;font-size:13px}
.card:hover{border-color:var(--main);box-shadow:0 0 10px var(--main)}
</style>
<script>
function setTheme(c){ localStorage.setItem('cyb_theme',c); document.documentElement.style.setProperty('--main',c); }
window.onload=function(){ let s=localStorage.getItem('cyb_theme')||'#ffcc00'; document.documentElement.style.setProperty('--main',s); }
</script>
</head><body>
<div class="top">
<h1>⚡ CYB3R TOOLS - 50 IN 1 ⚡</h1>
<p>50+ TOOLS | SECURE | MADE BY VICKY CHAUHAN</p>
</div>

<div class="theme-bar">
<button class="tbtn" style="background:#ffcc00" onclick="setTheme('#ffcc00')">Yellow Hacker</button>
<button class="tbtn" style="background:#00ff00" onclick="setTheme('#00ff00')">Green Matrix</button>
<button class="tbtn" style="background:#ff0040;color:#fff" onclick="setTheme('#ff0040')">Red Cyber</button>
<button class="tbtn" style="background:#00d9ff" onclick="setTheme('#00d9ff')">Blue</button>
</div>

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
:root{ --main:#ffcc00; }
body{background:#0a0a0a;color:#fff;font-family:sans-serif;display:flex;justify-content:center;padding:12px}
.box{border:2px solid var(--main);padding:20px;width:100%;max-width:500px;border-radius:20px;background:#141414}
input{width:100%;padding:12px;background:#000;color:#fff;border:1px solid #333;margin-top:5px;box-sizing:border-box;border-radius:12px}
button{background:var(--main);color:#000;font-weight:bold;padding:10px 15px;border:none;margin-top:8px;border-radius:10px;width:100%}
pre{background:#000;padding:10px;border-left:3px solid var(--main);white-space:pre-wrap;word-break:break-all;color:var(--main);border-radius:8px}
a{color:var(--main);text-decoration:none}
</style>
<script>
window.onload=function(){ let s=localStorage.getItem('cyb_theme')||'#ffcc00'; document.documentElement.style.setProperty('--main',s); }
</script>
</head><body>
<div class="box">
<a href="/">← Back to 50 Tools</a>
<h2 style="color:var(--main)">🔒 CYB3R - John Toolkit [Legal]</h2>
<form method="POST">
<label>1. Hash Identifier</label>
<input name="hash_input" placeholder="Hash paste karo" value="{{h_input}}">
<button name="action" value="identify">Identify</button>
{% if identify_out %}<pre>{{identify_out}}</pre>{% endif %}
<label>2. Hash Generator</label>
<input name="pass_input" placeholder="Password likho" value="{{p_input}}">
<button name="action" value="generate">Generate Hashes</button>
{% if gen_out %}<pre>{{gen_out}}</pre>{% endif %}
<label>3. Password Strength</label>
<input name="strength_input" placeholder="Password check karo" value="{{s_input}}">
<button name="action" value="strength">Check Strength</button>
{% if strength_out %}<pre>{{strength_out}}</pre>{% endif %}
</form></div></body></html>
"""

GENERIC_HTML = """
<html><head><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{{name}}</title>
<style>
:root{ --main:#ffcc00; }
body{background:#0a0a0a;color:#fff;font-family:sans-serif;display:flex;justify-content:center;padding:12px}
.box{border:2px solid var(--main);padding:20px;width:100%;max-width:500px;border-radius:20px;background:#141414}
textarea{width:100%;padding:12px;background:#000;color:#fff;border:1px solid #333;box-sizing:border-box;border-radius:12px}
button{background:var(--main);color:#000;font-weight:bold;padding:12px;border:none;margin-top:10px;width:100%;border-radius:12px}
pre{background:#000;padding:10px;white-space:pre-wrap;word-break:break-all;border-left:3px solid var(--main);color:var(--main);border-radius:8px}
a{color:var(--main);text-decoration:none}
</style>
<script>
window.onload=function(){ let s=localStorage.getItem('cyb_theme')||'#ffcc00'; document.documentElement.style.setProperty('--main',s); }
</script>
</head><body>
<div class="box"><a href="/">← Back</a><h2 style="color:var(--main)">{{name}}</h2>
<form method="POST"><textarea name="data" rows="4" placeholder="Input dalo...">{{inp}}</textarea>
<button>Run {{name}}</button></form>
{% if out %}<pre>{{out}}</pre>{% endif %}
</div></body></html>
"""

def identify_hash(h):
    h=h.strip()
    if len(h)==32 and re.match(r'^[a-fA-F0-9]{32}$',h): return "Possible: MD5"
    if len(h)==40 and re.match(r'^[a-fA-F0-9]{40}$',h): return "Possible: SHA1"
    if len(h)==64 and re.match(r'^[a-fA-F0-9]{64}$',h): return "Possible: SHA256"
    return "Unknown hash, Length: "+str(len(h))

@app.route('/')
def home():
    return render_template_string(HOME_HTML, tools=list(enumerate(TOOLS_LIST)))

@app.route('/tool/<int:tid>', methods=['GET','POST'])
def tool(tid):
    if tid<0 or tid>=len(TOOLS_LIST): return "Not Found",404
    name=TOOLS_LIST[tid][0]
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
                if len(s_input)<6: strength_out="WEAK - Crack < 1 sec"
                elif len(s_input)<10: strength_out="MEDIUM - Few hours"
                else: strength_out="STRONG - Years"
        return render_template_string(JOHN_HTML, h_input=h_input, p_input=p_input, s_input=s_input, identify_out=identify_out, gen_out=gen_out, strength_out=strength_out)
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
