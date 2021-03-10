import locale

from flask import render_template, abort, request, redirect, url_for, session
from sqlalchemy import func
from werkzeug.security import generate_password_hash, check_password_hash

from stepik_delivery import app, db
from stepik_delivery.models import User, Meal, Category, Order, meals_orders_association
from stepik_delivery.forms import RegisterForm, LoginForm, OrderForm
from stepik_delivery.admin import admin


@app.errorhandler(404)
def not_found_view(_):
    items = session.get('items', 0)
    total = session.get('total', 0)
    return render_template("404.html", items=items,
                           total=total), 404


@app.route("/")
def main_view():
    categories = db.session.query(Category).all()
    meals = {}
    for category in categories:
        meal = db.session.query(Meal).filter(Meal.category_id == category.id).order_by(func.random()).limit(3)
        meals[category.id] = meal
    items = session.get('items', 0)
    total = session.get('total', 0)
    return render_template("main.html", categories=categories,
                           meals=meals,
                           items=items,
                           total=total)


@app.route("/category/<int:id>/")
def category_view(id):
    category = db.session.query(Category).get_or_404(id)
    meals = dict()
    meals[id] = db.session.query(Meal).filter(Meal.category_id == id)
    items = session.get('items', 0)
    total = session.get('total', 0)
    return render_template("category.html", category=category,
                           meals=meals,
                           items=items,
                           total=total)


@app.route("/cart/", methods=["GET", "POST"])
def cart_view():
    cart = session.get('cart', {})
    items = session.get('items', 0)
    total = session.get('total', 0)
    meals = dict()
    for meal_id, amount in cart.items():
        meals[int(meal_id)] = db.session.query(Meal).filter(Meal.id == int(meal_id)).first()

    form = OrderForm()
    if not form.validate_on_submit():
        return render_template("cart.html", form=form,
                               cart=cart,
                               meals=meals,
                               items=items,
                               total=total)

    order = Order(name=form.name.data,
                  total=total,
                  status="Принят",
                  mail=form.mail.data,
                  phone=form.phone.data,
                  address=form.address.data,
                  users_id=session.get('user_id'))
    db.session.add(order)
    for i, meal in meals.items():
        for j in range(cart[str(i)]):
            order.items.append(meal)
    db.session.commit()
    return redirect(url_for("ordered_view"))


@app.route("/account/")
def account_view():
    if not session.get('is_auth'):
        error = "Для доступа необходимо войти в систему."
        form = LoginForm()
        return render_template("login.html", error=error,
                               form=form)
    user_id = session.get('user_id')
    items = session.get('items', 0)
    total = session.get('total', 0)
    orders = db.session.query(Order).filter(Order.users_id == user_id).order_by(Order.date.desc())
    meals = dict()
    for order in orders:
        all_items = []
        for item in order.items:
            meal_amount = list()
            meal_amount.append(item)
            meal_amount.append(db.session.query(func.count(meals_orders_association.c.meal_id))
                               .join(Order, Meal)
                               .filter(db.and_(Order.id == int(order.id), Meal.id == int(item.id))).scalar())
            all_items.append(meal_amount)
        meals[int(order.id)] = list(all_items)
    locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')
    return render_template("account.html", orders=orders,
                           meals=meals,
                           items=items,
                           total=total)


@app.route("/register/", methods=["GET", "POST"])
def register_view():
    first_reg = False
    if app.config['FIRST_REGISTRATION'] and not db.session.query(User).filter_by(id=1).first():
        first_reg = True

    form = RegisterForm()
    if not form.validate_on_submit():
        return render_template("register.html", form=form)

    user = db.session.query(User).filter_by(mail=form.mail.data).first()
    if user:
        error = "Пользователь с таким логином уже есть в системе. Попробуйте войти."
        return render_template("login.html", error=error, form=form)

    if first_reg:
        user = User(mail=form.mail.data,
                    password=generate_password_hash(form.password.data),
                    role="admin")
        app.config['FIRST_REGISTRATION'] = False
    else:
        user = User(mail=form.mail.data,
                    password=generate_password_hash(form.password.data),
                    role="customer")
    db.session.add(user)
    db.session.commit()
    session['user_id'] = user.id
    session['role'] = user.role
    session['is_auth'] = True
    if user.role == "admin":
        return redirect("/")
    return redirect("/cart/")


@app.route("/login/", methods=["GET", "POST"])
def login_view():
    error = ""
    form = LoginForm()

    if not form.validate_on_submit():
        return render_template("login.html", form=form,
                               error=error)

    user = db.session.query(User).filter_by(mail=form.mail.data).first()
    if user and check_password_hash(user.password, form.password.data):
        session['user_id'] = user.id
        session['role'] = user.role
        session['is_auth'] = True
        if session.get('cart'):
            return redirect("/cart/")
        if user.role == "admin":
            return redirect("/admin/")
        return redirect("/")
    else:
        error = "Неверная электропочта или пароль"
        return render_template("login.html", form=form,
                               error=error)


@app.route("/logout/")
def logout_view():
    if session.get("is_auth"):
        session.pop("is_auth")
        session.pop("user_id")
        session.pop("role")
    return redirect("/")


@app.route("/ordered/")
def ordered_view():
    cart = {}
    session['cart'] = cart
    items = 0
    session['items'] = items
    total = 0
    session['total'] = total
    return render_template("ordered.html")


@app.route("/addtocart/<int:id>/")
def addtocart_view(id):
    meal = db.session.query(Meal).get_or_404(id)
    cart = session.get('cart', {})
    cart[str(id)] = cart.get(str(id), 0) + 1
    session['cart'] = cart
    items = session.get('items', 0)
    session['items'] = items + 1
    total = session.get('total', 0)
    session['total'] = total + meal.price
    return redirect(request.referrer)


@app.route("/delfromcart/<int:id>/")
def delfromcart_view(id):
    meal = db.session.query(Meal).get_or_404(id)
    cart = session.get("cart", {})
    if not cart.get(str(id)):
        abort(404)
    elif cart.get(str(id)) and cart.get(str(id)) > 1:
        cart[str(id)] -= 1
    else:
        cart.pop(str(id))
    session['cart'] = cart
    items = session.get('items', 0)
    session['items'] = items - 1
    total = session.get('total', 0)
    session['total'] = total - meal.price
    session['meal_deleted'] = True
    return redirect('/cart/')
