from flask import Flask, request, render_template, redirect, url_for, session
from flask_cors import CORS
import os
import analize


app = Flask(__name__)
CORS(app)


@app.route("/")
def home():
    return render_template("home.html")
    
@app.route("/upload")
def upload_page():
    return render_template("upload.html")

@app.route("/result", methods=['POST'])
def upload():
    if request.method != 'POST':
        redirect('/upload')
    
    
    file = request.files['upload_file']
    filepath = os.path.join(".", "tmp", file.filename)
    file.save(filepath)
    
    # 呼叫音高分析函式
    result = analize.five(filepath)
    print(result)
    
    # 呼叫比對函式
    
    os.unlink(filepath)
    
    return render_template("result.html")


if __name__ == "__main__":
    app.run(debug=True)

