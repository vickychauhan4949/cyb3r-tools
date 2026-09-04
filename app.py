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
            # Ab hum direct cdn link nahi, apne server ka link denge
            return jsonify({"ok":True,"video_url":video_url,"title":info.get('title','Reel'),"thumbnail":info.get('thumbnail','')})
    except Exception as e:
        return jsonify({"ok":False,"error":str(e)}),500

# === NAYA ROUTE - YE GALLERY PROBLEM FIX KAREGA ===
@app.route('/download')
def download_video():
    cdn_url = request.args.get('url')
    if not cdn_url:
        return "No URL", 400
    
    # Insta se video fetch karke apne server se dega .mp4 naam ke saath
    try:
        r = requests.get(cdn_url, stream=True, timeout=20)
        filename = f"CYB3R_REEL_{datetime.now().strftime('%H%M%S')}.mp4"
        
        headers = {
            "Content-Disposition": f"attachment; filename={filename}",
            "Content-Type": "video/mp4"
        }
        return Response(r.iter_content(chunk_size=1024*1024), headers=headers, content_type="video/mp4")
    except Exception as e:
        return f"Error: {str(e)}", 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT",10000))
    app.run(host='0.0.0.0', port=port)
