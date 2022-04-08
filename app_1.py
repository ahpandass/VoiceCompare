from flask import Flask, request, jsonify, make_response,render_template
from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import SQLAlchemySchema as ModelSchema
from marshmallow import fields
import os,json

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://admin:!QAZ1qaz@shandbinstance.c114frthmt6s.us-east-1.rds.amazonaws.com:3306/shan_dev'
db = SQLAlchemy(app)


class Authors(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    specialisation = db.Column(db.String(50))
    def create(self):
        db.session.add(self)
        db.session.commit()
        return self
    def __init__(self, name, specialisation):
        self.name = name
        self.specialisation = specialisation
    def __repr__(self):
        return '<Author %d>' % self.id


class AuthorsSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = Authors
        sqla_session = db.session
    id = fields.Number(dump_only=True)
    name = fields.String(required=True)
    specialisation = fields.String(required=True)


@app.route('/')
def index():
    return render_template('index.html')
    
@app.route('/upload',methods=['POST'])
def upload():
    file = request.files.get('file')
    filename = file.filename
    file.save(os.path.join(app.root_path, 'static',filename))
    return 'static/{}'.format(filename)

@app.route('/authors', methods=['GET'])
def get_authors():
    get_authors = Authors.query.all()
    author_schema = AuthorsSchema(many=True)
    authors = author_schema.dump(get_authors)
    return make_response(jsonify({"authors": authors}))


@app.route('/authors/<id>', methods=['GET'])
def get_author_by_id(id):
    get_author = Authors.query.get(id)
    author_schema = AuthorsSchema()
    author = author_schema.dump(get_author)
    return make_response(jsonify({"author": author}))


@app.route('/authors', methods=['POST'])
def create_author():
    data_dict={'name':request.values.get('name'),'specialisation':request.values.get('specialisation')}
    data = json.dumps(data_dict)
    #data = request.get_json()
    author_schema = AuthorsSchema()
    author = author_schema.loads(data)
    result = author_schema.dump(author.create())
    return make_response(jsonify({"author": result}), 200)


@app.route('/authors/<id>', methods=['PUT'])
def update_author_by_id(id):
    data = request.get_json()
    get_author = Authors.query.get(id)
    if data.get('specialisation'):
        get_author.specialisation = data['specialisation']
    if data.get('name'):
        get_author.name = data['name']

    db.session.add(get_author)
    db.session.commit()
    author_schema = AuthorsSchema(only=['id', 'name', 'specialisation'])
    author = author_schema.dump(get_author)
    return make_response(jsonify({"author": author}))


@app.route('/authors/<id>', methods=['DELETE'])
def delete_author_by_id(id):
    get_author = Authors.query.get(id)
    db.session.delete(get_author)
    db.session.commit()
    return make_response("", 204)


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)