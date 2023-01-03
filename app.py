from flask import Flask, request, render_template, redirect, url_for, session
from flask_cors import CORS
import os
import analize
import recommendation_system
import librosa
import json

app = Flask(__name__)
CORS(app)


@app.route("/")
def home():
    return render_template("home.html")
    
@app.route("/upload")
def upload_page():
    return render_template("upload.html")

@app.route("/api/result", methods=['POST'])
def upload():
    if request.method != 'POST':
        redirect('/upload')
    
    
    file = request.files['upload_file']
    filepath = os.path.join(".", "tmp", file.filename)
    file.save(filepath)
    
    # 呼叫音高分析函式
    user_pitch = analize.five(filepath)
    # print(user_pitch)
    
    os.unlink(filepath)
    
    # 呼叫比對函式
    recommend = recommendation_system.recommendation(user_pitch)
    # print(recommend)
    
    result = []
    result.append(dict([('user_pitch', [librosa.midi_to_note(user_pitch[x]) for x in range(0, 5)])]))
    result.append(dict([('recommend', recommend)]))
    
    result = json.dumps(result)
    # print(result)
    
    return render_template("result.html")


if __name__ == "__main__":
    app.run(debug=True)

