from flask import Flask, render_template, request, redirect, url_for, send_file
from routes.negapoji import negaposi
import os
from models import initialize_database, History
import base64
import datetime

app = Flask(__name__)
# データベースの初期化
initialize_database()

#デフォルトページ
@app.route('/')
def index():
    return render_template('index.html')



#ボタンを押して画像をstatic内に保存されるようにする
@app.route('/upload', methods=['POST'])
def upload():
    # ファイルがアップロードされたか確認(本当はアラートを出したいがjsを使わなければならないので、時間が余ったら実装する)
    if 'file' not in request.files:
        return 'ファイルが選択されていません。', 400
    
    file = request.files['file']
    if file.filename == '':
        return 'ファイルが選択されていません。', 400
    
    if file:
        filepath = os.path.join('static', 'img.png')
        file.save(filepath)
        return redirect(url_for('change'))



#change.htmlのエンドポイント
@app.route('/change')
def change():
    #Historyデータの抽出
    histories = History.select()
    return render_template('change.html', histories = histories)



#画像変換ようのエンドポイント
@app.route('/change/conv',  methods=['POST'])
def conv():
    #変換用モジュールのインスタンス化
    nega = negaposi()

    # `select` タグで選択された値を取得
    selected_value = request.form.get('selected_option')
    if selected_value=="":
        return '変換方法を選択してください', 400
    elif selected_value == "1":
        nega.negaposi_ms()
        conv_message = "画像の画像内の濃淡を入れ替える変換です。画像内の明るい画素を暗い画素に、暗い画素を明るい画素に変換する処理です。"

    #change.html内で変換された画像とメッセージが表示されるようにする
    output_path = os.path.join('static', 'output.png')
    file_exists = os.path.exists(output_path)

    #bace64を用いて画像データをエンコードする
    with open(output_path, "rb") as output_file:
        encord_img_data = base64.b64encode(output_file.read())

    #Historyデータベースにエンコードした画像データと変換日時を代入する
    History.create(
        times = datetime.datetime.now(),
        image_data = encord_img_data
    )

    #Historyデータの抽出
    histories = History.select()
    
    return render_template('change.html', file_exists=file_exists, message=conv_message, histories = histories)
    


#変換画像ダウンロードようのエンドポイント
@app.route('/change/download', methods=['POST'])
def download():
    output_path = os.path.join('static', 'output.png')
    if os.path.exists(output_path):
        return send_file(output_path, as_attachment=True, download_name='output.png')
    else:
        return "変換された画像が見つかりません。", 404



if __name__ == '__main__':
    app.run(debug=True,port=8080)
