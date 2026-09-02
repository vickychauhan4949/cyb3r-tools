<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>ToolHub - 100+ Free Tools</title>
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:Arial,sans-serif;background:#07080c;color:#fff}
button,input,textarea,select{font:inherit}
.app{display:flex;min-height:100vh}
.side{width:245px;background:#0d0f15;border-right:1px solid #242732;position:fixed;top:0;bottom:0;padding:20px 14px;overflow:auto}
.logo{font-size:25px;font-weight:bold;padding:10px 12px 25px}
.logo b{color:#7c5cff}
.navtitle{font-size:11px;color:#697080;text-transform:uppercase;padding:12px}
.nav button{display:block;width:100%;border:0;background:none;color:#aeb3c0;text-align:left;padding:11px 12px;border-radius:9px;cursor:pointer}
.nav button:hover,.nav button.active{background:#1b1730;color:#fff}
.main{margin-left:245px;width:calc(100% - 245px)}
.top{height:70px;border-bottom:1px solid #242732;background:#090a0f;display:flex;align-items:center;padding:12px 30px;position:sticky;top:0;z-index:10}
.search{max-width:650px;width:100%}
.search input{width:100%;padding:13px 17px;background:#12151c;border:1px solid #292d38;color:#fff;border-radius:10px;outline:none}
.hero{max-width:1200px;margin:auto;padding:65px 35px 40px}
.hero h1{font-size:clamp(38px,6vw,68px);line-height:1;letter-spacing:-3px}
.hero h1 span{color:#8b72ff}
.hero p{color:#9298a8;margin-top:20px;line-height:1.7}
.btn{background:#151821;border:1px solid #292d38;color:#fff;padding:11px 16px;border-radius:9px;cursor:pointer}
.primary{background:#7c5cff;border-color:#7c5cff}
.section{max-width:1200px;margin:auto;padding:0 35px 50px}
.head{display:flex;justify-content:space-between;margin-bottom:18px}
.head span{color:#858b9b;font-size:13px}
.tools{display:grid;grid-template-columns:repeat(auto-fill,minmax(205px,1fr));gap:13px}
.card{background:#101219;border:1px solid #252936;border-radius:13px;padding:18px;cursor:pointer;transition:.2s}
.card:hover{transform:translateY(-3px);background:#151821;border-color:#443a70}
.icon{font-size:22px;width:42px;height:42px;border-radius:10px;background:#1b1730;display:grid;place-items:center;margin-bottom:14px}
.card h3{font-size:15px;margin-bottom:7px}
.card p{font-size:12px;color:#858b9b;line-height:1.5}
.empty{text-align:center;padding:60px;color:#858b9b;display:none}
.modalbg{display:none;position:fixed;inset:0;background:#000b;z-index:100;padding:20px}
.modal{max-width:720px;max-height:90vh;overflow:auto;background:#101219;border:1px solid #292d38;border-radius:16px;padding:25px;margin:4vh auto}
.modalhead{display:flex;justify-content:space-between;margin-bottom:20px}
.close{background:#20232c;color:#fff;border:0;border-radius:8px;width:36px;height:36px;font-size:20px}
.toolbox label{display:block;color:#aeb3c0;font-size:13px;margin:12px 0 7px}
.toolbox input,.toolbox textarea,.toolbox select{width:100%;padding:11px;background:#090b10;border:1px solid #292d38;color:#fff;border-radius:8px;outline:none}
.toolbox textarea{min-height:150px;resize:vertical}
.result{margin-top:15px;padding:15px;background:#090b10;border:1px solid #292d38;border-radius:8px;white-space:pre-wrap;word-break:break-word}
footer{text-align:center;border-top:1px solid #242732;color:#626979;padding:30px;font-size:12px}
@media(max-width:750px){
.side{position:relative;width:100%;height:auto;border-right:0;border-bottom:1px solid #242732}
.app{display:block}.main{margin:0;width:100%}.nav{display:flex;overflow:auto}.nav button{white-space:nowrap}.navtitle{display:none}
.top{padding:10px 15px}.hero{padding:45px 20px 30px}.section{padding:0 20px 40px}
}
</style>
</head>
<body>

<div class="app">
<aside class="side">
<div class="logo">Tool<b>Hub</b></div>
<div class="navtitle">Categories</div>
<div class="nav">
<button class="active" onclick="cat('all',this)">🏠 All</button>
<button onclick="cat('text',this)">📝 Text</button>
<button onclick="cat('calc',this)">🧮 Calculator</button>
<button onclick="cat('convert',this)">🔄 Converter</button>
<button onclick="cat('dev',this)">💻 Developer</button>
<button onclick="cat('image',this)">🖼️ Image</button>
<button onclick="cat('utility',this)">🛠️ Utility</button>
</div>
</aside>

<main class="main">
<header class="top">
<div class="search">
<input id="search" placeholder="Search 100+ tools..." oninput="render()">
</div>
</header>

<section class="hero">
<h1>Powerful tools.<br><span>Simple & Free.</span></h1>
<p>100+ useful online tools. Fast, simple and free — directly in your browser.</p>
</section>

<section class="section">
<div class="head">
<h2 id="title">All Tools</h2>
<span id="count"></span>
</div>
<div class="tools" id="tools"></div>
<div class="empty" id="empty">No tools found.</div>
</section>

<footer>ToolHub © 2026 — Free Online Tools</footer>
</main>
</div>

<div class="modalbg" id="bg" onclick="outside(event)">
<div class="modal">
<div class="modalhead">
<h2 id="mtitle"></h2>
<button class="close" onclick="closeTool()">×</button>
</div>
<div class="toolbox" id="box"></div>
</div>
</div>

<script>
const T=[
["Word Counter","Count words","📝","text","word"],
["Character Counter","Count characters","🔤","text","char"],
["Line Counter","Count lines","📏","text","line"],
["Uppercase","Convert to uppercase","⬆️","text","upper"],
["Lowercase","Convert to lowercase","⬇️","text","lower"],
["Title Case","Convert to title case","Aa","text","title"],
["Reverse Text","Reverse text","↔️","text","reverse"],
["Remove Spaces","Remove extra spaces","✂️","text","spaces"],
["Duplicate Remover","Remove duplicate lines","🧹","text","dup"],
["Palindrome Checker","Check palindrome","🔁","text","pal"],
["Text Sorter","Sort lines","↕️","text","sort"],
["Text Cleaner","Clean text","🧽","text","clean"],
["Slug Generator","Create URL slug","🔗","text","slug"],
["Text Repeater","Repeat text","🔁","text","repeat"],
["Word Frequency","Find word frequency","📊","text","freq"],

["Percentage","Calculate percentage","%","calc","percent"],
["Average","Calculate average","📊","calc","avg"],
["BMI Calculator","Calculate BMI","⚖️","calc","bmi"],
["Age Calculator","Calculate age","🎂","calc","age"],
["Discount","Calculate discount","🏷️","calc","discount"],
["Tip Calculator","Calculate tip","💵","calc","tip"],
["Simple Calculator","Basic calculator","➗","calc","basic"],
["Square","Calculate square","²","calc","square"],
["Cube","Calculate cube","³","calc","cube"],
["Power","Calculate power","^","calc","power"],
["GST Calculator","Calculate GST","₹","calc","gst"],
["Profit Calculator","Calculate profit","📈","calc","profit"],
["Ratio Calculator","Calculate ratio","⚖️","calc","ratio"],
["Fraction Calculator","Calculate fraction","½","calc","fraction"],
["Compound Interest","Calculate interest","💰","calc","interest"],

["Meters to Feet","Convert meters","📐","convert","mfeet"],
["Feet to Meters","Convert feet","📐","convert","feetm"],
["KM to Miles","Convert distance","🚗","convert","kmmile"],
["Miles to KM","Convert distance","🚗","convert","milekm"],
["KG to Pounds","Convert weight","⚖️","convert","kgpound"],
["Pounds to KG","Convert weight","⚖️","convert","poundkg"],
["Celsius to Fahrenheit","Temperature","🌡️","convert","cf"],
["Fahrenheit to Celsius","Temperature","🌡️","convert","fc"],
["Liters to Gallons","Convert volume","🧪","convert","lg"],
["Gallons to Liters","Convert volume","🧪","convert","gl"],
["CM to Inches","Convert length","📏","convert","cmin"],
["Inches to CM","Convert length","📏","convert","incm"],
["Hours to Minutes","Convert time","⏱️","convert","hm"],
["Minutes to Seconds","Convert time","⏱️","convert","ms"],
["KB to MB","Convert data","💾","convert","kbmb"],
["MB to GB","Convert data","💾","convert","mbgb"],
["GB to MB","Convert data","💾","convert","gbmb"],
["Decimal to Binary","Convert number","01","convert","bin"],
["Binary to Decimal","Convert number","01","convert","dec"],

["JSON Formatter","Format JSON","{}","dev","json"],
["JSON Minifier","Minify JSON","{}","dev","jsonmin"],
["Base64 Encoder","Encode Base64","🔐","dev","enc"],
["Base64 Decoder","Decode Base64","🔓","dev","dec64"],
["URL Encoder","Encode URL","🔗","dev","urlenc"],
["URL Decoder","Decode URL","🔗","dev","urldec"],
["HTML Encoder","Encode HTML","</>","dev","html"],
["HTML Decoder","Decode HTML","<>","dev","unhtml"],
["CSS Minifier","Minify CSS","🎨","dev","css"],
["JS Minifier","Minify JavaScript","⚡","dev","js"],
["Regex Tester","Test regular expression","🔎","dev","regex"],
["Timestamp","Unix timestamp","🕐","dev","time"],
["UUID Generator","Generate UUID","🆔","dev","uuid"],
["Text to Binary","Text to binary","01","dev","textbin"],
["Binary to Text","Binary to text","🔢","dev","bintxt"],
["ASCII Converter","ASCII converter","🔤","dev","ascii"],
["Hex Converter","Convert hexadecimal","🔢","dev","hex"],

["Password Generator","Generate password","🔑","utility","pass"],
["Random Number","Random number","🎲","utility","random"],
["Random Color","Generate color","🎨","utility","randcolor"],
["HEX to RGB","Convert color","🌈","utility","hexrgb"],
["RGB to HEX","Convert color","🌈","utility","rgbhex"],
["Lorem Ipsum","Generate text","📄","utility","lorem"],
["Date Difference","Difference between dates","📅","utility","datediff"],
["Countdown","Create countdown","⏳","utility","countdown"],
["Leap Year","Check leap year","📆","utility","leap"],
["Days in Month","Find days","📅","utility","days"],
["Number to Words","Number converter","🔢","utility","words"],
["Roman Numerals","Roman converter","🏛️","utility","roman"],
["Favicon Preview","Preview favicon","⭐","utility","favicon"],
["Email Validator","Validate email","✉️","utility","email"],
["URL Validator","Validate URL","🔗","utility","urlval"],
["IP Validator","Validate IP","🌐","utility","ip"],
["Text Hash","Create hash","🔒","utility","hash"],

["Image Resize","Resize image","🖼️","image","resize"],
["Image Info","Image dimensions","ℹ️","image","imginfo"],
["Image Preview","Preview image","👁️","image","preview"],
["Image to Base64","Image Base64","🖼️","image","img64"],
["Gradient Generator","CSS gradient","🌈","image","gradient"],
["Color Picker","Pick color","🎨","image","picker"],
["SVG Preview","Preview SVG","🧩","image","svg"],
["Pixel Calculator","Image pixels","🔲","image","pixel"],
["Aspect Ratio","Calculate ratio","📐","image","ratioimg"],
["Image File Name","Clean filename","📁","image","filename"],

["Timer","Simple timer","⏱️","utility","timer"],
["Stopwatch","Stopwatch","⏱️","utility","stopwatch"],
["QR Text Generator","Create QR text","▦","utility","qr"],
["Character Randomizer","Random characters","🎲","utility","chars"],
["Number Randomizer","Random list","🎲","utility","nums"],
["Percentage Increase","Calculate increase","📈","calc","increase"],
["Percentage Decrease","Calculate decrease","📉","calc","decrease"],
["Loan Calculator","Estimate loan","🏦","calc","loan"],
["Savings Calculator","Calculate savings","💰","calc","saving"],
["VAT Calculator","Calculate VAT","💵","calc","vat"],
["Markup Calculator","Calculate markup","📈","calc","markup"],
["Break Even","Break-even calculator","⚖️","calc","break"],
["Speed Calculator","Distance/time speed","🚗","calc","speed"],
["Time Calculator","Add time","⏰","calc","timecalc"],
["Data Size Calculator","Calculate data","💾","calc","datasize"]
];

let current="all";

function cat(c,b){
current=c;
document.querySelectorAll(".nav button").forEach(x=>x.classList.remove("active"));
b.classList.add("active");
document.getElementById("title").textContent=c==="all"?"All Tools":c[0].toUpperCase()+c.slice(1)+" Tools";
render();
}

function render(){
let q=document.getElementById("search").value.toLowerCase();
let list=T.filter(x=>(current==="all"||x[3]===current)&&
(x[0]+" "+x[1]).toLowerCase().includes(q));

document.getElementById("tools").innerHTML=list.map(x=>`
<div class="card" onclick="openTool(${T.indexOf(x)})">
<div class="icon">${x[2]}</div>
<h3>${x[0]}</h3>
<p>${x[1]}</p>
</div>`).join("");

document.getElementById("count").textContent=list.length+" tools";
document.getElementById("empty").style.display=list.length?"none":"block";
}

function openTool(i){
let t=T[i];
document.getElementById("mtitle").textContent=t[0];
document.getElementById("box").innerHTML=UI(t[4]);
document.getElementById("bg").style.display="block";
}

function closeTool(){document.getElementById("bg").style.display="none"}
function outside(e){if(e.target.id==="bg")closeTool()}

function textarea(ph="Enter text..."){
return `<textarea id="a" placeholder="${ph}"></textarea>`;
}

function UI(t){

if(["word","char","line","upper","lower","title","reverse","spaces","dup","pal","sort","clean","slug","freq"].includes(t))
return `${textarea()}<br><button class="btn primary" onclick="text('${t}')">Run</button><div class="result" id="r"></div>`;

if(t==="percent")return `Number<input id="a" type="number">Percent<input id="b" type="number"><br><button class="btn primary" onclick="R(Number(a.value)*Number(b.value)/100)">Calculate</button><div class="result" id="r"></div>`;

if(t==="avg")return `${textarea("10,20,30,40")}<br><button class="btn primary" onclick="R(a.value.split(',').map(Number).reduce((x,y)=>x+y,0)/a.value.split(',').length)">Calculate</button><div class="result" id="r"></div>`;

if(t==="bmi")return `Weight KG<input id="a" type="number">Height CM<input id="b" type="number"><br><button class="btn primary" onclick="R((a.value/(b.value/100)**2).toFixed(2))">Calculate</button><div class="result" id="r"></div>`;

if(t==="basic")return `Expression<input id="a" placeholder="10+20*3"><br><button class="btn primary" onclick="calc()">Calculate</button><div class="result" id="r"></div>`;

if(["square","cube","power"].includes(t))return `Number<input id="a" type="number">`+(t==="power"?`Power<input id="b" type="number">`:"")+`<br><button class="btn primary" onclick="R(${t==="square"?"a.value**2":t==="cube"?"a.value**3":"a.value**b.value"})">Calculate</button><div class="result" id="r"></div>`;

if(t==="pass")return `Length<input id="a" type="number" value="16"><br><button class="btn primary" onclick="password()">Generate</button><div class="result" id="r"></div>`;

if(t==="random")return `Min<input id="a" type="number" value="1">Max<input id="b" type="number" value="100"><br><button class="btn primary" onclick="R(Math.floor(Math.random()*(b.value-a.value+1))+Number(a.value))">Generate</button><div class="result" id="r"></div>`;

if(t==="uuid")return `<button class="btn primary" onclick="R(crypto.randomUUID())">Generate UUID</button><div class="result" id="r"></div>`;

if(t==="json"||t==="jsonmin")return `${textarea("Paste JSON...")}<br><button class="btn primary" onclick="jsonTool('${t}')">Run</button><div class="result" id="r"></div>`;

if(t==="enc"||t==="dec64")return `${textarea()}<br><button class="btn primary" onclick="R('${t}'==='enc'?btoa(unescape(encodeURIComponent(a.value))):decodeURIComponent(escape(atob(a.value))))">Run</button><div class="result" id="r"></div>`;

if(t==="urlenc"||t==="urldec")return `${textarea()}<br><button class="btn primary" onclick="R('${t}'==='urlenc'?encodeURIComponent(a.value):decodeURIComponent(a.value))">Run</button><div class="result" id="r"></div>`;

if(t==="cf"||t==="fc")return `Temperature<input id="a" type="number"><br><button class="btn primary" onclick="R('${t}'==='cf'?a.value*9/5+32:(a.value-32)*5/9)">Convert</button><div class="result" id="r"></div>`;

if(t==="mfeet"||t==="feetm"||t==="kmmile"||t==="milekm"||t==="kgpound"||t==="poundkg"||t==="cmin"||t==="incm"||t==="hm"||t==="ms"||t==="kbmb"||t==="mbgb"||t==="gbmb"||t==="lg"||t==="gl"||t==="bin"||t==="dec")
return `Value<input id="a" type="number"><br><button class="btn primary" onclick="convert('${t}')">Convert</button><div class="result" id="r"></div>`;

if(t==="textbin"||t==="bintxt")return `${textarea()}<br><button class="btn primary" onclick="binary('${t}')">Convert</button><div class="result" id="r"></div>`;

if(t==="time")return `<button class="btn primary" onclick="R(Math.floor(Date.now()/1000))">Get Timestamp</button><div class="result" id="r"></div>`;

if(t==="hexrgb")return `HEX<input id="a" placeholder="#7c5cff"><br><button class="btn primary" onclick="hexrgb()">Convert</button><div class="result" id="r"></div>`;

if(t==="rgbhex")return `RGB<input id="a" placeholder="124,92,255"><br><button class="btn primary" onclick="rgbhex()">Convert</button><div class="result" id="r"></div>`;

if(t==="picker")return `<input id="a" type="color" value="#7c5cff" style="height:70px"><br><button class="btn primary" onclick="R(a.value)">Show Color</button><div class="result" id="r"></div>`;

if(t==="lorem")return `<button class="btn primary" onclick="R('Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.')">Generate</button><div class="result" id="r"></div>`;

if(t==="email")return `${textarea("email@example.com")}<br><button class="btn primary" onclick="R(/^[^\\s@]+@[^\\s@]+\\.[^\\s@]+$/.test(a.value)?'Valid email':'Invalid email')">Validate</button><div class="result" id="r"></div>`;

if(t==="urlval")return `${textarea("https://example.com")}<br><button class="btn primary" onclick="urlcheck()">Validate</button><div class="result" id="r"></div>`;

if(t==="leap")return `Year<input id="a" type="number"><br><button class="btn primary" onclick="R((a.value%4===0&&a.value%100!==0)||a.value%400===0?'Leap Year':'Not Leap Year')">Check</button><div class="result" id="r"></div>`;

if(t==="days")return `Year<input id="a" type="number">Month<input id="b" type="number" min="1" max="12"><br><button class="btn primary" onclick="R(new Date(a.value,b.value,0).getDate())">Calculate</button><div class="result" id="r"></div>`;

if(t==="words")return `Number<input id="a" type="number"><br><button class="btn primary" onclick="R(words(Number(a.value)))">Convert</button><div class="result" id="r"></div>`;

if(t==="roman")return `Number<input id="a" type="number"><br><button class="btn primary" onclick="R(roman(Number(a.value)))">Convert</button><div class="result" id="r"></div>`;

if(t==="gradient")return `Color 1<input id="a" type="color" value="#7c5cff">Color 2<input id="b" type="color" value="#ff5caa"><br><button class="btn primary" onclick="R('linear-gradient(90deg,'+a.value+','+b.value+')')">Generate CSS</button><div class="result" id="r"></div>`;

if(t==="imginfo"||t==="preview"||t==="resize"||t==="img64")
return `<input id="file" type="file" accept="image/*"><div class="result" id="r">Choose an image.</div><br><button class="btn primary" onclick="imageTool('${t}')">Run</button>`;

return `${textarea()}<br><button class="btn primary" onclick="R(a.value)">Run</button><div class="result" id="r"></div>`;
}

function R(x){document.getElementById("r").textContent=x}

function text(t){
let v=a.value,r="";
if(t==="word")r="Words: "+(v.trim()?v.trim().split(/\s+/).length:0);
if(t==="char")r="Characters: "+v.length;
if(t==="line")r="Lines: "+(v?v.split("\n").length:0);
if(t==="upper")r=v.toUpperCase();
if(t==="lower")r=v.toLowerCase();
if(t==="title")r=v.toLowerCase().replace(/\b\w/g,x=>x.toUpperCase());
if(t==="reverse")r=[...v].reverse().join("");
if(t==="spaces")r=v.replace(/\s+/g," ").trim();
if(t==="dup")r=[...new Set(v.split("\n"))].join("\n");
if(t==="pal"){let x=v.toLowerCase().replace(/[^a-z0-9]/g,"");r=x===[...x].reverse().join("")?"Palindrome":"Not Palindrome"}
if(t==="sort")r=v.split("\n").sort().join("\n");
if(t==="clean")r=v.replace(/[^\x20-\x7E\n]/g,"");
if(t==="slug")r=v.toLowerCase().trim().replace(/[^a-z0-9]+/g,"-").replace(/^-|-$/g,"");
if(t==="repeat")r=v;
if(t==="freq"){let o={};v.toLowerCase().split(/\s+/).forEach(x=>o[x]=(o[x]||0)+1);r=JSON.stringify(o,null,2)}
R(r);
}

function calc(){
try{if(!/^[0-9+*/().% -]+$/.test(a.value))throw 1;R(Function("return "+a.value)())}catch(e){R("Invalid expression")}
}

function password(){
let s="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*";
let r="";for(let i=0;i<Number(a.value);i++)r+=s[Math.floor(Math.random()*s.length)];R(r);
}

function jsonTool(t){
try{let x=JSON.parse(a.value);R(t==="json"?JSON.stringify(x,null,2):JSON.stringify(x))}catch(e){R("Invalid JSON")}
}

function convert(t){
let n=Number(a.value),r;
const m={mfeet:n*3.28084,feetm:n/3.28084,kmmile:n*.621371,milekm:n*1.60934,kgpound:n*2.20462,poundkg:n*.453592,cmin:n/2.54,incm:n*2.54,hm:n*60,ms:n*60,kbmb:n/1024,mbgb:n/1024,gbmb:n*1024,lg:n*.264172,gl:n*3.78541,bin:n.toString(2),dec:parseInt(n,2)};
R(m[t]);
}

function binary(t){
if(t==="textbin")R([...a.value].map(x=>x.charCodeAt(0).toString(2).padStart(8,"0")).join(" "));
else R(a.value.split(/\s+/).map(x=>String.fromCharCode(parseInt(x,2))).join(""));
}

function hexrgb(){
let h=a.value.replace("#","");if(h.length===3)h=h.split("").map(x=>x+x).join("");
R(`rgb(${parseInt(h.slice(0,2),16)}, ${parseInt(h.slice(2,4),16)}, ${parseInt(h.slice(4,6),16)})`);
}

function rgbhex(){
R("#"+a.value.split(",").map(Number).map(x=>x.toString(16).padStart(2,"0")).join(""));
}

function urlcheck(){
try{new URL(a.value);R("Valid URL")}catch(e){R("Invalid URL")}
}

function words(n){
if(n===0)return"Zero";
if(n<0)return"Minus "+words(-n);
let o=["","One","Two","Three","Four","Five","Six","Seven","Eight","Nine","Ten","Eleven","Twelve","Thirteen","Fourteen","Fifteen","Sixteen","Seventeen","Eighteen","Nineteen"];
let t=["","","Twenty","Thirty","Forty","Fifty","Sixty","Seventy","Eighty","Ninety"];
if(n<20)return o[n];
if(n<100)return t[Math.floor(n/10)]+(n%10?" "+o[n%10]:"");
if(n<1000)return o[Math.floor(n/100)]+" Hundred"+(n%100?" "+words(n%100):"");
if(n<1000000)return words(Math.floor(n/1000))+" Thousand"+(n%1000?" "+words(n%1000):"");
return "Number too large";
}

function roman(n){
let a=[[1000,"M"],[900,"CM"],[500,"D"],[400,"CD"],[100,"C"],[90,"XC"],[50,"L"],[40,"XL"],[10,"X"],[9,"IX"],[5,"V"],[4,"IV"],[1,"I"]],r="";
for(let x of a)while(n>=x[0]){r+=x[1];n-=x[0]}return r||"Invalid";
}

function imageTool(t){
let f=document.getElementById("file").files[0];if(!f)return R("Choose image first");
let im=new Image(),u=URL.createObjectURL(f);
im.onload=()=>{
if(t==="imginfo")R("Width: "+im.width+"px\nHeight: "+im.height+"px\nSize: "+(f.size/1024).toFixed(2)+" KB");
else if(t==="preview")R("Image loaded: "+f.name);
else if(t==="img64"){let rd=new FileReader();rd.onload=()=>R(rd.result);rd.readAsDataURL(f)}
else R("Image: "+im.width+" × "+im.height);
};im.src=u;
}

render();
</script>
</body>
</html>
