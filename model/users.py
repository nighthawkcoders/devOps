""" database dependencies to support sqliteDB examples """
from random import randrange
from datetime import date
import os, base64
import json

from __init__ import app, db
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash

''' Tutorial: https://www.sqlalchemy.org/library.html#tutorials, try to get into Python shell and follow along '''

# Define the Post class to manage actions in 'posts' table,  with a relationship to 'users' table
# Define the User class to manage actions in the 'users' table
# -- Object Relational Mapping (ORM) is the key concept of SQLAlchemy
# -- a.) db.Model is like an inner layer of the onion in ORM
# -- b.) User represents data we want to store, something that is built on db.Model
# -- c.) SQLAlchemy ORM is layer on top of SQLAlchemy Core, then SQLAlchemy engine, SQL
class User(db.Model):
    __tablename__ = 'users'  # table name is plural, class name is singular

    # Define the User schema with "vars" from object
    id = db.Column(db.Integer, primary_key=True)
    _name = db.Column(db.String(255), unique=False, nullable=False)
    _uid = db.Column(db.String(255), unique=True, nullable=False)
    _password = db.Column(db.String(255), unique=False, nullable=False)
    _server_needed = db.Column(db.Boolean, default=False, nullable=False)
    _kasm_server = db.Column(db.String(255), default="N/A", server_default="N/A", nullable=False)
    _active_classes = db.Column(db.String(255), default="none", nullable=False)
    _archived_classes = db.Column(db.String(255), default="none", nullable=False)
    _latest_commmits = db.Column(db.Integer, default=0, server_default="0", nullable=False)

    # constructor of a User object, initializes the instance variables within object (self)
    def __init__(self, name, uid, password="123Qwerty!", server_needed=False, active_classes='', archived_classes=''):
        self._name = name    # variables with self prefix become part of the object, 
        self._uid = uid
        self.set_password(password)
        self._server_needed = server_needed
        self._active_classes = active_classes
        self._archived_classes = archived_classes

    @property
    def latest_commits(self):
        return self._latest_commmits
    
    @latest_commits.setter
    def latest_commits(self, latest_commits):
        self._latest_commmits = latest_commits

    # name getter methods, extracts name from object
    @property
    def name(self):
        return self._name
    
    @property
    def first_name(self):
        split_name = self._name.split()
        return split_name[0:-1] if len(split_name) > 1 else split_name[0]
        
    @property
    def last_name(self):
        full_name_parts = self._name.split()
        return full_name_parts[-1] if len(full_name_parts) > 1 else ""
        
    # a setter function, allows name to be updated after initial object creation
    @name.setter
    def name(self, name):
        self._name = name
    
    # a getter method, extracts email from object
    @property
    def uid(self):
        return self._uid
    
    # a setter function, allows name to be updated after initial object creation
    @uid.setter
    def uid(self, uid):
        self._uid = uid
        
    # check if uid parameter matches user id in object, return boolean
    def is_uid(self, uid):
        return self._uid == uid
    
    @property
    def password(self):
        return self._password[0:10] + "..." # because of security only show 1st characters

    # update password, this is conventional setter
    def set_password(self, password):
        """Create a hashed password."""
        self._password = generate_password_hash(password, method='sha256')

    # check password parameter versus stored/encrypted password
    def is_password(self, password):
        """Check against hashed password."""
        result = check_password_hash(self._password, password)
        return result
    
    # Getter method for _server_needed
    @property
    def server_needed(self):
        return self._server_needed
    
    # Setter method for _server_needed
    @server_needed.setter
    def server_needed(self, value):
        self._server_needed = value

    # Getter method for _kasm_server
    @property
    def kasm_server(self):
        return self._kasm_server

    # setter method for _kasm_server
    @kasm_server.setter
    def kasm_server(self, value):
        self._kasm_server = value

    # getter for _active_classes
    @property
    def active_classes(self):
        return self._active_classes
    
    # setter for _active_classes
    @active_classes.setter
    def active_classes(self, value):
        self._active_classes = value

    # getter for _archived_classes
    @property
    def archived_classes(self):
        return self._archived_classes
    
    # setter for _archived_classes
    @archived_classes.setter
    def archived_classes(self, value):
        self._archived_classes = value
        
    # output content using str(object) in human readable form, uses getter
    # output content using json dumps, this is ready for API response
    def __str__(self):
        return json.dumps(self.read())

    # CRUD create/add a new record to the table
    # returns self or None on error
    def create(self):
        try:
            # creates a person object from User(db.Model) class, passes initializers
            db.session.add(self)  # add prepares to persist person object to Users table
            db.session.commit()  # SqlAlchemy "unit of work pattern" requires a manual commit
            return self
        except IntegrityError:
            db.session.remove()
            return None

    # CRUD read converts self to dictionary
    # returns dictionary
    def read(self):
        return {
            "id": self.id,
            "name": self.name,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "uid": self.uid,
            "server_needed": self.server_needed,
            "kasm_server": self.kasm_server,
            "active_classes": self.active_classes,
            "archived_classes": self.archived_classes,
        }
        
    # CRUD read converts self to dictionary
    # returns dictionary
    def read_2025(self):
        server_needed = self.server_needed 
        if self.server_needed != "N/A":
            server_needed = False
            
        sections = []
        year = date.today().year
        # Concatenate active_classes and archived_classes with a comma and split, then iterate
        for section in (self.active_classes + "," + self.archived_classes).split(","):
            if section:  # Check if section is not empty
                if section.startswith("AP"):  # Check if section starts with "AP"
                    section = section[2:]  # Remove "AP" from the start
                sections.append({"abbreviation": section, "year": year})
                year -= 1
            
        
        return {
            "name": self.name,
            "uid": self.uid,
            "role": "User",
            "kasm_server_needed": self.server_needed,
            "sections": sections, 
        }

    # CRUD update: updates user name, password, phone
    # returns self
    def update(self, name="", uid="", password="", active_classes="", archived_classes=""):
        """only updates values with length"""
        if len(name) > 0:
            self.name = name
        if len(uid) > 0:
            self.uid = uid
        if len(password) > 0:
            self.set_password(password)
        if len(active_classes) > 0:
            self.active_classes = active_classes
        if len(archived_classes) > 0:
            self.archived_classes = archived_classes
        db.session.commit()
        return self

    # CRUD delete: remove self
    # None
    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return None


"""Database Creation and Testing """


# Builds working data for testing
def initUsers():
    with app.app_context():
        """Create database and tables"""
        db.create_all()
        """Tester data for table"""
        u1 = User(name='Thomas Edison', uid='vardaansinha', password='123toby', server_needed=True, active_classes="APCSP", archived_classes="")
        u2 = User(name='Nicholas Tesla', uid='safinsingh', password='123niko', active_classes="APCSA", archived_classes="APCSP")
        u3 = User(name='Alexander Graham Bell', uid='rjawesome')
        u4 = User(name='Grace Hopper', uid='hop', password='123hop', server_needed=True, active_classes="CSSE", archived_classes="")
        u5 = User(name='Pele', uid='king')

        users = [u1, u2, u3, u4, u5]

        """Builds sample user/note(s) data"""
        for user in users:
            try:
                user.create()
            except IntegrityError:
                '''fails with bad or duplicate data'''
                db.session.remove()
                print(f"Records exist, duplicate email, or error: {user.uid}")
