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
