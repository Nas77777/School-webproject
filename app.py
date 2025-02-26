from operator import is_
from flask import Flask, request, render_template, redirect, url_for, flash, session, jsonify, send_from_directory
from werkzeug.security import generate_password_hash
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_migrate import Migrate
from sqlalchemy.sql import func, or_
import bcrypt
from flask_login import current_user, login_user, UserMixin, LoginManager, login_required
from datetime import date, datetime, timedelta
import os
import logging
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, TextAreaField, DateField, TimeField, BooleanField
from wtforms.validators import DataRequired, Email, Length, EqualTo
from flask_admin.form import ImageUploadField



app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(__file__), 'static/uploads')
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SECURE'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Verdant_Database.db' 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'
app.permanent_session_lifetime = timedelta(days=1)



logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'
admin = Admin(app)

# User Table
class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone = db.Column(db.String(15), unique=True, nullable=False)
    password_hash = db.Column(db.Text, nullable=False)
    role = db.Column(db.String(20), nullable=False, default="customer")
    reservations = db.relationship("Reservation", back_populates="user")

# Reservation Table
class Reservation(db.Model):
    __tablename__ = "reservations"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    availability_id = db.Column(db.Integer, db.ForeignKey("availabilities.id"), nullable=False)
    number_of_guests = db.Column(db.Integer, nullable=False)
    special_requests = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(20), nullable=False, default="pending")
    created_at = db.Column(db.DateTime, nullable=False, default=func.now())
    user = db.relationship("User", back_populates="reservations")
    availability = db.relationship("Availability", back_populates="reservations")
    menu_items = db.relationship("MenuItem", secondary='reservation_menu_items', back_populates="reservations")

    reservation_menu_items = db.Table('reservation_menu_items',
    db.Column('reservation_id', db.Integer, db.ForeignKey('reservations.id'), primary_key=True), 
    db.Column('menu_item_id', db.Integer, db.ForeignKey('menu_items.id'), primary_key=True)
)
    
# Menu Items Table
class MenuItem(db.Model):
    __tablename__ = "menu_items"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    image_url = db.Column(db.String(100), nullable=True)
    is_featured = db.Column(db.Boolean, default=False)
    tag1 = db.Column(db.String(50), nullable=True) 
    tag2 = db.Column(db.String(50), nullable=True) 
    tag3 = db.Column(db.String(50), nullable=True) 
    reservations = db.relationship("Reservation", secondary='reservation_menu_items', back_populates="menu_items") 


# Availability Table
class Availability(db.Model):
    __tablename__ = "availabilities"
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    is_available = db.Column(db.Boolean, default=True, nullable=False)
    reservations = db.relationship("Reservation", back_populates="availability")
    
    @property
    def formatted_start_time(self):
        """Return the start time in 12-hour format with AM/PM."""
        return self.start_time.strftime("%I:%M %p").lstrip("0")

    @property
    def formatted_end_time(self):
        """Return the end time in 12-hour format with AM/PM."""
        return self.end_time.strftime("%I:%M %p").lstrip("0")
   
# Events Table
class Events(db.Model):
    __tablename__ = "events"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    date = db.Column(db.Date, nullable=False)
    month = db.Column(db.String(3), nullable=False)
    Start_time = db.Column(db.Time, nullable=False)
    finish_time = db.Column(db.Time, nullable=False)
    ticket = db.Column(db.String(100), nullable=False)
    
