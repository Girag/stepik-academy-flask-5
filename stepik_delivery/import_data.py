import csv

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
from models import Meal, Category

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)

with open("data/delivery_categories.csv", "r", encoding="utf-8") as f:
    categories = csv.DictReader(f)
    for category in categories:
        cat = Category(id=int(category['id']), title=category['title'])
        db.session.add(cat)
db.session.commit()

with open("data/delivery_items.csv", "r", encoding="utf-8") as f:
    items = csv.DictReader(f)
    for item in items:
        meal = Meal(id=int(item['id']),
                    title=item['title'],
                    price=float(item['price']),
                    description=item['description'],
                    picture=item['picture'], category_id=int(item['category_id']))
        db.session.add(meal)
db.session.commit()
