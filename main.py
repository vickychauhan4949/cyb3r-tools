from flask import Flask, render_template, request, jsonify
import yt_dlp
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/reel', methods=['POST'])
def reel_api():
    data = request.get_json() or {}
    url = data.get('url','').strip()
    
    if not url or 'instagram.com' not in url:
        return jsonify({"ok": False, "error": "Invalid Instagram URL"}), 400

    if '/reel/' not in url and '/reels/' not in url:
        return jsonify({"ok": False, "error": "Please enter a Reel URL"}), 400

    ydl_opts = {
        'format': 'best',
        'quiet': True,
        'no_warnings': True,
        'noplaylist': True,
        'extractor_args': {'instagram': {'api_version': 'v1'}},
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            # Instagram gives multiple formats
            video_url = info.get('url')
            # If no direct url, try formats
            if not video_url and 'formats' in info:
                # best mp4
                formats = [f for f in info['formats'] if f.get('vcodec') != 'none']
                if formats:
                    video_url = formats[-1]['url']
            
            if not video_url:
                return jsonify({"ok": False, "error": "Could not extract video. Reel may be private."}), 400
                
            return jsonify({
                "ok": True,
                "video_url": video_url,
                "title": info.get('title','instagram_reel')[:50],
                "thumbnail": info.get('thumbnail')
            })
    except Exception as e:
        print(f"yt-dlp error: {e}")
        return jsonify({"ok": False, "error": f"Download failed: {str(e)[:100]}. Try again or use OPEN REEL."}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
