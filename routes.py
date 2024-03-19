# # routes.py
# from app import app, db, jwt
# from flask import jsonify, request
# from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
# from models import Book




# # Authentication routes
# @site.route('/login', methods=['POST'])
# def login():
#     username = request.json.get('username')
#     password = request.json.get('password')

#     # Your authentication logic goes here
#     # For simplicity, let's assume authentication always succeeds
#     access_token = create_access_token(identity=username)
#     return jsonify(access_token=access_token), 200

# # CRUD API routes
# @site.route('/books', methods=['GET'])
# def get_books():
#     books = Book.query.all()
#     return jsonify(books=[book.__dict__ for book in books]), 200

# @site.route('/books/<int:id>', methods=['GET'])
# def get_book(id):
#     book = Book.query.get(id)
#     if book:
#         return jsonify(book.__dict__), 200
#     else:
#         return jsonify(message='Book not found'), 404

# @site.route('/books', methods=['POST'])
# @jwt_required()
# def create_book():
#     data = request.json
#     book = Book(**data)
#     db.session.add(book)
#     db.session.commit()
#     return jsonify(message='Book created successfully'), 201

# @site.route('/books/<int:id>', methods=['PUT'])
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

# @site.route('/books/<int:id>', methods=['DELETE'])
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
# @site.route('/protected', methods=['GET'])
# @jwt_required()
# def protected():
#     current_user = get_jwt_identity()
#     return jsonify(logged_in_as=current_user), 200



# !!!!!!!!!!!!!!!!This code is for getting directing use this code on the bottom first so that 
# I can test this out!!!!!!!!!!!!!!!!!! [line 80]


from flask import Flask, render_template, request, redirect, url_for, session, Blueprint
from models import db, User, Book
from flask import  render_template

site = Blueprint('site', __name__, template_folder='templates')

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a secure random key in production

# Dummy user data for demonstration
# users = {
#    'user1': {'password': 'password1'},
#    'user2': {'password': 'password2'}
# }

# Helper Functions

def retrieve_all_users():
    users = User.query.all()
    return users

def handle_add_user(username, email, password, confirm_password):
    
    if password == confirm_password:
        
        # Use passed in form information to create an instance of the User class
        user = User(username=username, email=email, password=password)  
    
        # Add the "user" to the DB Session before committing these changes
        # to the DB
        db.session.add(user)
        db.session.commit()
        
        print("hello")

@site.route('/')
def home():
    if 'username' in session:
        return redirect('/index')
    else:
        return render_template('home.html')



@site.route('/signup', methods=['GET', 'POST'])
def signup():

    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        # With the values that were passed from the submitted "Sign Up"
        # form, we then want to pass these values on to a helper function
        # that will be responsible for passing that information to the DB
        handle_add_user(username, email, password, confirm_password)

    return render_template('signup.html')

@site.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            session['username'] = username
            return redirect('/index')
        else:
            error = 'Invalid username or password. Please try again.'
            return render_template('login.html', error=error)
    return render_template('login.html')


# # Authentication routes
# @site.route('/login', methods=['POST'])
# def login():
#     username = request.json.get('username')
#     password = request.json.get('password')

#     # Your authentication logic goes here
#     # For simplicity, let's assume authentication always succeeds
#     access_token = create_access_token(identity=username)
#     return jsonify(access_token=access_token), 200

@site.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/index')

@site.route('/index')
def index():
    if 'username' in session:
        return render_template('index.html')
    else:
        return redirect("/login")

if __name__ == '__main__':
    app.run(debug=True)

@site.route('/add_book', methods=['GET', 'POST'])
def add_a_book():

    if request.method == 'POST':
        isbn = request.form['isbn']
        author = request.form['author']
        title = request.form['title']
        length = request.form['length']
        if request.form['hardcover'] == 'true':
            hardcover = True
        else:
            hardcover = False

    book = Book(
        isbn = isbn,
        author = author,
        title = title,
        length = length,
        hardcover = hardcover
    )
    
    db.session.add(book)
    db.session.commit()
    return redirect('/manage_books')


@site.route('/manage_books', methods=['GET', 'POST'])
def manage_books():

    books = Book.query.order_by(Book.title).all()

    return render_template('manage_books.html', books=books)

@site.route('/edit_book/<book_id>', methods=['GET', 'POST'])
def edit_book(book_id):

    book = Book.query.filter_by(id=book_id).first()

    # If an "Edit Book" form is submitted, we update the found "book" instance
    # before committing these changes to the DB.
    if request.method == 'POST':
        book.isbn = request.form['isbn']
        book.author = request.form['author']
        book.title = request.form['title']
        book.length = request.form['length']
        if request.form['hardcover'] == 'true':
            book.hardcover = True
        else:
            book.hardcover = False
    
        # Commit the changes made to the "book" instance to the DB.
        db.session.commit()
        return redirect('/manage_books')
        
    return render_template('edit_book.html', book=book)

@site.route('/delete_book/<book_id>')
def delete_book(book_id):

    book = Book.query.filter_by(id=book_id).first()

    db.session.delete(book)
    db.session.commit()

    return redirect('/manage_books')

@site.route('/search_books', methods=['POST'])
def find_books():

    search = request.form['search']
    books = Book.query.filter(Book.title.contains(search)).all()

    return render_template('manage_books.html', books=books)