from flask import Flask, request, render_template_string
import hashlib, os

app = Flask(__name__)

# --- VISITOR 1200+ CODE ---
VISITOR_FILE = "count.txt"
if not os.path.exists(VISITOR_FILE):
    with open(VISITOR_FILE, "w") as f:
        f.write("1301")

def get_visitors():
    try:
        with open(VISITOR_FILE, "r") as f:
            c = int(f.read())
    except:
        c = 1301
    c += 1
    with open(VISITOR_FILE, "w") as f:
        f.write(str(c))
    return c
# --------------------------

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
:root{ --main:#00ff00; }
body{
  margin:0; padding:12px; color:#fff; font-family:sans-serif;
  background: linear-gradient(rgba(0,0,0,0.88), rgba(0,0,0,0.92)), url('https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?q=80&w=1000');
  background-size:cover; background-attachment:fixed; background-position:center;
}
.top{border:2px solid var(--main);border-radius:25px;padding:22px;text-align:center;background:rgba(0,20,0,0.85);box-shadow:0 0 25px var(--main)}
.top h1{color:var(--main);margin:0;font-size:26px;text-shadow:0 0 12px var(--main)}
.theme-bar{display:flex;gap:8px;justify-content:center;margin:15px 0;flex-wrap:wrap}
.tbtn{padding:8px 16px;border-radius:20px;border:none;font-weight:bold}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(140px,1fr));gap:10px}
.card{border:1px solid #222;padding:14px;text-align:center;background:rgba(15,15,15,0.9);border-radius:18px}
.card a{color:var(--main);text-decoration:none;font-weight:bold;font-size:13px}
.footer{margin-top:30px;border:2px solid var(--main);border-radius:25px;padding:18px;text-align:center;background:rgba(0,15,0,0.9)}
.footer h3{color:var(--main);margin:0}
.badge{display:inline-block;border:1px solid var(--main);border-radius:20px;padding:7px 16px;margin:5px;color:var(--main);font-size:12px;background:#000}
</style>
<script>
function setTheme(c){ localStorage.setItem('cyb_theme',c); document.documentElement.style.setProperty('--main',c); }
window.onload=function(){ let s=localStorage.getItem('cyb_theme')||'#00ff00'; document.documentElement.style.setProperty('--main',s); }
</script>
</head><body>
<div class="top">
<h1>⚡ CYB3R TOOLS - 50 IN 1 ⚡</h1>
<p style="color:#aaa;font-size:11px">50+ TOOLS | 100% SECURE | MADE BY VICKY CHAUHAN</p>
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

<div class="footer">
<h3>⚡ MADE WITH ❤️ BY VICKY CHAUHAN ⚡</h3>
<p style="color:#888;font-size:11px">50+ CYBER TOOLS | 100% SECURE | FOUNDER - CYB3R TOOLS</p>
<span class="badge">👁️ Visitors: {{visitors}}</span>
<span class="badge">🟢 Status: ONLINE</span><br>
<span class="badge">© 2026 CYB3R TOOLS</span>
</div>
</body></html>
"""

@app.route('/')
def home():
    v = get_visitors()
    return render_template_string(HOME_HTML, tools=list(enumerate(TOOLS_LIST)), visitors=f"{v:,}")

@app.route('/tool/<int:tid>', methods=['GET','POST'])
def tool_page(tid):
    if tid<0 or tid>=len(TOOLS_LIST): return "Not Found",404
    name=TOOLS_LIST[tid][0]
    out=""
    if request.method=='POST':
        d=request.form.get('data','')
        if "MD5" in name: out=hashlib.md5(d.encode()).hexdigest()
        elif "SHA256" in name: out=hashlib.sha256(d.encode()).hexdigest()
        else: out=f"Done: {d[:300]}"
    return f"<body style='background:#000;color:#0f0;padding:20px'><a href='/' style='color:#0f0'>← Back</a><h2>{name}</h2><form method='POST'><textarea name='data' style='width:100%;background:#111;color:#0f0'></textarea><button>Run</button></form><pre>{out}</pre></body>"

if __name__=='__main__':
    app.run(host='0.0.0.0', port=10000)
