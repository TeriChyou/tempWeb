from flask import Flask, render_template, request, redirect, session
import sqlite3
import logging

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['SESSION_TYPE'] = 'filesystem'

# 設定 logging
logging.basicConfig(filename='error.log', level=logging.ERROR)

DB_NAME = 'mydb.db'

def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    try:
        if 'userid' not in session:
            return redirect('/login')
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM member WHERE iid = ?', (session['userid'],)).fetchone()
        conn.close()
        return render_template('index.html', user=user)
    except Exception as e:
        logging.error("Error in index route: %s", str(e))
        return render_template('error.html', message=f'{e}')

@app.route('/login', methods=['GET', 'POST'])
def login():
    try:
        if request.method == 'POST':
            idno = request.form['idno']
            pwd = request.form['pwd']
            logging.info("Login attempt with ID: %s", idno)
            conn = get_db_connection()
            user = conn.execute('SELECT * FROM member WHERE idno = ? AND pwd = ?', (idno, pwd)).fetchone()
            conn.close()
            if user:
                session['userid'] = user['iid']
                return redirect('/')
            else:
                logging.warning("Login failed for ID: %s", idno)
                return render_template('login.html', error='請輸入正確的身分證字號和密碼')
        return render_template('login.html')
    except Exception as e:
        logging.error("Error in login route: %s", str(e))
        return render_template('error.html', message='發生了例外情形')

@app.route('/edit', methods=['GET', 'POST'])
def edit():
    try:
        if 'userid' not in session:
            return redirect('/login')
        if request.method == 'POST':
            # 假設我們允許使用者修改這些欄位
            nm = request.form['nm']
            birth = request.form['birth']
            blood = request.form['blood']
            phone = request.form['phone']
            email = request.form['email']
            idno = request.form['idno']
            pwd = request.form['pwd']
            conn = get_db_connection()
            conn.execute('''
                UPDATE member SET
                    nm = ?,
                    birth = ?,
                    blood = ?,
                    phone = ?,
                    email = ?,
                    idno = ?,
                    pwd = ?
                WHERE iid = ?
            ''', (nm, birth, blood, phone, email, idno, pwd, session['userid']))
            conn.commit()
            conn.close()
            return redirect('/')
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM member WHERE iid = ?', (session['userid'],)).fetchone()
        conn.close()
        return render_template('edit.html', user=user)
    except Exception as e:
        logging.error("Error in edit route: %s", str(e))
        return render_template('error.html', message='發生了例外情形')

@app.route('/logout')
def logout():
    session.pop('userid', None)
    return redirect('/')

if __name__ == '__main__':
    print(app.config)
    app.run(debug=True, host='0.0.0.0', port=80)
