from flask import Flask, send_from_directory, jsonify, request
import os
import yt_dlp, re

app = Flask(__name__)

BASE = os.path.dirname(os.path.abspath(__file__))
POSSIBLE_ROOTS = [
    os.path.join(BASE, "cyb3r-tools"),
    os.path.join(BASE, "cyb3r-tools", "cyb3r-tools"),
    BASE
]

def find_root():
    for r in POSSIBLE_ROOTS:
        if os.path.exists(os.path.join(r, "index.html")):
            return r
    return POSSIBLE_ROOTS[0]

ROOT = find_root()
FF_DIR = None
for r in POSSIBLE_ROOTS:
    p = os.path.join(r, "free-fire-tools")
    if os.path.exists(p):
        FF_DIR = p
        break
    p2 = os.path.join(r, "cyb3r-tools", "free-fire-tools")
    if os.path.exists(p2):
        FF_DIR = p2
        break
if not FF_DIR:
    FF_DIR = os.path.join(ROOT, "free-fire-tools")

print("ROOT:", ROOT, os.listdir(ROOT))
print("FF_DIR:", FF_DIR, os.listdir(FF_DIR) if os.path.exists(FF_DIR) else "NOT FOUND")

@app.route('/api/health')
def health():
    return jsonify({"online": True})

@app.route('/')
def home():
    return send_from_directory(ROOT, 'index.html')

@app.route('/free-fire-tools/')
def ff_index():
    return send_from_directory(FF_DIR, 'index.html')

@app.route('/free-fire-tools/<path:path>')
def ff_files(path):
    return send_from_directory(FF_DIR, path)

@app.route('/<path:path>')
def all_files(path):
    # try root
    full = os.path.join(ROOT, path)
    if os.path.exists(full) and os.path.isfile(full):
        return send_from_directory(ROOT, path)
    # try ff
    full2 = os.path.join(FF_DIR, path)
    if os.path.exists(full2) and os.path.isfile(full2):
        return send_from_directory(FF_DIR, path)
    # fallback to index
    if path.startswith("api/"):
        return jsonify({"error":"not found"}), 404
    return send_from_directory(ROOT, 'index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
