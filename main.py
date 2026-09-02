from flask import Flask
import os
app = Flask(__name__)

@app.route('/')
def home():
    try:
        path = os.path.join(os.path.dirname(__file__), 'index.html')
        with open(path,'r',encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return f"Error: {e} - index.html not found"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
