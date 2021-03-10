from flask_admin import Admin

from stepik_delivery import app, db
from stepik_delivery.models import User, Meal, Category, Order
from stepik_delivery.models import IndexView, OrderView, CategoryView, MealView, UserView

admin = Admin(app, name="Stepik Delivery админка", template_mode="bootstrap4", index_view=IndexView(), endpoint="admin")

admin.add_view(OrderView(Order, db.session, name="Заказы", endpoint="orders"))
admin.add_view(CategoryView(Category, db.session, name="Категории", endpoint="categories"))
admin.add_view(MealView(Meal, db.session, name="Блюда", endpoint="meals"))
admin.add_view(UserView(User, db.session, name="Пользователи", endpoint="users"))
