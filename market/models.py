from market import db, login_manager
from market import bcrypt
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=30), nullable=False, unique=True)
    email_address = db.Column(db.String(length=50), nullable=False, unique=True)
    password_hash = db.Column(db.String(length=60), nullable=False)
    budget = db.Column(db.Integer(), nullable=False, default=1000)
    items = db.relationship('Item', backref='owned_user', lazy=True)

    @property
    def prettier_budget(self):
        if len(str(self.budget)) >= 4:
            return f'{str(self.budget)[:-3]},{str(self.budget)[-3:]}$'
        else:
            return f'{self.budget}$'

    @property
    def password(self):
        return self.password

    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)

    def __repr__(self):
        return f'User({self.username})'


class Item(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=30), nullable=False, unique=True)
    barcode = db.Column(db.String(length=12), nullable=False, unique=True)
    price = db.Column(db.Integer(), nullable=False)
    description = db.Column(db.String(length=1024), nullable=False, unique=True)
    owner = db.Column(db.Integer(), db.ForeignKey('user.id'))

    def __repr__(self):
        return f'Item({self.name})'


"""
    # db.session.rollback()
    
    from market import db
    from market.models import User, Item
    
    db.drop_all()
    db.create_all()
    
    u1 = User(username='jsc', password_hash='123234', email_address='jsc@jsc.com')
    db.session.add(u1)
    db.session.commit()
    User.query.all()
    
    item1 = Item(name='IPhone 10', price=500, barcode='851326497025', description='Description of apple iphone')
    item2 = Item(name='Apple Macbook Air', price=1199, barcode='851326497026', description='Description of apple macbook air')
    db.session.add(item1)
    db.session.add(item2)
    db.session.commit()
    Item.query.all()
    
    item1 = Item.query.filter_by(name='IPhone 10').first()
    item1.owner = User.query.filter_by(username='jsc').first().id
    db.session.add(item1)
    db.session.commit()
    Item.query.all()
    
    import os
    os.urandom(12).hex()
"""