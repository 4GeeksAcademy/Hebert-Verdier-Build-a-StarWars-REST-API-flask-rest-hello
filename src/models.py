from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# USER
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    last_name = db.Column(db.String(80), unique=False, nullable=False)
    email = db.Column(db.String(80), unique=False, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    subscription_date = db.Column(db.Date, unique=False, nullable=False)

    favorites = db.relationship('Favorite', backref = 'user', lazy = True)

    def __repr__(self):
        return f'Email: {self.email} - ID: {self.id}' # ALTERNATIVA A ['<User %r>' % self.email] PARA COMPLEMENTAR EMAIL CON ID
            # '<User %r>' % self.email

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "last_name": self.name,
            "email": self.email,
            "subscription_date": self.subscription_date,
            # do not serialize the password, its a security breach
        }
    
    def get_user_favorite(self):
        return {
            "user": self.serialize(),
            "favorites": list(map(lambda item: item.serialize(), self.favorites))
        }
    
# CHARACTERS
class Character(db.Model):
    # __tablename__ = 'character'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    gender = db.Column(db.String(250), nullable=False)
    eye_color = db.Column(db.String(250), nullable=False)

    favorite = db.relationship('Favorite', backref = 'character', lazy = True)

    def __repr__(self):
        return '<Character %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "gender": self.gender,
            "eye_color": self.eye_color,
        }

# PLANETS
class Planet(db.Model):
    # __tablename__ = 'planet'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    population = db.Column(db.String(250), nullable=False)
    diameter = db.Column(db.String(250), nullable=False)

    favorite = db.relationship('Favorite', backref = 'planet', lazy = True)

    def __repr__(self):
        return '<Planet %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "population": self.population,
            "diameter": self.diameter,
        }

# VEHICLES
class Vehicle(db.Model):
    # __tablename__ = 'vehicle'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    model = db.Column(db.String(250), nullable=False)
    size = db.Column(db.Integer, nullable=False)
    
    favorite = db.relationship('Favorite', backref = 'vehicle', lazy = True)

    def __repr__(self):
        return '<Vehicle %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "model": self.model,
            "size": self.size,
        }

# FAVORITES
class Favorite(db.Model):
    # __tablename__ = 'favorite'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    character_id = db.Column(db.Integer, db.ForeignKey('character.id'))
    planet_id = db.Column(db.Integer, db.ForeignKey('planet.id'))
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicle.id'))

    def __repr__(self):
        return '<Favorite %r>' % self.id
        # return f"User: {str(self.user_id)}{' - Character: ' + str(self.character_id) if self.character_id else ''}{' - Planet: ' + str(self.planet_id) if self.planet_id else ''}{' - Vehicle: ' + str(self.vehicle_id) if self.vehicle_id else ''}"


    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "character_id": self.character_id,
            "planet_id": self.planet_id,
            "vehicle_id": self.vehicle_id,
        }