from flask import Flask, request, render_template, redirect, url_for, session
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route("/")
def home():
    return render_template("home.html")
    
@app.route("/upload")
def upload_page():
    return render_template("upload.html")

@app.route("/api/upload", methods=['POST'])
def upload():
    if request.method != 'POST':
        redirect('/upload')
    # 呼叫音高分析函式
    
    # 呼叫比對函式
    
    return render_template("result.html")


if __name__ == "__main__":
    app.run(debug=True)

