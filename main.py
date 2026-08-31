from flask import Flask, render_template_string

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>CYB3R Tools - Vicky</title>
<style>
body{background:#0a0a0a;color:#00ff88;font-family:monospace;padding:20px}
h1{text-align:center;text-shadow:0 0 10px #00ff88;font-size:32px}
.card{background:#111;border:1px solid #00ff88;border-radius:12px;padding:20px;margin:20px 0;box-shadow:0 0 15px #00ff8855}
input,button{width:100%;padding:12px;margin:10px 0;border-radius:8px;border:none;font-size:16px}
input{background:#222;color:white;border:1px solid #00ff88}
button{background:#00ff88;color:black;font-weight:bold;cursor:pointer}
.result{margin-top:10px;padding:10px;background:#000;border-radius:8px}
</style>
</head>
<body>
<h1>⚡ CYB3R TOOLS ⚡</h1>
<p style="text-align:center">By Vicky Chauhan - Ethical Hacker</p>

<div class="card">
<h3>🔐 Password Strength Checker</h3>
<input id="pass" placeholder="Enter password">
<button onclick="checkPass()">Check Strength</button>
<div id="passRes" class="result"></div>
</div>

<div class="card">
<h3>🔗 Link Scanner</h3>
<input id="link" placeholder="https://example.com">
<button onclick="checkLink()">Scan Link</button>
<div id="linkRes" class="result"></div>
</div>

<div class="card">
<h3>🎣 Phishing Detector</h3>
<input id="phish" placeholder="Enter suspicious email/text">
<button onclick="checkPhish()">Detect</button>
<div id="phishRes" class="result"></div>
</div>

<script>
function checkPass(){
 let p=document.getElementById('pass').value;
 let s=0;
 if(p.length>8)s++; if(/[A-Z]/.test(p))s++; if(/[0-9]/.test(p))s++; if(/[^A-Za-z0-9]/.test(p))s++;
 let r=["Very Weak 🔴","Weak 🟠","Medium 🟡","Strong 🟢","Very Strong 💪"];
 document.getElementById('passRes').innerText=r[s]||r[0];
}
function checkLink(){
 let l=document.getElementById('link').value;
 let bad=["bit.ly","tinyurl","free-money","login-verify"];
 let isBad=bad.some(b=>l.includes(b)) ||!l.startsWith("https");
 document.getElementById('linkRes').innerText=isBad?"⚠️ Suspicious Link!":"✅ Link Looks Safe";
}
function checkPhish(){
 let t=document.getElementById('phish').value.toLowerCase();
 let k=["urgent","verify your account","click immediately","lottery winner","bank blocked"];
 let isPhish=k.some(w=>t.includes(w));
 document.getElementById('phishRes').innerText=isPhish?"🚨 Phishing Detected!":"✅ No Phishing Found";
}
</script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
