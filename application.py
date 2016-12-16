'''
Flask application to manipulate images
Deployed on Amazon Web Services EC2

Initial fork from Flask Tutorial by:
Author: Scott Rodkey - rodkeyscott@gmail.com
https://medium.com/@rodkey/deploying-a-flask-application-on-aws-a72daba6bb80
'''

# flask imports
from flask import Flask, render_template, request, jsonify
from flask_restful import reqparse, abort, Api, Resource, marshal_with, fields

# application imports
from application import db
from application.models import Data, Image
from application.forms import EnterDBInfo, RetrieveDBInfo

# declaration of fields -- used by marshal_with (for json serialization)
image_fields = {
    'id': fields.Integer,
    'filename': fields.String,
    'filetype': fields.String,
    'height': fields.Integer,
    'width': fields.Integer
}

# image fields

# application initalization
application = Flask(__name__)
application.debug=True
# change this to your own value
application.secret_key = 'GDxTkzGIWeDekQYm42Lg'

# create an API for this application
api = Api(application)

# build user routes
@application.route('/', methods=['GET', 'POST'])
@application.route('/index', methods=['GET', 'POST'])
def index():
    form1 = EnterDBInfo(request.form) 
    form2 = RetrieveDBInfo(request.form) 
    
    if request.method == 'POST' and form1.validate():
        data_entered = Data(notes=form1.dbNotes.data)
        try:     
            db.session.add(data_entered)
            db.session.commit()        
            db.session.close()
        except:
            db.session.rollback()
        return render_template('thanks.html', notes=form1.dbNotes.data)
        
    if request.method == 'POST' and form2.validate():
        try:   
            num_return = int(form2.numRetrieve.data)
            query_db = Data.query.order_by(Data.id.desc()).limit(num_return)
            for q in query_db:
                print(q.notes)
            db.session.close()
        except:
            db.session.rollback()
        return render_template('results.html', results=query_db, num_return=num_return)                
    
    return render_template('index.html', form1=form1, form2=form2)


# API Resources
class ImageResource(Resource):
    @marshal_with(image_fields)
    def get(self, image_id):
        image = db.session.query(Image).filter(Image.id == image_id).first()
        if not image:
            abort(404, message = "Image {} does not exist".format(image_id))
        return image

class ImageListResource(Resource):
    @marshal_with(image_fields)
    def get(self):
        # images = db.session.query(Image).all()
        images = Image.query.all()
        return images

    @marshal_with(image_fields)
    def post(self):
        image = Image('sample.jpg', 'jpg', 100, 100)
        db.session.add(image)
        db.session.commit()        
        return image, 201

# build api routes
api.add_resource(ImageListResource, '/v1/image')
api.add_resource(ImageResource, '/v1/image/<image_id>')

if __name__ == '__main__':
    application.run(host='0.0.0.0')

