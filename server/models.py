from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators 
    @validates('name')
    def validate_name_length(self, key, value):
        if not value:
            raise ValueError("Name must be present")
        
        
                     
        existing_name= Author.query.filter(Author.name == value, Author.id != self.id).first()

        if existing_name:
            raise ValueError("Name has to be unique")
    
        
        return value
    
    @validates('phone_number')
    def validate_phone_length(self, key, value):
        
    # Check if phone number is provided
        if not value:
            raise ValueError("Phone number must be provided")
        
        if len(value) != 10:
            raise ValueError("Phone length must be 10 characters")
        
        if not value.isdigit():
            raise ValueError("Phone number must only contain digits")
        
        return value
    
  

    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'

class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators
    @validates('content')
    def validate_content(self, key, value):
        if len(value)<250:
            raise ValueError("Failed simple email validation")
        return value  
    
    @validates('summary')
    def validate_summary(self, key, value):
        if len(value)>250:
            raise ValueError("Failed simple email validation")
        return value
    
    @validates('title')
    def validate_title(self, key, value):
        if not value:
            raise ValueError("Title must be present")
        
        clickbait_phrases =  ["Won't Believe", "Secret", "Top", "Guess"]

        if not any(phrase in value for phrase in clickbait_phrases):
            raise ValueError("Title not sufficiently clickbait-y")
        
        return value
    
    @validates('category')
    def validate_category(self, key, value):
        if value not in ['Fiction', 'Non-Fiction']:
            raise ValueError("Category must be fiction or non-fiction")
        return value
   


    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'
