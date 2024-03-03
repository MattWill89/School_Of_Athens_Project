# # routes.py
# from app import app, db, jwt
# from flask import jsonify, request
# from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
# from models import Book




# # Authentication routes
# @app.route('/login', methods=['POST'])
# def login():
#     username = request.json.get('username')
#     password = request.json.get('password')

#     # Your authentication logic goes here
#     # For simplicity, let's assume authentication always succeeds
#     access_token = create_access_token(identity=username)
#     return jsonify(access_token=access_token), 200

# # CRUD API routes
# @app.route('/books', methods=['GET'])
# def get_books():
#     books = Book.query.all()
#     return jsonify(books=[book.__dict__ for book in books]), 200

# @app.route('/books/<int:id>', methods=['GET'])
# def get_book(id):
#     book = Book.query.get(id)
#     if book:
#         return jsonify(book.__dict__), 200
#     else:
#         return jsonify(message='Book not found'), 404

# @app.route('/books', methods=['POST'])
# @jwt_required()
# def create_book():
#     data = request.json
#     book = Book(**data)
#     db.session.add(book)
#     db.session.commit()
#     return jsonify(message='Book created successfully'), 201

# @app.route('/books/<int:id>', methods=['PUT'])
# @jwt_required()
# def update_book(id):
#     data = request.json
#     book = Book.query.get(id)
#     if book:
#         for key, value in data.items():
#             setattr(book, key, value)
#         db.session.commit()
#         return jsonify(message='Book updated successfully'), 200
#     else:
#         return jsonify(message='Book not found'), 404

# @app.route('/books/<int:id>', methods=['DELETE'])
# @jwt_required()
# def delete_book(id):
#     book = Book.query.get(id)
#     if book:
#         db.session.delete(book)
#         db.session.commit()
#         return jsonify(message='Book deleted successfully'), 200
#     else:
#         return jsonify(message='Book not found'), 404

# # Example protected route
# @app.route('/protected', methods=['GET'])
# @jwt_required()
# def protected():
#     current_user = get_jwt_identity()
#     return jsonify(logged_in_as=current_user), 200



# !!!!!!!!!!!!!!!!This code is for getting directing use this code on the bottom first so that 
# I can test this out!!!!!!!!!!!!!!!!!! [line 80]


from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a secure random key in production

# Dummy user data for demonstration
users = {
    'user1': {'password': 'password1'},
    'user2': {'password': 'password2'}
}

@app.route('/')
def home():
    if 'username' in session:
        return redirect(url_for('index'))
    else:
        return render_template('home.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    # if request.method == 'POST':
    #     username = request.form['username']
    #     email = request.form['email']
    #     password = request.form['password']
    #     confirm_password = request.form['confirm_password']
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username]['password'] == password:
            session['username'] = username
            return redirect(url_for('home'))
        else:
            error = 'Invalid username or password. Please try again.'
            return render_template('login.html', error=error)
    return render_template('login.html')

# # Authentication routes
# @app.route('/login', methods=['POST'])
# def login():
#     username = request.json.get('username')
#     password = request.json.get('password')

#     # Your authentication logic goes here
#     # For simplicity, let's assume authentication always succeeds
#     access_token = create_access_token(identity=username)
#     return jsonify(access_token=access_token), 200

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/index')
def index():
    if 'username' in session:
        return render_template('index.html')
    else:
        return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)