# Newsletter Signup Table
class NewsletterSignup(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email_address = db.Column(db.String(120), unique=True, nullable=False)
    signup_date = db.Column(db.DateTime, default=datetime.utcnow)

@login.user_loader
def load_user(user_id):
    print("Loading user with ID:", user_id) 
    return User.query.get(int(user_id))


class AvailabilityView(ModelView):
    column_formatters = {
        'start_time': lambda v, c, m, p: m.formatted_start_time,
        'end_time': lambda v, c, m, p: m.formatted_end_time,
    }
class AdminMixin:
    def is_accessible(self):
        return current_user.is_authenticated and current_user.role == 'admin'

class MyModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.role == 'admin'

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login'))

    def on_model_change(self, form, model, is_created):
        if is_created and hasattr(model, 'creator_id'):
            model.creator_id = current_user.id
        return super(MyModelView, self).on_model_change(form, model, is_created)

class AvailabilityView(AdminMixin, ModelView):
    column_formatters = {
        'start_time': lambda v, c, m, p: m.formatted_start_time,
        'end_time': lambda v, c, m, p: m.formatted_end_time,
    }

class ProductAdminView(MyModelView):
    form_extra_fields = {
        'image_url': ImageUploadField('Image', base_path=app.config['UPLOAD_FOLDER'], allowed_extensions=app.config['ALLOWED_EXTENSIONS'])
    }

admin.add_view(AvailabilityView(Availability, db.session))
admin.add_view(ProductAdminView(MenuItem, db.session))
admin.add_view(MyModelView(User, db.session))
admin.add_view(MyModelView(NewsletterSignup, db.session))
class UserAdminView(AdminMixin, ModelView):
    pass

class MenuItemAdminView(AdminMixin, ModelView):
    pass

class EventsAdminView(AdminMixin, ModelView):
    pass


admin.add_view(EventsAdminView(Events, db.session))

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route('/', methods=['GET', 'POST'])
@app.route('/home_page', methods=['GET', 'POST'])
def Futured_product():
    featured_products = MenuItem.query.filter_by(is_featured=1).all()
    regular_products = MenuItem.query.filter_by(is_featured=0).all()
    return render_template('main-page.html', featured_products=featured_products, regular_products=regular_products)





@app.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        user = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")
        phone = request.form.get("phone")

        if not user or not email or not password or not confirm_password:
            error = "All fields are required."
            return render_template("signup.html", error=error)

        if password != confirm_password:
            error = "Passwords do not match."
            return render_template("signup.html", error=error)

        
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        try:
            if User.query.filter((User.email == email)).first():
                error = "Email already exists. Please try another."
                return render_template("signup.html", error=error)

            new_user = User(email=email, password_hash=hashed_password, name=user, phone=phone)
            
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('login'))
        except Exception as e:
            db.session.rollback()
            error = "An error occurred while creating your account. Please try again."
            return render_template("signup.html", error=error)

    return render_template("signup.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()


        if bcrypt.checkpw(password.encode('utf-8'), user.password_hash):
            session['user_id'] = user.id
            login_user(user)
            flash("Logged in successfully!", "success")
            return redirect(url_for('Futured_product'))
        elif user is None:
                flash("Invalid email or password.", "danger")
                return render_template("login.html")
        else:
            flash("Invalid email or password.", "danger")
            return render_template("login.html")

    return render_template('login.html')




if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)


@app.route('/menu', methods=['GET', 'POST'])
def menu():
    products = MenuItem.query.all()

    return render_template("menu.html", products=products)


@app.route('/reservation', methods=['GET', 'POST'])
def reservation():
    user_id = session.get('user_id')
    if not user_id:
        flash("Please log in first.", "danger")
        return redirect(url_for('login'))
    
    start_time = None
    end_time = None
    availability_id = session.get('availability_id')

    if availability_id:
        availability = Availability.query.get(availability_id)
        if availability:
            start_time = availability.formatted_start_time
            end_time = availability.formatted_end_time
    
    return render_template('reservation.html',
        reservation_date=session.get('reservation_date'),
        start_time=start_time,
        end_time=end_time,
        number_of_guests=session.get('number_of_guests'),
        special_requests=session.get('special_requests'))


@app.route('/select_date', methods=['GET', 'POST'])
def select_date():
    user_id = session.get('user_id')
    if not user_id:
        flash("Please log in first.", "danger")
        return redirect(url_for('login'))
    reservation_date = request.form.get('reservation_date')
    availability_id = request.form.get('time_selection')

    if not reservation_date:
        flash("Please select a date.", "danger")
        return redirect(url_for('reservation'))
    
    
    session['availability_id'] = availability_id
    session['reservation_date'] = reservation_date
    return redirect(url_for('time_slot')) 


