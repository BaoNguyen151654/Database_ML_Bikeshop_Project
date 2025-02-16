from flask import Flask, render_template, request, jsonify
from flask_mysqldb import MySQL
from datetime import datetime

app = Flask(__name__)

# Cấu hình MySQL - điền thông tin kết nối của bạn
app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'giabao04052000'
app.config['MYSQL_DB'] = 'bike_shop'
app.config['MYSQL_PORT'] = 3306

mysql = MySQL(app)

@app.route('/')
def index():
    # Lấy danh sách sản phẩm
    cur = mysql.connection.cursor()
    cur.execute('''
        SELECT p.product_id, p.product_name, b.brand_name, 
               c.category_name, p.list_price, s.quantity
        FROM products p
        JOIN brands b ON p.brand_id = b.brand_id
        JOIN categories c ON p.category_id = c.category_id
        JOIN stocks s ON p.product_id = s.product_id
        WHERE s.store_id = 1
    ''')
    products = cur.fetchall()
    cur.close()
    return render_template('index.html', products=products)

@app.route('/buy', methods=['POST'])
def buy_product():
    data = request.json
    product_id = data.get('product_id')
    customer_id = 1  # Demo với customer_id cố định

    try:
        cur = mysql.connection.cursor()

        # Kiểm tra còn hàng không
        cur.execute("SELECT quantity FROM stocks WHERE product_id = %s AND store_id = 1", (product_id,))
        quantity = cur.fetchone()[0]

        if quantity <= 0:
            return jsonify({'error': 'Out of stock'})

        # Lấy giá sản phẩm
        cur.execute("SELECT list_price FROM products WHERE product_id = %s", (product_id,))
        price = cur.fetchone()[0]

        # Tạo order mới
        cur.execute('''
            INSERT INTO orders (customer_id, order_status, order_date, store_id, staff_id)
            VALUES (%s, 'Pending', %s, 1, 1)
        ''', (customer_id, datetime.now()))
        
        order_id = cur.lastrowid  # Lấy ID của đơn hàng vừa tạo

        # Tạo item_id tự động tăng (dựa trên số lượng các mục trong đơn hàng)
        cur.execute('''
            SELECT COALESCE(MAX(item_id), 0) + 1 FROM order_items WHERE order_id = %s
        ''', (order_id,))
        item_id = cur.fetchone()[0]

        # Thêm order item
        cur.execute('''
            INSERT INTO order_items (order_id, item_id, product_id, quantity, list_price, discount)
            VALUES (%s, %s, %s, 1, %s, 0)
        ''', (order_id, item_id, product_id, price))

        # Cập nhật số lượng trong kho
        cur.execute('''
            UPDATE stocks 
            SET quantity = quantity - 1
            WHERE store_id = 1 AND product_id = %s
        ''', (product_id,))

        mysql.connection.commit()
        return jsonify({'success': True, 'message': 'Order placed successfully!'})

    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
