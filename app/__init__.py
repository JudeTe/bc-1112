import json
from flask import Flask, render_template, request, redirect, session, url_for, jsonify
from app.route import hello_world, index
from backend import Blockchain


class User():
    id_counter = 0
    all_users = []
    def __init__(self, username, password, is_admin=False):
        self.id = User.id_counter
        self.is_admin = is_admin
        self.is_voted = False
        self.ganache_address = None
        self.username = username
        self.password = password
        User.all_users.append(self)
        User.id_counter += 1

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

def create_app():
    app = Flask(__name__, template_folder='../templates', static_folder='../static')
    app.secret_key = 'your_secret_key'
    app.add_url_rule('/', '/', hello_world)
    # app.add_url_rule('/index', 'index', index)

    user = User(username='abc', password='123', is_admin=True)
    user = User(username='test1', password='123')
    user = User(username='test2', password='123')

    def redirect_login():
        if 'user_id' in session:
            user_id = session['user_id']
            user = next((u for u in User.all_users if u.id == user_id), None)
            if user:
                logged_in = True
                is_admin = user.is_admin
            else:
                logged_in = False
                return redirect(url_for('login'))
        else:
            redirect(url_for('login'))
        return user

    @app.route('/index')
    # @require_login
    def home():
        if 'user_id' in session:
            user_id = session['user_id']
            user = next((u for u in User.all_users if u.id == user_id), None)
            if user:
                logged_in = True
                is_admin = user.is_admin
            else:
                logged_in = False
                # is_admin = False
                return redirect(url_for('login'))
        else:
            return redirect(url_for('login'))
        return render_template('index.html', logged_in=logged_in, user=user)
    # def home(logged_in, user):
    #     return render_template('index.html', logged_in=logged_in, username=user.username)

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            # 在這裡進行帳號密碼的驗證
            user = authenticate_user(username, password)
            if user:
                session['user_id'] = user.id
                return redirect('/index')
        if 'user_id' in session:
            user_id = session['user_id']
            user = next((u for u in User.all_users if u.id == user_id), None)
            if user:
                return redirect('/index')
        return render_template('login.html')

    @app.route('/donate/', methods=['GET'])
    def donate_page():
        user = redirect_login()
        print("Here")
        return render_template('donate.html', user=user, logged_in=True)

    @app.route('/logout')
    def logout():
        session.pop('user_id', None)
        return redirect('/login')

    def authenticate_user(username, password):
        # 在這裡進行帳號密碼的驗證
        # 示範程式碼，假設 username 和 password 都符合條件才認證成功
        user = next((u for u in User.all_users if u.username == username and u.password == password), None)
        return user

    """
    Below is old main.py
    """

    # Initializing class here
    blockchain = Blockchain()

    # Registered Voters with unique Identity
    voterID_array=[
            'VOID001','VOID002','VOID003',
            'VOID004','VOID005','VOID006',
            'VOID007','VOID008','VOID009',
            'VOID010','VOID011','VOID012',
            'VOID013','VOID014','VOID015']
    # For Reference
    vote_see_chain=voterID_array.copy()
    vote_check=voterID_array.copy()
    minerID_array=[
        'MOID001','MOID002','MOID003']

    @app.route('/',methods=['GET','POST'])
    def start():
        # Miners Home Page
        if request.method=='POST':
            user=request.form["minerID"]
            if user in minerID_array and request.form['submit']=='mine':
                return redirect(url_for('mine'))
            if request.form['submit']=='vote':
                return redirect(url_for('initial'))
            if user in minerID_array and request.form['submit']=='vote':
                return '<h3>A miner with Miner ID cannot vote</h3>'
            else:
                return redirect(url_for("control",User="Miner",ID=user))
        else:
            return render_template('index.html')

    # For Better User Interface
    @app.route('/voter',methods=['POST','GET'])
    def initial():
        # Voters Home Page
        if request.method=='POST':
            user=request.form["voterID"]
            if user in vote_see_chain and request.form["submit"]=='see_chain':
                return redirect(url_for('full_chain'))
            if user in voterID_array and request.form["submit"]=='new_vote':
                return redirect(url_for("put_vote",name=user))
            else:
                return redirect(url_for("control",User="Voter",ID=user))
        else:
            return render_template('initial.html')


    @app.route('/<User>_repeat/<ID>/<error_msg>')
    def control(User, ID, error_msg=""):
        if not error_msg:
            error_msg = f"已投過票，或查無ID: {ID}"
        # CONTROL Reload and Back Reference After Vote
        return render_template("repeat_old.html",User=User, ID=ID, error_msg=error_msg)

    @app.route('/put_vote/<name>',methods=['POST','GET'])
    def put_vote(name):
        # POLL vote by Voter
        if request.method=='POST':
        # if request.method=='POST' and name in voterID_array:
            # voterID_array.remove(name)
            option=request.form['vote']
            return redirect(url_for("new_transaction",name=name, option=option))
        else:
            return render_template("fillup_old.html")

    # The process of Mining
    # This takes up the transactions done recently 
    # and put all into a block and append to the chain
    @app.route('/mine/', methods=['GET'])
    def mine():
        last_block = blockchain.last_block
        last_proof = last_block['proof']
        proof = blockchain.proof_of_work(last_proof)
        
        block = blockchain.new_block(proof)
        # block = blockchain.chain[0]
        # data = {
        #     'message': "New Block Mined",
        #     'index': block['index'],
        #     'transactions': block['transactions'],
        #     'proof': block['proof'],
        #     'previous_hash': block['previous_hash'],
        # }
        data = {'message': 'Mine succeed!'}
        response = app.response_class(
            response =json.dumps(data,indent=2),
            status = 200,
            mimetype = 'application/json'
        )
        return response

    # New Votes are done here
    @app.route('/vote/new/<name>/<option>', methods=['GET','POST'])
    def new_transaction(name,option):
        if request.method=="POST":
            """ values = request.get_json()
            # Check that the required fields are in the POST'ed data
            required = ['Party_A', 'Party_B'] """
            required=[name,option]

            # Part_A is the nominee participating in the elections
            # Party_B is the voter who votes
            if not all(k in values for k in required):
                return 'Missing values', 400

            # Create a new Transaction
            """ name=values['Party_B']
            option=values['Party_A'] """
        # if name not in vote_check:
        #     return redirect(url_for("control",User="Voter",ID=name))
        # else:
        #     vote_check.remove(name)

        index = blockchain.new_transaction(name, option)
        data = {'message': 'Transaction(The vote) will be added to Block 0'}
        # data = {
        #     'message': f'Transaction(The vote) will be added to Block {index}'}
        response = app.response_class(
            response = json.dumps(data,indent=2),
            status = 201,
            mimetype = 'application/json'
        )
        return response

    @app.route('/chain/<user_id>', methods=['GET'])
    def full_chain(user_id):
        user = next((u for u in User.all_users if u.id == int(user_id)), None)
        if user.is_admin == False:
            return redirect(url_for("control", User=user.username, ID=user_id, error_msg='權限不足！'))
        # Displays the whole block chain
        data = {
            'chain': blockchain.chain,
            'length': len(blockchain.chain),
            }
        response = app.response_class(
            response = json.dumps(data,indent=2),
            status = 200,
            mimetype = 'application/json'
        )
        return response
    
    for user in User.all_users:
        print(user.id, user.username)

    @app.route('/voting/<user_id>', methods=['POST'])
    def vote_in_html(user_id):
        user = next((u for u in User.all_users if u.id == int(user_id)), None)
        if user.is_voted:
            return redirect(url_for("control", User=user.username, ID=user_id, error_msg='不可重複投票!'))
        user.is_voted = True
        return redirect(url_for("put_vote", name=user.username))

    return app