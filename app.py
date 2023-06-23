from flask import Flask, request
from flask_restful import Resource, Api, marshal_with, fields
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

app.app_context().push()

# Modelling the data
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

    def __repr__(self):
        return self.name

# a fake database
fakeDatabase = {
    1:{'name':'Clean car'},
    2:{'name':'Write blog'},
    3:{'name':'Start stream'},
}

# Add a schema for the data to be serialized
taskFields = {
    "id": fields.Integer,
    "name": fields.String,
}

# Creating routes using class based views
# Access all items
class Items(Resource):
    @marshal_with(taskFields)
    def get(self):
        tasks = Task.query.all()
        return tasks
    
    @marshal_with(taskFields)
    def post(self):
        data = request.json
        task = Task(name=data["name"])
        db.session.add(task)
        db.session.commit()

        tasks = Task.query.all()
        # itemId = len(fakeDatabase.keys()) + 1
        # fakeDatabase[itemId] = {"name": data["name"]}
        return tasks

# Access a single item
class Item(Resource):
    @marshal_with(taskFields)
    def get(self, pk):
        task = Task.query.filter_by(id=pk).first()
        return task
    
    #Modify an item
    @marshal_with(taskFields)
    def put(self, pk):
        data = request.json
        task = Task.query.filter_by(id=pk).first()
        task.name = data["name"]
        db.session.commit()
        return task
        # fakeDatabase[pk]["name"] = data["name"]
        # return fakeDatabase
    
    # Delete an Item
    @marshal_with(taskFields)
    def delete(self, pk):
        task = Task.query.filter_by(id=pk).first()
        db.session.delete(task)
        db.session.commit()
        tasks = Task.query.all()
        return tasks
        # del fakeDatabase[pk]
        # return fakeDatabase

# Routes
api.add_resource(Items, '/')
api.add_resource(Item, '/<int:pk>')

if __name__ == "__main__":
    app.run(debug=True)