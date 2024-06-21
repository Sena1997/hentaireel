from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__)

# MySQLに接続
db = mysql.connector.connect(
    host="localhost",
    user="root",  # 確認したユーザー名
    password="ckyu676D0620!",  # rootユーザーのパスワード
    database="FanzaDB"
)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    keyword = request.form['keyword']
    cursor = db.cursor(dictionary=True)
    
    # SQLクエリを実行して検索結果を取得
    query = """
        SELECT * FROM Products 
        WHERE product_code LIKE %s OR performers LIKE %s OR label LIKE %s OR genres LIKE %s
    """
    cursor.execute(query, (f"%{keyword}%", f"%{keyword}%", f"%{keyword}%", f"%{keyword}%"))
    results = cursor.fetchall()
    cursor.close()
    
    return render_template('results.html', keyword=keyword, results=results)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port = 5001)

