from flask import Flask, render_template, request, redirect, session, url_for

app = Flask(__name__)
app.secret_key = 'your_secret_key'


def require_login(func):
    def wrapper(*args, **kwargs):
        if 'username' in session:
            # logged_in = True
            # username = session['username']
            return func(logged_in=True, username=session['username'], *args, **kwargs)
        else:
            # logged_in = False
            # username = None
            return redirect(url_for('login'))
    return wrapper



@app.route('/index')
@require_login
def home(logged_in, username):
    return render_template('index.html', logged_in=logged_in, username=username)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # 在這裡進行帳號密碼的驗證
        if username != 'abc' and password != '123':
            return render_template('login.html')
        # 如果驗證成功，將使用者名稱存入 session 中，示範程式碼如下
        session['username'] = username
        return redirect('/')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/login')

if __name__ == '__main__':
    app.run()




