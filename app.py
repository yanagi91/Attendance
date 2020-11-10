import os
from flask import Flask, render_template, request, url_for, redirect

import sebcam
from AZURE import identify
from DB import attendance_db as db


app = Flask(__name__)


@app.route('/')
def index():
    path = './static/images/myface.jpg'
    if os.path.exists(path):
        os.remove(path)
    return render_template('index.html')


@app.context_processor
def override_url_for():
    """staticの画像の更新用"""
    return dict(url_for=dated_url_for)


def dated_url_for(endpoint, **values):
    # 判定後の画像の保存を上書きしているためhtmlの画像を更新する処理
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path,
                                     endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)


@app.route('/identify/<taikin>', methods=(['GET', 'POST']))
def main(taikin=None):
    global result_name, rate
    img = '/Users/owner/Desktop/Attendance/static/images/myface.jpg'
    if not os.path.exists(img):
        sebcam.face_cap()
        result_name, rate = identify.start_identify_faces(img)
        rate = rate + '%'
        if result_name == None:
            result_name = ''
            rate = '検出できませんでした'
        else:
            db.add_attendance_db(result_name, rate, taikin)

    db_info = db.get_infomation_attendance()
    img = "images/myface.jpg"
    
    return render_template(
        'identify.html', taikin=taikin, img=img, result_name=result_name, rate=rate, db_info=db_info)


if __name__ == '__main__':
    app.run(debug=True)