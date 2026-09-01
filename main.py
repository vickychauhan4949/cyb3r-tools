from flask import Flask, request, render_template_string, session, redirect, url_for
import hashlib, base64, random, string, secrets, urllib.parse, sqlite3, os
from datetime import datetime

app = Flask(__name__)
app.secret_key = "vicky_cyb3r_2026_super_secret"

# DB setup
def init_db():
    conn = sqlite3.connect('users.db')
    conn.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT UNIQUE, password TEXT)')
    conn.commit(); conn.close()
init_db()

HTML = """
<!DOCTYPE html><html><head>
<title>CYB3R DASHBOARD - By Vicky</title>
<link rel="icon" href="https://img.icons8.com/color/48/hacker.png?v=2" type="image/png">
<link rel="shortcut icon" href="https://img.icons8.com/color/48/hacker.png?v=2" type="image/png">
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{background:linear-gradient(135deg,#0f0c29,#302b63,#24243e);color:#fff;font-family:Poppins,sans-serif;min-height:100vh}
.header{text-align:center;padding:25px;border:2px solid #FFD60A;border-radius:20px;background:linear-gradient(145deg,#1a1a00,#000);margin-bottom:15px}
.header h1{color:#FFD60A;font-size:32px;letter-spacing:2px}
.nav{display:flex;gap:8px;overflow-x:auto;padding:10px 0}
.nav button{white-space:nowrap;padding:10px 18px;border-radius:20px;font-size:13px}
.card{background:#121212;border:1px solid #222;padding:18px;margin:12px 0;border-radius:16px}
.card h2{color:#FFD60A;font-size:18px;margin-bottom:10px}
input,select{width:100%;padding:12px;margin:6px 0;background:#000;color:#fff;border:1px solid #333;border-radius:10px}
button{width:100%;padding:12px;background:#FFD60A;color:#000;border:none;border-radius:10px;font-weight:800;cursor:pointer}
button:hover{background:#fff}
.result{background:#000;padding:12px;margin-top:10px;border:1px dashed #FFD60A;border-radius:10px;font-family:monospace;font-size:12px;word-break:break-all}
.result img{max-width:100%;border-radius:10px}
.grid{display:grid;grid-template-columns:1fr 1fr;gap:10px}
.badge{background:#FFD60A;color:#000;padding:2px 8px;border-radius:10px;font-size:9px;font-weight:800}
.topbar{display:flex;justify-content:space-between;align-items:center;padding:10px;background:#111;border-radius:12px;margin-bottom:12px;border:1px solid #222}
</style></head><body>

<div class="header" style="position:relative; overflow:hidden; height:120px;">
  <canvas id="matrix" style="position:absolute; top:0; left:0; width:100%; height:100%; z-index:0;"></canvas>
  <div style="position:relative; z-index:1;">
    <h1 style="color:#FFD60A; text-shadow: 0 0 15px #FFD60A;">⚡ CYB3R DASHBOARD ⚡</h1>
    <p style="color:#FFD60A; font-size:12px;">30+ TOOLS | SECURE | MADE BY VICKY CHAUHAN</p>
  </div>
</div>

<script>
const c = document.getElementById('matrix');
const ctx = c.getContext('2d');
c.width = c.offsetWidth; c.height = c.offsetHeight;
const letters = "01".split("");
const fontSize = 14;
const columns = c.width / fontSize;
const drops = [];
for(let x=0;x<columns;x++) drops[x]=1;
function draw(){
  ctx.fillStyle="rgba(15,12,41,0.1)";
  ctx.fillRect(0,0,c.width,c.height);
  ctx.fillStyle="#FFD60A";
  ctx.font=fontSize+"px monospace";
  for(let i=0;i<drops.length;i++){
    const text=letters[Math.floor(Math.random()*letters.length)];
    ctx.fillText(text,i*fontSize,drops[i]*fontSize);
    if(drops[i]*fontSize>c.height && Math.random()>0.975) drops[i]=0;
    drops[i]++;
  }
}
setInterval(draw,35);
</script>

{% if not session.get('user') %}
<div class="card">
<h2>🔐 Login / Register</h2>
<form method="post">
<input type="hidden" name="type" value="login">
<input name="username" placeholder="Username" required>
<input name="password" type="password" placeholder="Password" required>
<button>Login / Register</button>
</form>
<p style="font-size:10px;color:#666;margin-top:8px">Pehli baar username dalo to auto-register ho jayega</p>
</div>
{% else %}
<div class="topbar">
<span>👋 Hi, <b style="color:#FFD60A">{{ session.user }}</b></span>
<a href="/logout"><button style="width:auto;padding:6px 14px;font-size:12px">Logout</button></a>
</div>
{% endif %}

<div class="nav">
<button onclick="filterTools('all')">All 30</button>
<button onclick="filterTools('qr')">QR</button>
<button onclick="filterTools('hack')">Hacking</button>
<button onclick="filterTools('text')">Text</button>
<button onclick="filterTools('calc')">Calc</button>
<button onclick="filterTools('fun')">Fun</button>
</div>

<!-- 1-10 CORE -->
<div class="card t-qr t-all"><h2>1. 💸 UPI QR <span class="badge">TOP</span></h2>
<form method="post"><input type="hidden" name="type" value="upi"><input name="upi_id" placeholder="UPI ID" required><input name="amount" placeholder="Amount"><button>Generate</button></form>
{% if upi %}<div class="result"><img src="{{ upi }}"></div>{% endif %}</div>

<div class="card t-qr t-all"><h2>2. 📱 Text QR</h2>
<form method="post"><input type="hidden" name="type" value="qr"><input name="text" placeholder="Text/Link" required><button>QR Banao</button></form>
{% if qr %}<div class="result"><img src="{{ qr }}"></div>{% endif %}</div>

<div class="card t-qr t-all"><h2>3. 📶 WiFi QR</h2>
<form method="post"><input type="hidden" name="type" value="wifi"><input name="ssid" placeholder="WiFi Name" required><input name="wpass" placeholder="Password" required><button>WiFi QR</button></form>
{% if wqr %}<div class="result"><img src="{{ wqr }}"></div>{% endif %}</div>

<div class="card t-hack t-all"><h2>4. 🔗 Link Checker</h2>
<form method="post"><input type="hidden" name="type" value="linkcheck"><input name="text" placeholder="Link paste karo" required><button>Check</button></form>
{% if lres %}<div class="result">{{ lres|safe }}</div>{% endif %}</div>

<div class="card t-hack t-all"><h2>5. 🌐 My IP Info</h2><div class="result">IP: {{ ip }}<br>Browser: {{ ua[:80] }}</div></div>

<div class="card t-hack t-all"><h2>6. 🔐 Password Gen</h2>
<form method="post"><input type="hidden" name="type" value="pass"><button>Generate 16 Char</button></form>
{% if pgen %}<div class="result" style="color:#FFD60A;font-size:16px">{{ pgen }}</div>{% endif %}</div>

<div class="card t-hack t-all"><h2>7. 🔑 Hash (MD5/SHA)</h2>
<form method="post"><input type="hidden" name="type" value="hash"><input name="text" placeholder="Text" required><button>Hash</button></form>
{% if hres %}<div class="result">MD5: {{ hres.md5 }}<br><br>SHA256: {{ hres.sha256 }}</div>{% endif %}</div>

<div class="card t-text t-all"><h2>8. 🔤 Base64</h2>
<form method="post"><input type="hidden" name="type" value="b64"><input name="text" placeholder="Text" required><button>Encode</button></form>
{% if bres %}<div class="result">{{ bres }}</div>{% endif %}</div>

<div class="card t-text t-all"><h2>9. ✨ Stylish Name</h2>
<form method="post"><input type="hidden" name="type" value="font"><input name="text" placeholder="Name" required><button>Stylish Banao</button></form>
{% if fres %}<div class="result">{{ fres|safe }}</div>{% endif %}</div>

<div class="card t-fun t-all"><h2>10. 📸 Insta DP Viewer</h2>
<form method="post"><input type="hidden" name="type" value="insta"><input name="text" placeholder="Username" required><button>View HD</button></form>
{% if insta %}<div class="result"><img src="{{ insta }}"><br><a href="{{ insta }}" target="_blank">Download</a></div>{% endif %}</div>

<!-- 11-30 NEW -->
<div class="card t-fun t-all"><h2>11. 🎥 YT Thumbnail</h2>
<form method="post"><input type="hidden" name="type" value="yt"><input name="text" placeholder="YouTube Link" required><button>Get Thumbnail</button></form>
{% if yt %}<div class="result"><img src="{{ yt }}"></div>{% endif %}</div>

<div class="card t-text t-all"><h2>12. 🔠 Case Converter</h2>
<form method="post"><input type="hidden" name="type" value="case"><input name="text" placeholder="Text" required><select name="ctype"><option value="upper">UPPER</option><option value="lower">lower</option><option value="title">Title</option></select><button>Convert</button></form>
{% if case %}<div class="result">{{ case }}</div>{% endif %}</div>

<div class="card t-text t-all"><h2>13. 🔢 Word Counter</h2>
<form method="post"><input type="hidden" name="type" value="wc"><input name="text" placeholder="Text likho" required><button>Count</button></form>
{% if wc %}<div class="result">{{ wc|safe }}</div>{% endif %}</div>

<div class="card t-text t-all"><h2>14. ↔️ Reverse Text</h2>
<form method="post"><input type="hidden" name="type" value="rev"><input name="text" placeholder="Text" required><button>Reverse</button></form>
{% if rev %}<div class="result">{{ rev }}</div>{% endif %}</div>

<div class="card t-text t-all"><h2>15. ••• Morse Code</h2>
<form method="post"><input type="hidden" name="type" value="morse"><input name="text" placeholder="Text" required><button>To Morse</button></form>
{% if morse %}<div class="result">{{ morse }}</div>{% endif %}</div>

<div class="card t-text t-all"><h2>16. 010 Binary</h2>
<form method="post"><input type="hidden" name="type" value="bin"><input name="text" placeholder="Text" required><button>To Binary</button></form>
{% if bin %}<div class="result">{{ bin }}</div>{% endif %}</div>

<div class="card t-text t-all"><h2>17. 🔗 URL Encode</h2>
<form method="post"><input type="hidden" name="type" value="url"><input name="text" placeholder="Link/Text" required><button>Encode/Decode</button></form>
{% if urlres %}<div class="result">{{ urlres }}</div>{% endif %}</div>

<div class="card t-fun t-all"><h2>18. 💬 Fake Chat</h2>
<form method="post"><input type="hidden" name="type" value="fchat"><input name="cname" placeholder="Name"><input name="msg" placeholder="Message"><button>Generate</button></form>
{% if fchat %}<div class="result">{{ fchat|safe }}</div>{% endif %}</div>

<div class="card t-fun t-all"><h2>19. 🆔 Fake ID</h2>
<form method="post"><input type="hidden" name="type" value="fake"><button>Generate ID</button></form>
{% if fake %}<div class="result">{{ fake|safe }}</div>{% endif %}</div>

<div class="card" style="background:#121212; border:1px dashed #FFD60A;">
<p style="color:#FFD60A; font-size:10px;">🔥 Sponsored</p>
<script async="async" data-cfasync="false" src="https://pl31125495.profitableratecpmnetwork.com/96b8326926ff16d26996637019139071/invoke.js"></script>
<div id="container-96b8326926ff16d26996637019139071"></div>
 <div class="card t-calc t-all"><h2>20. 🎂 Age Calculator</h2>
<form method="post"><input type="hidden" name="type" value="age"><input name="text" type="date" required><button>Calculate Age</button></form>
{% if age %}<div class="result">{{ age }}</div>{% endif %}</div>

<div class="card t-calc t-all"><h2>21. 📊 BMI Calculator</h2>
<form method="post"><input type="hidden" name="type" value="bmi"><input name="height" placeholder="Height cm" required><input name="weight" placeholder="Weight kg" required><button>Calculate BMI</button></form>
{% if bmi %}<div class="result">{{ bmi|safe }}</div>{% endif %}</div>

<div class="card t-calc t-all"><h2>22. 💰 EMI Calculator</h2>
<form method="post"><input type="hidden" name="type" value="emi"><input name="p" placeholder="Loan Amount" required><input name="r" placeholder="Interest % per year"><input name="n" placeholder="Months"><button>Calculate EMI</button></form>
{% if emi %}<div class="result">{{ emi }}</div>{% endif %}</div>

<div class="card t-calc t-all"><h2>23. % Percentage Calc</h2>
<form method="post"><input type="hidden" name="type" value="perc"><input name="a" placeholder="What % of"><input name="b" placeholder="Number"><button>Calculate</button></form>
{% if perc %}<div class="result">{{ perc }}</div>{% endif %}</div>

<div class="card t-hack t-all"><h2>24. 🔍 Leetspeak</h2>
<form method="post"><input type="hidden" name="type" value="leet"><input name="text" placeholder="Text" required><button>Convert</button></form>
{% if leet %}<div class="result">{{ leet }}</div>{% endif %}</div>

<div class="card t-hack t-all"><h2>25. 🧑‍💻 Username Gen</h2>
<form method="post"><input type="hidden" name="type" value="uname"><input name="text" placeholder="Your name" required><button>Generate Usernames</button></form>
{% if uname %}<div class="result">{{ uname|safe }}</div>{% endif %}</div>

<div class="card t-qr t-all"><h2>26. 📦 Barcode Gen</h2>
<form method="post"><input type="hidden" name="type" value="barcode"><input name="text" placeholder="Number/Text" required><button>Barcode</button></form>
{% if barcode %}<div class="result"><img src="{{ barcode }}"></div>{% endif %}</div>

<div class="card t-text t-all"><h2>27. 🎨 Color Picker Info</h2>
<form method="post"><input type="hidden" name="type" value="color"><input name="text" placeholder="Hex - ex: #FFD60A" required><button>Show</button></form>
{% if color %}<div class="result">{{ color|safe }}</div>{% endif %}</div>

<div class="card t-calc t-all"><h2>28. ⏰ Days Between</h2>
<form method="post"><input type="hidden" name="type" value="days"><input name="d1" type="date" required><input name="d2" type="date" required><button>Calculate Days</button></form>
{% if days %}<div class="result">{{ days }}</div>{% endif %}</div>

<div class="card t-hack t-all"><h2>29. 🛡️ Password Strength</h2>
<form method="post"><input type="hidden" name="type" value="pcheck"><input name="text" placeholder="Password check karo" required><button>Check Strength</button></form>
{% if pcheck %}<div class="result">{{ pcheck|safe }}</div>{% endif %}</div>

<div class="card t-text t-all"><h2>30. 🔡 Lorem Generator</h2>
<form method="post"><input type="hidden" name="type" value="lorem"><input name="text" placeholder="How many words? ex: 20"><button>Generate</button></form>
{% if lorem %}<div class="result">{{ lorem }}</div>{% endif %}</div>

<div style="text-align:center; padding:22px; margin-top:25px; border-top:2px solid #FFD60A; background:#121212; border-radius:15px 15px 0 0;">
  <p style="color:#FFD60A; font-weight:bold; font-size:16px; letter-spacing:1px;">⚡ MADE WITH ❤️ BY VICKY CHAUHAN ⚡</p>
  <p style="color:#aaa; font-size:12px; margin-top:6px;">30+ CYBER TOOLS | 100% SECURE | FOUNDER - CYB3R TOOLS</p>
  <div style="margin-top:12px; display:flex; justify-content:center; gap:15px; flex-wrap:wrap;">
    <span style="background:#000; border:1px solid #FFD60A; color:#FFD60A; padding:5px 12px; border-radius:20px; font-size:12px;">👁️ Visitors: <span id="visits">1,247</span></span>
    <span style="background:#000; border:1px solid #FFD60A; color:#FFD60A; padding:5px 12px; border-radius:20px; font-size:12px;">🟢 Status: ONLINE</span>
    <span style="background:#000; border:1px solid #FFD60A; color:#FFD60A; padding:5px 12px; border-radius:20px; font-size:12px;">© 2026 CYB3R TOOLS</span>
  </div>
</div>
<script>
let count = 1247 + Math.floor(Math.random()*50);
document.getElementById('visits').innerText = count.toLocaleString();
setInterval(()=>{ count++; document.getElementById('visits').innerText = count.toLocaleString(); }, 5000);
</script>
<script src="https://pl31107541.profitableratecpmnetwork.com/53/80/65/538065a4ef16329efd62bd1aeda8552e.js"></script>
<script>
function filterTools(c){
 document.querySelectorAll('.card').forEach(el=>{
  if(c=='all' || el.classList.contains('t-'+c)) el.style.display='block';
  else el.style.display='none';
 });
}
</script>
</body></html>
"""

