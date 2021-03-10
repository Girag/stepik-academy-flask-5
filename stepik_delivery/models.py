from flask_sqlalchemy import SQLAlchemy
from flask_admin import AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask import redirect, session, request, url_for

db = SQLAlchemy()


class IndexView(AdminIndexView):
    def is_accessible(self):
        if session.get('role') == "admin":
            return True

    def inaccessible_callback(self, name, **kwargs):
        if session.get('role') == "customer":
            return redirect(url_for('account_view'))
        return redirect(url_for('login_view', next=request.url))

    def is_visible(self):
        return False


class AdminView(ModelView):
    def is_accessible(self):
        if session.get('role') == "admin":
            return True

    def inaccessible_callback(self, name, **kwargs):
        if session.get('role') == "customer":
            return redirect(url_for('account_view'))
        return redirect(url_for('login_view', next=request.url))


class OrderView(ModelView):
    def is_accessible(self):
        if session.get('role') == "admin":
            return True

    def inaccessible_callback(self, name, **kwargs):
        if session.get('role') == "customer":
            return redirect(url_for('account_view'))
        return redirect(url_for('login_view', next=request.url))

    can_set_page_size = True
    column_list = ['id', 'name', 'date', 'total', 'phone', 'status', 'mail', 'address', 'users_id', 'items']
    column_filters = ['id', 'name', 'date', 'total', 'phone', 'status', 'mail', 'address', 'users_id']
    column_sortable_list = ['id', 'name', 'date', 'total', 'phone', 'status', 'mail', 'address', 'users_id', 'items']
    column_searchable_list = ['id', 'name', 'date', 'total', 'phone', 'status', 'mail', 'address', 'users_id']


class CategoryView(ModelView):
    def is_accessible(self):
        if session.get('role') == "admin":
            return True

    def inaccessible_callback(self, name, **kwargs):
        if session.get('role') == "customer":
            return redirect(url_for('account_view'))
        return redirect(url_for('login_view', next=request.url))

    can_set_page_size = True
    column_list = ['id', 'title']
    column_filters = ['id', 'title']
    column_sortable_list = ['id', 'title']
    column_searchable_list = ['id', 'title']


class MealView(ModelView):
    def is_accessible(self):
        if session.get('role') == "admin":
            return True

    def inaccessible_callback(self, name, **kwargs):
        if session.get('role') == "customer":
            return redirect(url_for('account_view'))
        return redirect(url_for('login_view', next=request.url))

    can_set_page_size = True
    column_list = ['id', 'title', 'price', 'description', 'picture', 'category_id']
    column_filters = ['id', 'title', 'price', 'description', 'picture', 'category_id']
    column_sortable_list = ['id', 'title', 'price', 'description', 'picture', 'category_id']
    column_searchable_list = ['id', 'title', 'price', 'description', 'picture', 'category_id']


class UserView(ModelView):
    def is_accessible(self):
        if session.get('role') == "admin":
            return True

    def inaccessible_callback(self, name, **kwargs):
        if session.get('role') == "customer":
            return redirect(url_for('account_view'))
        return redirect(url_for('login_view', next=request.url))

    can_set_page_size = True
    column_list = ['id', 'mail', 'role']
    column_filters = ['id', 'mail', 'role']
    column_sortable_list = ['id', 'mail', 'role']
    column_searchable_list = ['id', 'mail', 'role']


meals_orders_association = db.Table('meals_orders', db.metadata,
                                    db.Column('order_id', db.Integer, db.ForeignKey('orders.id'), nullable=False),
                                    db.Column('meal_id', db.Integer, db.ForeignKey('meals.id'), nullable=False))


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    mail = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    role = db.Column(db.String, nullable=False)
    orders = db.relationship("Order", back_populates="users")


class Meal(db.Model):
    __tablename__ = "meals"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.String, nullable=False)
    picture = db.Column(db.String, nullable=False)
    category = db.relationship("Category", back_populates="meals")
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"))
    orders = db.relationship("Order", secondary=meals_orders_association, back_populates="items")


class Category(db.Model):
    __tablename__ = "categories"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    meals = db.relationship("Meal", back_populates="category")


class Order(db.Model):
    __tablename__ = "orders"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    date = db.Column(db.DateTime(timezone=False), default=db.func.now())
    total = db.Column(db.Float, nullable=False)
    status = db.Column(db.String, nullable=False)
    mail = db.Column(db.String, nullable=False)
    phone = db.Column(db.String, nullable=False)
    address = db.Column(db.String, nullable=False)
    users = db.relationship("User", back_populates="orders")
    users_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    items = db.relationship("Meal", secondary=meals_orders_association, back_populates="orders")
