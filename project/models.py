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
    logs=db.relationship('Logs',backref='users')

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


class Logs(db.Model):
    __tablename__='logs'
    id=db.Column(db.Integer,primary_key=True)
    use_at=db.Column(db.DateTime(),unique=True)
    userID=db.Column(db.Integer,db.ForeignKey('users.id'),nullable=False)

    def __repr__(self):
        data={
            'id':self.id,
            'use_at':self.use_at,
            'userID':self.userID
        }
        return  json.dumps(data)


PeopleLinks=db.Table("peopleLinks",
                    db.Column('peoplesId',db.Integer,db.ForeignKey('peoples.id')),
                    db.Column('linksId',db.Integer,db.ForeignKey('links.id')),
                    db.Column('url',db.Text(300))
                    )
class Peoples(db.Model):
    __tablename__='peoples'
    id=db.Column(db.Integer,primary_key=True)
    fullname=db.Column(db.String(245),nullable=False)
    email=db.Column(db.Text(40))
    description=db.Column(db.Text(500))
    phone=db.Column(db.String(25))
    images=db.relationship('Images',backref='peoples',uselist=False)
    links=db.relationship('Links',secondary=PeopleLinks)

    def __repr__(self):
        data={
            'id':self.id,
            'fullname':self.fullname,
            'email':self.email,
            'description':self.description,
            'phone':self.phone
        }

        return json.dumps(data)




class Images(db.Model):
    __tablename__='images'
    id=db.Column(db.Integer,primary_key=True)
    imageName=db.Column(db.Text(40),nullable=False)
    peopleID=db.Column(db.Integer,db.ForeignKey('peoples.id'),nullable=False)

    def __repr__(self):
        data={
            'image':self.imageName
        }
        return json.dumps(data)


class Links(db.Model):
    __tablename__='links'
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.Text(300),nullable=True)

