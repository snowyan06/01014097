from flask import Flask, request, jsonify
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app, origins="*")  # 允许所有来源

# 模拟用户数据库
users = [
    {"id": 1, "username": "admin", "password": "admin", "nickname": "管理员", "role": "admin"},
    {"id": 2, "username": "teacher", "password": "teacher", "nickname": "教师", "role": "teacher"},
    {"id": 3, "username": "student", "password": "student", "nickname": "学生", "role": "student"}
]

# 模拟登录API
@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    role = data.get('role')
    
    # 查找用户
    user = next((u for u in users if u['username'] == username and u['password'] == password and u['role'] == role), None)
    
    if user:
        return jsonify({
            "id": user["id"],
            "username": user["username"],
            "nickname": user["nickname"],
            "role": user["role"],
            "token": "mock-token-" + username
        })
    else:
        return jsonify({"message": "用户名或密码错误"}), 401

# 模拟注册API
@app.route('/api/admin/users', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    nickname = data.get('nickname', username)
    role = data.get('role')
    
    # 检查用户名是否已存在
    if any(u['username'] == username for u in users):
        return jsonify({"message": "用户名已存在"}), 400
    
    # 创建新用户
    new_user = {
        "id": len(users) + 1,
        "username": username,
        "password": password,
        "nickname": nickname,
        "role": role
    }
    users.append(new_user)
    
    return jsonify(new_user)

# 模拟获取用户列表API
@app.route('/api/admin/users', methods=['GET'])
def get_users():
    return jsonify(users)

# 模拟获取单个用户信息API
@app.route('/api/admin/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = next((u for u in users if u['id'] == user_id), None)
    if user:
        return jsonify(user)
    else:
        return jsonify({"message": "用户不存在"}), 404

# 模拟获取客户数据API
@app.route('/api/customers', methods=['GET'])
def get_customers():
    return jsonify([
        {
            "id": 1000,
            "name": "James Butt",
            "country": {
                "name": "Algeria",
                "code": "dz"
            },
            "company": "Benton, John B Jr",
            "date": "2015-09-13",
            "status": "unqualified",
            "verified": True,
            "activity": 17,
            "representative": {
                "name": "Ioni Bowcher",
                "image": "ionibowcher.png"
            },
            "balance": 70663
        },
        {
            "id": 1001,
            "name": "Josephine Darakjy",
            "country": {
                "name": "Egypt",
                "code": "eg"
            },
            "company": "Chanay, Jeffrey A Esq",
            "date": "2019-02-09",
            "status": "negotiation",
            "verified": True,
            "activity": 0,
            "representative": {
                "name": "Amy Elsner",
                "image": "amyelsner.png"
            },
            "balance": 82429
        }
    ])

if __name__ == '__main__':
    app.run(port=8080, debug=True)