@app.route('/time_slot', methods=['GET', 'POST'])
def time_slot():
    if request.method == 'POST':
        availability_id = request.form.get('time_selection')
        if availability_id:
            session['availability_id'] = availability_id
            return redirect(url_for('reservation'))  
        else:
            flash("Please select a time slot.", "danger")
            return redirect(url_for('reservation'))
    
    
    reservation_date_str = session.get('reservation_date')
    if not reservation_date_str:
        flash("Please select a date first.", "danger")
        return redirect(url_for('reservation'))
    
    reservation_date = datetime.strptime(reservation_date_str, '%Y-%m-%d').date()
    available_slots = Availability.query.filter(
        Availability.date == reservation_date,
        Availability.is_available == True
    ).all()
    
    return render_template('reservation.html', available_slots=available_slots)


@app.route('/save_details', methods=['POST'])
def save_details():
    number_of_guests = request.form.get('number_of_guests')
    special_requests = request.form.get('special_requests')

    session['number_of_guests'] = number_of_guests
    session['special_requests'] = special_requests

    return redirect(url_for('confirm'))


@app.route('/confirm', methods=['GET', 'POST'])
def confirm():
    user_id = session.get('user_id')
    reservation_date = session.get('reservation_date')
    availability_id = session.get('availability_id') 
    number_of_guests = session.get('number_of_guests')
    special_requests = session.get('special_requests')

    if not user_id:
        flash("Please log in first.", "danger")
        return redirect(url_for('login'))
    
    if not availability_id:
        flash("No time slot selected. Please start over.", "danger")
        return redirect(url_for('reservation'))
    

    availability = Availability.query.get(availability_id)
    if not availability:
        flash("Invalid time slot. Please start over.", "danger")
        return redirect(url_for('reservation'))
    
    start_time = availability.formatted_start_time
    end_time = availability.formatted_end_time

    if request.method == 'POST':
        reservation_submission = Reservation(
            user_id=user_id, 
            availability_id=availability_id, 
            number_of_guests=number_of_guests, 
            special_requests=special_requests
        )
        db.session.add(reservation_submission)
        db.session.commit()
        flash("Reservation confirmed!", "success")
    
    return render_template('reservation.html',
        reservation_date=reservation_date,
        start_time=start_time,
        end_time=end_time,
        number_of_guests=number_of_guests, 
        special_requests=special_requests)

@app.route('/events', methods=['GET', 'POST'])
def events():
    events = Events.query.all()

    return render_template('events.html', events=events)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

icon_dictionary = {
    "appetizers": '<i class="fas fa-leaf"></i>',
    "soups": '<i class="fas fa-utensils"></i>',
    "salads": '<i class="fas fa-seedling"></i>', 
    "main": '<i class="fas fa-star"></i>',
    "desserts": '<i class="fas fa-ice-cream"></i>',
    "beverages": '<i class="fas fa-glass-martini-alt"></i>'
}

@app.route('/staff/reservation', methods=['GET', 'POST'])
@login_required
def staff_reservation():
    if current_user.role != 'admin':
        flash("You do not have permission to access this page.", "danger")
        return redirect(url_for('home_page'))
    
    reservations = []
    selected_date = None  
    if request.method == 'POST':
        select_date_str = request.form.get('selected_date')
        if select_date_str:
            selected_date = datetime.strptime(select_date_str, '%Y-%m-%d').date()

            
            reservations = Reservation.query.join(Availability).filter(
                Availability.date == selected_date
            ).all()

            
            reservations_details = []
            for reservation in reservations:
                user = User.query.get(reservation.user_id)  
                reservations_details.append({
                    "id": reservation.id,
                    "user_name": user.name if user else "N/A",
                    "number_of_guests": reservation.number_of_guests,
                    "special_requests": reservation.special_requests,
                    "start_time": reservation.availability.formatted_start_time,
                    "end_time": reservation.availability.formatted_end_time,
                    "status": reservation.status,
                })

            reservations = reservations_details  

    return render_template('staff_reservations.html', reservations=reservations, selected_date=selected_date)

@app.route('/contact_us', methods=['GET', 'POST'])
def contact():
    return render_template('contact-page.html')

@app.route('/about_us', methods=['GET', 'POST'])
def about():
    return render_template('about.html')

@app.route('/refrences', methods=['GET', 'POST'])
def refrences():

    return render_template('Refrence.HTML')


@app.route('/home', methods=['GET', 'POST'])
def home():

    return render_template('main-page.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=False)