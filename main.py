from flask import Flask, request, jsonify, send_from_directory
import yt_dlp
import os

app = Flask(__name__)

# Auto-find index.html location
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
POSSIBLE_PATHS = [
    os.path.join(BASE_DIR, "cyb3r-tools"),
    os.path.join(BASE_DIR, "templates"),
    BASE_DIR
]

def find_index():
    for p in POSSIBLE_PATHS:
        if os.path.exists(os.path.join(p, "index.html")):
            return p
    return BASE_DIR

TEMPLATE_DIR = find_index()

@app.route('/')
def index():
    return send_from_directory(TEMPLATE_DIR, "index.html")
@app.route('/free-fire-tools/')
def free_fire():
    return send_from_directory(os.path.join(TEMPLATE_DIR, "free-fire-tools"), "index.html")

@app.route('/free-fire-tools/<path:filename>')
def free_fire_files(filename):
    return send_from_directory(os.path.join(TEMPLATE_DIR, "free-fire-tools"), filename)
@app.route('/api/reel', methods=['POST'])
def reel_api():
    data = request.get_json() or {}
    url = data.get('url','').strip()
    if 'instagram.com' not in url:
        return jsonify({"ok": False, "error": "Invalid Instagram URL"}), 400
    ydl_opts = {'format': 'best','quiet': True,'no_warnings': True,'noplaylist': True}
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            video_url = info.get('url')
            if not video_url and 'formats' in info:
                fmts = [f for f in info['formats'] if f.get('vcodec') != 'none']
                if fmts:
                    video_url = fmts[-1]['url']
            if not video_url:
                return jsonify({"ok": False, "error": "Private reel / cannot extract"}), 400
            return jsonify({"ok": True, "video_url": video_url, "title": (info.get('title') or 'reel')[:50], "thumbnail": info.get('thumbnail')})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)[:200]}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 10000)))
