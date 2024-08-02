from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# USER
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    subscription_date = db.Column(db.Date, nullable=False)

    favorites = db.relationship('Favorite', backref = 'user', lazy = True)
    # REFERENCIA A LA RELACION ENTRE LA TABLA USER Y FAVORITE

    def __repr__(self):
        return f'Email: {self.email} - ID: {self.id}' # ALTERNATIVA A ['<User %r>' % self.email] PARA COMPLEMENTAR EMAIL CON ID
            # '<User %r>' % self.email

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "last_name": self.last_name,
            "email": self.email,
            "subscription_date": self.subscription_date,
            # do not serialize the password, its a security breach
        }
    
    # MOSTRAR DATOS DEL USUARIO Y SU LISTA DE FAVORITOS DEL USUAIRO
    def get_user_favorite(self):
        return {
            "user": self.serialize(),
            "favorites": list(map(lambda item: item.serialize(), self.favorites))
            # LISTA DE USUARIOS SERIALIZADA
        }
    
# CHARACTERS
class Character(db.Model):
    # __tablename__ = 'character'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    birth_year = db.Column(db.String(250), nullable=False)
    gender = db.Column(db.String(250), nullable=False)
    height = db.Column(db.String(250), nullable=False)
    eye_color = db.Column(db.String(250), nullable=False)
    skin_color = db.Column(db.String(250), nullable=False)
    image = db.Column(db.String(500), nullable=False)


    favorite = db.relationship('Favorite', backref = 'character', lazy = True)

    def __repr__(self):
        return '<Character %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "birth_year": self.birth_year,
            "gender": self.gender,
            "height": self.height,
            "eye_color": self.eye_color,
            "skin_color": self.skin_color,
            "image": self.image
        }

# PLANETS
class Planet(db.Model):
    # __tablename__ = 'planet'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    climate = db.Column(db.String(250), nullable=False)
    population = db.Column(db.String(250), nullable=False)
    orbital_period = db.Column(db.String(250), nullable=False)
    rotation_period = db.Column(db.String(250), nullable=False)
    diameter = db.Column(db.String(250), nullable=False)
    image = db.Column(db.String(250), nullable=False)

    favorite = db.relationship('Favorite', backref = 'planet', lazy = True)

    def __repr__(self):
        return '<Planet %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "climate": self.climate,
            "population": self.population,
            "orbital_period": self.orbital_period,
            "rotation_period": self.rotation_period,
            "diameter": self.diameter,
            "image": self.image,
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
        # EVITAR MOSTRAR DATOS DE LOS CAMPOS VACIOS

    def serialize(self):
        character = Character.query.filter_by(id=self.character_id).first()
        planet = Planet.query.filter_by(id=self.planet_id).first()
        vehicle = Vehicle.query.filter_by(id=self.vehicle_id).first()

        print(character.serialize()["name"])
        if self.character_id:
            return {"character": self.character_id, "name": character.serialize()["name"] , "id": self.id, "user": self.user_id}
        elif self.planet_id:
            return {"planet": self.planet_id, "name": planet.serialize()["name"], "id": self.id, "user": self.user_id}
        elif self.vehicle_id:
            return {"vehicle": self.vehicle_id, "name": vehicle.serialize()["name"], "id": self.id, "user": self.user_id}
        else:
            return {"id": self.id, "user": self.user_id}
