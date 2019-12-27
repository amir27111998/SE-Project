from flask import json
from project import db
class Role(db.Model):
    __tablename__="roles"
    id=db.Column(db.Integer,primary_key=True)
    role=db.Column(db.String(10),nullable=False)
    users=db.relationship('User',backref='roles')

    def __repr__(self):
        return '{}'.format(self.role)


class User(db.Model):
    __tablename__="users"
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(20),nullable=False)
    password=db.Column(db.String(50),nullable=False)
    email=db.Column(db.Text(50),nullable=False)
    phone=db.Column(db.String(20),nullable=False)
    image=db.Column(db.Text(50),nullable=False)
    address=db.Column(db.Text(40),nullable=False)
    status=db.Column(db.Boolean(),nullable=False)
    role_id=db.Column(db.Integer,db.ForeignKey('roles.id'),nullable=False)

    def __repr__(self):
        data={
            'id':self.id,
            'name':self.name,
            'password':self.password,
            'email':self.email,
            'phone':self.phone,
            'image':self.image,
            'address':self.address,
            'status':self.status,
            'role_id':self.role_id
        }
        return json.dumps(data)