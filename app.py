from flask import Flask, render_template, request, redirect, url_for, send_file
from routes.negapoji import negaposi
import os

app = Flask(__name__)


#デフォルトページ
@app.route('/')
def index():
    return render_template('index.html')



#ボタンを押して画像をstatic内に保存されるようにする
@app.route('/upload', methods=['POST'])
def upload():
    # ファイルがアップロードされたか確認
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
    return render_template('change.html')



#画像変換ようのエンドポイント
@app.route('/change/conv',  methods=['POST'])
def conv():
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
    return render_template('change.html', file_exists=file_exists, message=conv_message)
    


#変換画像ダウンロードようのエンドポイント
@app.route('/change/dwonload', methods=['POST'])
def dwonload():
    output_path = os.path.join('static', 'output.png')
    if os.path.exists(output_path):
        return send_file(output_path, as_attachment=True, download_name='output.png')
    else:
        return "変換された画像が見つかりません。", 404



if __name__ == '__main__':
    app.run(debug=True,port=8080)
