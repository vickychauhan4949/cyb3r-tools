from flask import Flask, request, jsonify
import re, requests, os

app = Flask(__name__)

@app.route('/')
def home():
    html = """
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>CYB3R TOOLS</title>
<style>
body{background:#000;color:#fff;font-family:Arial;padding:12px;margin:0}
.card{background:#111;border:1px solid #333;padding:16px;border-radius:14px;margin-bottom:14px}
input{width:93%;padding:11px;border-radius:8px;border:1px solid #444;background:#000;color:#fff;margin-top:7px}
button{padding:11px;background:#ffcc00;color:#000;border:none;border-radius:8px;margin-top:9px;width:100%;font-weight:bold;font-size:16px}
h2{color:#ffcc00}
</style>
</head>
<body>
<h1 style="text-align:center;color:#ffcc00">CYB3R TOOLS by Vicky</h1>

<div class="card"><h2>1. UPI QR Generator</h2>
<input id="upi" placeholder="UPI ID - ex: vicky@upi">
<input id="name" placeholder="Name - ex: Vicky">
<button onclick="makeQR()">Generate QR</button>
<div id="qr" style="text-align:center;margin-top:10px"></div>
</div>

<div class="card"><h2>2. Link Safety Checker</h2>
<input id="link" placeholder="Link paste karo">
<button onclick="checkLink()">Check Now</button>
<p id="r2"></p>
</div>

<div class="card"><h2>3. Insta Direct Download</h2>
<input id="insta" placeholder="Insta Reel Link">
<button onclick="downloadInsta()">Get Download Link</button>
<p id="r3"></p>
</div>

<script>
function makeQR(){
 let upi=document.getElementById('upi').value;
 let name=document.getElementById('name').value||'Vicky';
 if(!upi){alert('UPI ID daalo');return}
 let data=`upi://pay?pa=${upi}&pn=${name}`;
 let url=`https://api.qrserver.com/v1/create-qr-code/?size=300x300&data=`+encodeURIComponent(data);
 document.getElementById('qr').innerHTML=`<br><img src="${url}" style="background:#fff;padding:10px;border-radius:10px">`;
}
function checkLink(){
 let l=document.getElementById('link').value.toLowerCase();
 let r=document.getElementById('r2');
 if(l.includes('.tk')||l.includes('.ml')||l.includes('free')||l.length>90){
   r.innerHTML='⚠️ <span style="color:red">FAKE / RISKY LINK</span>';
 } else {
   r.innerHTML='✅ <span style="color:lightgreen">Safe Lag Raha Hai</span>';
 }
}
async function downloadInsta(){
 let link=document.getElementById('insta').value;
 if(!link){alert('Link daalo');return}
 document.getElementById('r3').innerHTML='⏳ Wait...';
 let res=await fetch('/api/insta?url='+encodeURIComponent(link));
 let d=await res.json();
 if(d.video_url){
   document.getElementById('r3').innerHTML='<br><a href="'+d.video_url+'" target="_blank"><button style="width:auto;background:#00ff88">Direct Download</button></a>';
 } else {
   document.getElementById('r3').innerHTML='❌ Video nahi mila';
 }
}
</script>
</body>
</html>
"""
    return html

@app.route('/api/insta')
def insta_api():
    url=request.args.get('url','')
    try:
        r=requests.get(url, headers={'User-Agent':'Mozilla/5.0'}, timeout=15)
        m=re.search(r'"video_url":"([^"]+)"', r.text)
        if m:
            return jsonify({'video_url': m.group(1).replace('\\u0026','&')})
        return jsonify({'error':'not found'})
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__=='__main__':
    port=int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
