from flask import Blueprint, render_template, request, redirect, url_for,session,current_app

web_bp = Blueprint('web', __name__)

@web_bp.route('/')
def index():
    return render_template('index.html')  # Show your homepage first

@web_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')


        db = current_app.db  # Get the database attached to app
        users_collection = db.users

        # Optional: Check if user already exists
        if users_collection.find_one({"email": email}):
            return "User already exists", 400

        users_collection.insert_one({
            "name": name,
            "email": email,
            "password": password
        })

        return redirect(url_for('web.login'))  # Redirect after signup

    return render_template('signup.html')

@web_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        role = request.form.get('role')  # 'admin' or 'customer'
        db = current_app.db

        try:
            if role == 'customer':
                email = request.form.get('email')
                password = request.form.get('password')
                user = db.users.find_one({"email": email})
                
                if user and user.get("password") == password:
                    session['user_id'] = str(user['_id'])
                    session['user_name'] = user.get('name')
                    session['role'] = 'customer'
                    return redirect(url_for('web.dashboard'))
                else:
                    return render_template('login.html', error="Invalid customer credentials")

            elif role == 'admin':
                employee_id = request.form.get('employee_id')
                password = request.form.get('password')
                admin = db.admin.find_one({"employee_id": employee_id})  # <- Separate collection

                if admin and admin.get("password") == password:
                    session['admin_id'] = str(admin['_id'])
                    session['admin_name'] = admin.get('name')
                    session['role'] = 'admin'
                    return redirect(url_for('web.dashboard'))
                else:
                    return render_template('login.html', error="Invalid admin credentials")

            else:
                return render_template('login.html', error="Unknown role selected")

        except Exception as e:
            print("Login error:", str(e))
            return f"Internal Server Error: {e}", 500

    return render_template('login.html')



@web_bp.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@web_bp.route('/prince')
def prince():
    return render_template('test.html')
