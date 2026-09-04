from flask import Flask, request, jsonify, send_from_directory, Response
import yt_dlp, os, requests
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def home():
    return send_from_directory('.', 'index.html')

@app.route('/<path:path>')
def static_files(path):
    if os.path.exists(path):
        return send_from_directory('.', path)
    return send_from_directory('.', 'index.html')

@app.route('/api/reel', methods=['POST'])
def reel():
    data = request.get_json()
    url = data.get('url','').strip()
    if not url:
        return jsonify({"ok":False,"error":"URL empty"}),400
    try:
        ydl_opts = {'quiet':True,'skip_download':True,'noplaylist':True,'nocheckcertificate':True}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            video_url = info.get('url')
            if not video_url:
                fmts = info.get('formats',[])
                if fmts:
                    video_url = sorted([f for f in fmts if f.get('url')], key=lambda x: x.get('height',0) or 0)[-1]['url']
            if not video_url:
                return jsonify({"ok":False,"error":"Could not extract video - Instagram blocked"}),500
            return jsonify({"ok":True,"video_url":video_url,"title":info.get('title','Reel'),"thumbnail":info.get('thumbnail','')})
    except Exception as e:
        return jsonify({"ok":False,"error":str(e)}),500

@app.route('/download')
def download_video():
    cdn_url = request.args.get('url')
    if not cdn_url:
        return "No URL", 400
    try:
        # Full browser headers taaki Insta block na kare
        headers_req = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Referer": "https://www.instagram.com/",
            "Origin": "https://www.instagram.com",
            "Accept": "*/*",
            "Accept-Language": "en-US,en;q=0.9",
        }
        r = requests.get(cdn_url, headers=headers_req, stream=True, timeout=60)
        if r.status_code != 200:
            return f"CDN Error {r.status_code}", 500
            
        filename = f"CYB3R_REEL_{datetime.now().strftime('%H%M%S')}.mp4"
        return Response(
            r.iter_content(chunk_size=8192),
            headers={
                "Content-Disposition": f"attachment; filename={filename}",
            },
            content_type="video/mp4"
        )
    except Exception as e:
        return f"Error: {str(e)}", 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT",10000))
    app.run(host='0.0.0.0', port=port)
