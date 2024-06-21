import pandas as pd
import mysql.connector

# Excelファイルのパスを設定
file_path = '/Users/koichi/Downloads/Fanza_sample_updated_tags.xlsx'  # 実際のパスに置き換えてください
data = pd.read_excel(file_path)

# MySQLに接続
db = mysql.connector.connect(
    host="localhost",
    user="root",  # 確認したユーザー名
    password="ckyu676D0620!",  # rootユーザーのパスワード
    database="FanzaDB"
)
cursor = db.cursor()

# Productsテーブルにデータを挿入
for index, row in data.iterrows():
    cursor.execute("""
        INSERT INTO Products (product_code, performers, label, genres)
        VALUES (%s, %s, %s, %s)
    """, (row['Product Code'], row['Performers'], row['Label'], row['Genres']))
    product_id = cursor.lastrowid

    # TagsテーブルとProductTagsテーブルにデータを挿入
    for i in range(1, 15):  # Assuming there are up to 14 tags
        tag = row[f'Tag_{i}']
        if tag:
            cursor.execute("SELECT id FROM Tags WHERE tag = %s", (tag,))
            result = cursor.fetchone()
            if result:
                tag_id = result[0]
            else:
                cursor.execute("INSERT INTO Tags (tag) VALUES (%s)", (tag,))
                tag_id = cursor.lastrowid
            cursor.execute("INSERT INTO ProductTags (product_id, tag_id) VALUES (%s, %s)", (product_id, tag_id))

db.commit()
cursor.close()
db.close()