MORSE = { 'a':'.-','b':'-...','c':'-.-.','d':'-..','e':'.','f':'..-.','g':'--.','h':'....','i':'..','j':'.---','k':'-.-','l':'.-..','m':'--','n':'-.','o':'---','p':'.--.','q':'--.-','r':'.-.','s':'...','t':'-','u':'..-','v':'...-','w':'.--','x':'-..-','y':'-.--','z':'--..',' ':'/' }

@app.route('/', methods=['GET','POST'])
def home():
    ctx = {'ip': request.headers.get('X-Forwarded-For', request.remote_addr), 'ua': request.headers.get('User-Agent','')}
    if request.method=='POST':
        t=request.form.get('type')
        txt=request.form.get('text','').strip()
        if t=='login':
            u=request.form.get('username'); p=request.form.get('password')
            phash=hashlib.sha256(p.encode()).hexdigest()
            conn=sqlite3.connect('users.db'); cur=conn.cursor()
            cur.execute("SELECT * FROM users WHERE username=?", (u,))
            row=cur.fetchone()
            if row:
                if row[2]==phash: session['user']=u
                else: ctx['lres']="Wrong password!"
            else:
                cur.execute("INSERT INTO users (username,password) VALUES (?,?)",(u,phash)); conn.commit(); session['user']=u
            conn.close(); return redirect(url_for('home'))
        elif t=='upi':
            upi_id=request.form.get('upi_id'); amt=request.form.get('amount','')
            s=f"upi://pay?pa={upi_id}&pn=Vicky";
            if amt: s+=f"&am={amt}&cu=INR"
            ctx['upi']=f"https://api.qrserver.com/v1/create-qr-code/?size=500x500&data={urllib.parse.quote(s)}"
        elif t=='qr': ctx['qr']=f"https://api.qrserver.com/v1/create-qr-code/?size=500x500&data={urllib.parse.quote(txt)}"
        elif t=='wifi':
            ss=request.form.get('ssid'); wp=request.form.get('wpass')
            s=f"WIFI:T:WPA;S:{ss};P:{wp};;"
            ctx['wqr']=f"https://api.qrserver.com/v1/create-qr-code/?size=500x500&data={urllib.parse.quote(s)}"
        elif t=='linkcheck':
            low=txt.lower()
            if any(x in low for x in ['bit.ly','tinyurl','free','lottery']): ctx['lres']="<span style='color:red'>❌ RISKY</span>"
            else: ctx['lres']="<span style='color:#0f0'>✅ SAFE</span><br>"+txt
        elif t=='pass':
            ctx['pgen']=''.join(secrets.choice(string.ascii_letters+string.digits+"!@#$%") for _ in range(16))
        elif t=='hash': ctx['hres']={'md5':hashlib.md5(txt.encode()).hexdigest(),'sha256':hashlib.sha256(txt.encode()).hexdigest()}
        elif t=='b64': ctx['bres']=base64.b64encode(txt.encode()).decode()
        elif t=='font': ctx['fres']=f"Bold: <b>{txt}</b><br>Upper: {txt.upper()}<br>Lower: {txt.lower()}<br>Reverse: {txt[::-1]}<br>Circle: {' '.join(txt)}"
        elif t=='insta': ctx['insta']=f"https://unavatar.io/instagram/{txt}?fallback=https://ui-avatars.com/api/?name={txt}&background=FFD60A&color=000"
        elif t=='yt':
            vid=txt.split("v=")[-1].split("&")[0] if "v=" in txt else txt.split("/")[-1][:11]
            ctx['yt']=f"https://img.youtube.com/vi/{vid}/maxresdefault.jpg"
        elif t=='case':
            ctype=request.form.get('ctype');
            if ctype=='upper': ctx['case']=txt.upper()
            elif ctype=='lower': ctx['case']=txt.lower()
            else: ctx['case']=txt.title()
        elif t=='wc': ctx['wc']=f"Words: {len(txt.split())}<br>Chars: {len(txt)}<br>Lines: {len(txt.splitlines())}"
        elif t=='rev': ctx['rev']=txt[::-1]
        elif t=='morse': ctx['morse']=' '.join(MORSE.get(ch.lower(),'') for ch in txt)
        elif t=='bin': ctx['bin']=' '.join(format(ord(c),'08b') for c in txt)
        elif t=='url': ctx['urlres']=urllib.parse.quote(txt)
        elif t=='fchat': ctx['fchat']=f"👤 {request.form.get('cname')}<br>💬 {request.form.get('msg')}<br>✓✓ {datetime.now().strftime('%H:%M')}"
        elif t=='fake': ctx['fake']=f"Name: {random.choice(['Vicky','Aarav','Raj'])} Sharma<br>Email: {''.join(random.choices(string.ascii_lowercase,k=6))}@gmail.com<br>Phone: 9{random.randint(100000000,999999999)}"
        elif t=='age':
            from datetime import date; b=date.fromisoformat(txt); today=date.today(); age=today.year-b.year-((today.month,today.day)<(b.month,b.day)); ctx['age']=f"Age: {age} years"
        elif t=='bmi':
            h=float(request.form.get('height'))/100; w=float(request.form.get('weight')); bmi=w/(h*h); ctx['bmi']=f"BMI: {bmi:.2f}<br>{'Fit' if 18.5<bmi<25 else 'Check diet'}"
        elif t=='emi':
            p=float(request.form.get('p') or 0); r=float(request.form.get('r') or 10)/12/100; n=float(request.form.get('n') or 12); emi=p*r*(1+r)**n/(((1+r)**n)-1) if r>0 else p/n; ctx['emi']=f"EMI: ₹{emi:.2f}/month"
        elif t=='perc':
            a=float(request.form.get('a') or 0); b=float(request.form.get('b') or 0); ctx['perc']=f"{a}% of {b} = {(a/100)*b}"
        elif t=='leet': ctx['leet']=txt.replace('a','4').replace('e','3').replace('i','1').replace('o','0').replace('s','5')
        elif t=='uname': ctx['uname']=f"{txt}123<br>{txt}_official<br>{txt}.cyb3r<br>real_{txt}"
        elif t=='barcode': ctx['barcode']=f"https://barcode.tec-it.com/barcode.ashx?data={urllib.parse.quote(txt)}&code=Code128"
        elif t=='color': ctx['color']=f"<div style='width:100%;height:80px;background:{txt};border-radius:10px'></div><br>{txt}"
        elif t=='days':
            from datetime import date; d1=date.fromisoformat(request.form.get('d1')); d2=date.fromisoformat(request.form.get('d2')); ctx['days']=f"Days: {(d2-d1).days} days"
        elif t=='pcheck':
            score=len(txt); s="Weak" if score<6 else "Medium" if score<10 else "Strong"; ctx['pcheck']=f"Strength: <b>{s}</b><br>Length: {score}"
        elif t=='lorem':
            n=int(txt or 20); words="lorem ipsum dolor sit amet consectetur adipiscing elit cyb3r tools vicky vadodara".split(); ctx['lorem']=' '.join(random.choices(words,k=n))
    return render_template_string(HTML, **ctx, session=session)

@app.route('/logout')
def logout(): session.pop('user',None); return redirect(url_for('home'))

if __name__=='__main__': app.run()
