from flask import Flask, render_template, request, redirect, url_for
from flask_login import current_user, login_required, LoginManager, UserMixin, logout_user
from google.cloud import bigquery
import os


from waitress import serve

app = Flask(__name__, template_folder='templates')
app.secret_key = os.environ.get("SECRET_KEY") or os.urandom(24)

login_manager = LoginManager()
login_manager.init_app(app)

# 指定服務帳戶密鑰檔案的路徑
key_path = os.path.join(os.getcwd(), "credentials", "peterproject-364114-3539754c6db0.json")

# 設置環境變數
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = key_path

# 創建BigQuery客戶端
client = bigquery.Client(project='peterproject-364114')


class User(UserMixin):
    def __init__(self, username, email, password):
        self.id = username
        self.email = email
        self.password = password


@login_manager.user_loader
def load_user(username):
    # 在 BigQuery 中查找用户数据
    table_id = "peterproject-364114.userdata.Userdata"
    query = "SELECT * FROM {} WHERE username = '{}'".format(table_id, username)
    print(query)
    query_job = client.query(query)
    print(query_job)
    results = query_job.result()
    print(results)
    # 如果找到用户数据，就返回用户对象
    for row in results:
        print(row)
        return User(row['username'], row['email'], row['password'])

    # 如果未找到用户数据，就返回None
    return None


@app.route('/dashboard')
@login_required
def dashboard():
    return 'This is the dashboard page accessible only to logged in users'


# 首頁
@app.route('/')
def home():
    return render_template('base.html', current_user=current_user)


# 註冊頁面
@app.route('/register')
def register():
    return render_template('register.html')

if __name__ == '__main__':
    app.run(debug=True)

 # index
@app.route('/index')
@login_required
def index():
    # 從 BigQuery 中獲取帖子數據
    print("index")
    table_id = "peterproject-364114.postdata.Postdata"
    query = "SELECT * FROM {} ORDER BY timestamp DESC".format(table_id)
    query_job = client.query(query)
    results = query_job.result()

    posts = []
    for row in results:
        post = {'author': {'username': row['username']}, 'body': row['body']}
        posts.append(post)

    return render_template('index.html', title='Home', posts=posts)


# 登錄頁面
@app.route('/login', methods=['GET', 'POST'])
def login():
    print("login")
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        role = request.form.get('role')

        # 在 BigQuery 表中查詢用戶數據
        table_id = "peterproject-364114.userdata.Userdata"
        query = f"SELECT * FROM {table_id} WHERE username = @username AND password = @password"
        print(query)
        job_config = bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ScalarQueryParameter("username", "STRING", username),
                bigquery.ScalarQueryParameter("password", "STRING", password),
            ]
        )

        query_job = client.query(query, job_config=job_config)
        print(query_job)
        results = query_job.result()
        print(results)

        if(results.total_rows == 1):
            for row in query_job:
                print(row)
                role = row["role"]
        else:
            role = -1

        #print(results.row)
        #print(results.row.role)
        if role == "admin":
            return redirect(url_for('admin', username=username))
        elif role == "" or role is None:
            return redirect(url_for('user', username=username))
        else:
            return "Incorrect username or password"
    return render_template('login.html')


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

# 註冊提交
@app.route('/register', methods=['POST'])
def register_submit():
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')
    role = request.form.get('role')

    user_data = {
        'username': username,
        'email': email,
        'password': password
    }
    # 在这里使用 user_data 字典进行后续操作   
 # 将注册数据插入到 BigQuery 表中
    table_id = "peterproject-364114.userdata.Userdata"
    client = bigquery.Client()
    table = client.get_table(table_id)

    row = [(username, email, password , role)]
    errors = client.insert_rows(table, row)

    if errors == []:
        return redirect(url_for('login'))
    else:
        return "Error inserting row into BigQuery table: {}".format(errors)

    return '注册成功！'

# 登录提交
@app.route('/login_submit', methods=['POST'])
def login_submit():
    username = request.form.get('username')
    password = request.form.get('password')

# 在 BigQuery 表中查找普通用户
    user_table_id = "peterproject-364114.userdata.Userdata"
    user_query = f"SELECT * FROM {user_table_id} WHERE username = @username AND password = @password"
    user_job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("username", "STRING", username),
            bigquery.ScalarQueryParameter("password", "STRING", password),
        ]
    )
    user_query_job = client.query(user_query, job_config=user_job_config)
    user_results = user_query_job.result()

    # 如果找到普通用户，重定向到 user page
    if user_results.total_rows == 1:
        return redirect(url_for('user'))
    else:
    # 如果找不到用户，则返回错误消息
        return "Incorrect username or password"

# 管理頁面
@app.route('/admin')
def admin():
    # 從BigQuery表中獲取所有用戶數據
    table_id = "peterproject-364114.userdata.Userdata"
    query = "SELECT * FROM {}".format(table_id)
    query_job = client.query(query)
    results = query_job.result()

    return render_template('admin.html', results=results)
print('hello')
# @login_required
# 用戶主頁面
@app.route('/user/<username>')
def user(username):
    # 在 BigQuery 中查找用户数据
    print("user route")
    table_id = "peterproject-364114.userdata.Userdata"
    query = "SELECT * FROM {} WHERE username = '{}'".format(table_id, username)
    print(query)
    query_job = client.query(query)
    print(query_job)
    results = query_job.result()
    print(results)

    # 如果找到用户数据，就返回用户主页
    for row in results:
        print(row)
        return render_template('user.html', user=row)

    # 如果未找到用户数据，就返回404错误
    return "User not found", 404


# 個人資料編輯頁面
def get_current_user():
    pass


@app.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():
    user = get_current_user()  # 獲取當前用戶
