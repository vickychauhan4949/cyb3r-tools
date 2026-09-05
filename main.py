import os, yt_dlp
from flask import Flask, send_from_directory, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def find_ff():
    for r, d, f in os.walk(BASE_DIR):
        if "free-fire-tools" in d:
            p = os.path.join(r, "free-fire-tools")
            if os.path.exists(os.path.join(p, "index.html")):
                return p
    for r, d, f in os.walk(os.path.dirname(BASE_DIR)):
        if "free-fire-tools" in d:
            p = os.path.join(r, "free-fire-tools")
            if os.path.exists(os.path.join(p, "index.html")):
                return p
    return os.path.join(BASE_DIR, "free-fire-tools")

FREE = find_ff()
print("FREE FIRE DIR:", FREE)

@app.route('/')
def index():
    return send_from_directory(BASE_DIR, "index.html")

@app.route('/free-fire-tools')
@app.route('/free-fire-tools/')
def ff():
    return send_from_directory(FREE, "index.html")

@app.route('/free-fire-tools/<path:filename>')
def ff_files(filename):
    return send_from_directory(FREE, filename)

def valid_insta_url(v):
    try:
        from urllib.parse import urlparse
        u = urlparse(v)
        host = u.hostname in ["instagram.com", "www.instagram.com"]
        path = u.path.startswith("/reel/") or u.path.startswith("/reels/") or u.path.startswith("/p/")
        return host and path
    except:
        return False

@app.route('/api/reel', methods=['POST'])
def reel_api():
    data = request.get_json() or {}
    url = data.get('url','').strip()
    if not url:
        return jsonify({"success": False, "error": "Instagram Reel URL required"}), 400
    if not valid_insta_url(url):
        return jsonify({"success": False, "error": "Invalid Instagram Reel URL"}), 400
    
    # yt-dlp se real video nikalo
    try:
        ydl_opts = {'format': 'best', 'quiet': True, 'no_warnings': True, 'noplaylist': True}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            video_url = info.get('url')
            if not video_url and 'formats' in info:
                fmts = [f for f in info['formats'] if f.get('vcodec') != 'none']
                if fmts:
                    video_url = fmts[-1]['url']
        # server.js jaisa response + video_url bhi
        return jsonify({
            "success": True,
            "ok": True,
            "status": "URL verified",
            "message": "Reel URL valid hai.",
            "reelUrl": url,
            "video_url": video_url,
            "title": info.get('title','reel')
        })
    except Exception as e:
        return jsonify({"success": False, "ok": False, "error": str(e)[:200]}), 500

@app.route('/api/health')
def health():
    return jsonify({"online": True, "service": "HACKTOOLS PRO"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 10000)))
