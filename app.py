from flask import Flask, request, send_from_directory, redirect, send_file, session
from flask_cors import CORS
import os
import recommendation_system
import reference_pitch
import librosa
import json

app = Flask(__name__,static_folder="./dist/static")
CORS(app)


def root_dir():  # pragma: no cover
    return os.path.abspath(os.path.dirname(__file__))


@app.route("/")
@app.route("/about")
@app.route("/analysis")
@app.route("/analysis/mode")
@app.route("/analysis/upload")
@app.route("/analysis/result")
def home():
    print(os.path.join(root_dir(), "index.html"))
    return send_file(os.path.join(root_dir(), "./dist/index.html"))



@app.route("/static/<path:path>")
def static_folder(path):
    print(path)
    return send_from_directory("./dist/static/", path)

@app.route("/assets/<path:path>")
def assets_folder(path):
    return send_from_directory("./dist/assets/", path)

@app.route('/Cover/<path:path>')
def get_resource(path):  # pragma: no cover
    complete_path = os.path.join(root_dir()+"/cover/", path)
    return send_file(complete_path, mimetype='image/png')


@app.route("/api/result", methods=['POST'])
def upload():
    if request.method != 'POST':
        redirect('/upload')

    file = request.files['upload_file']
    filepath = os.path.join(".", "tmp", file.filename)
    file.save(filepath)

    # 呼叫音高分析函式
    user_pitch = reference_pitch.ref_pitch(filepath, fmin="C2", fmax="C6")
    # print(user_pitch)

    os.unlink(filepath)

    # 呼叫比對函式
    recommend = recommendation_system.recommendation(user_pitch)
    recommend_a8 = recommendation_system.recommendation(
        [user_pitch[x]+12 for x in range(0, 5)])
    recommend_m8 = recommendation_system.recommendation(
        [user_pitch[x]-12 for x in range(0, 5)])
    # print(recommend)

    result = dict()
    result['user_pitch_visualize'] = [
        librosa.midi_to_note(user_pitch[x]) for x in range(0, 5)]
    result['user_pitch'] = user_pitch
    result['recommends'] = []
    result['recommends'].append(recommend_m8)
    result['recommends'].append(recommend)
    result['recommends'].append(recommend_a8)

    result = json.dumps(result)
    return result


if __name__ == "__main__":
    app.run(debug=True)
