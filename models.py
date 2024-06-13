from flask_sqlalchemy import SQLAlchemy # type: ignore
from flask_bcrypt import Bcrypt # type: ignore


db = SQLAlchemy()

bcrypt = Bcrypt()


def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)


class User(db.Model):

    __tablename__ = 'users'


    username = db.Column(db.String(20), unique = True, primary_key = True, nullable = False)

    password = db.Column(db.Text, nullable = False)

    first_name = db.Column(db.String(30), nullable = False)

    last_name = db.Column(db.String(30), nullable = False)

    email = db.Column(db.String(30), nullable = False)

    
    feedbacks = db.relationship("Feedback", backref='user', cascade="all, delete-orphan")    

    @property
    def full_name(self):
         return f"{self.first_name} {self.last_name}"
    


    @classmethod
    def register(cls, username, password, first_name, last_name, email):
        """Register user w/hased password & return user."""

        hashed = bcrypt.generate_password_hash(password)
        # turn bytestring into normal (unicode utf8) string
        hased_utf8 = hashed.decode("utf8")

        new_user = cls(
            username=username,
            password=hased_utf8,
            first_name=first_name,
            last_name=last_name,
            email=email
        )
        
        db.session.add(new_user)
        
        return new_user
    
    @classmethod
    def authenticate(cls, username, password):
        """Validate that user exists & password is correct"""

        user = User.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password, password):
            
            return user
        else: 
            return False
        


class Feedback(db.Model):

    __tablename__ = 'feedbacks'


    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    title = db.Column(db.String(100), nullable=False)

    content = db.Column(db.Text, nullable=False)

    username = db.Column(db.String(20), db.ForeignKey('users.username'))