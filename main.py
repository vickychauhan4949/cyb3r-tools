from flask import Flask, send_from_directory, request, jsonify
import os, re
import yt_dlp

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.join(BASE_DIR, "cyb3r-tools")

def valid_insta_url(url):
    return re.match(r'^(https?:\/\/)?(www\.)?instagram\.com\/(reel|p)\/.*', url)

@app.route('/api/reel', methods=['POST'])
def reel_api():
    data = request.get_json() or {}
    url = data.get('url','').strip()
    if not url:
        return jsonify({"success": False, "error": "URL required"}), 400
    if not valid_insta_url(url):
        return jsonify({"success": False, "error": "Invalid Instagram URL"}), 400
    try:
        ydl_opts = {'quiet': True, 'skip_download': True}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            return jsonify({"success": True, "video_url": info.get('url'), "title": info.get('title')})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/health')
def health():
    return jsonify({"online": True})

# --- Main site ---
@app.route('/')
def home():
    return send_from_directory(ROOT_DIR, 'index.html')

@app.route('/free-fire-tools/')
def ff_home():
    return send_from_directory(os.path.join(ROOT_DIR, 'free-fire-tools'), 'index.html')

@app.route('/<path:path>')
def serve_all(path):
    # agar api nahi hai to file dhoondo
    if os.path.exists(os.path.join(ROOT_DIR, path)):
        return send_from_directory(ROOT_DIR, path)
    ff_path = os.path.join(ROOT_DIR, 'free-fire-tools', path.replace('free-fire-tools/',''))
    if os.path.exists(ff_path):
        return send_from_directory(os.path.join(ROOT_DIR, 'free-fire-tools'), path.replace('free-fire-tools/',''))
    return send_from_directory(ROOT_DIR, 'index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
