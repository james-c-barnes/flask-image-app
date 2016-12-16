'''
Flask application to manipulate images
Deployied on Amazon Web Services EC2

Initial fork from Flask Tutorial by:
Author: Scott Rodkey - rodkeyscott@gmail.com
Step-by-step tutorial: https://medium.com/@rodkey/deploying-a-flask-application-on-aws-a72daba6bb80
'''

from flask import Flask, render_template, request
from flask_restful import reqparse, abort, Api, Resource

from application import db
from application.models import Data
from application.forms import EnterDBInfo, RetrieveDBInfo

# application initalization
application = Flask(__name__)
application.debug=True
# change this to your own value
# application.secret_key = 'cC1YCIWOj9GgWspgNEo2'   

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


images_l = [
    {'id': 'key1', 'filename': 'image1', 'filetype': 'jpg', 'filesize': 1231},
    {'id': 'key2', 'filename': 'image2', 'filetype': 'gif', 'filesize': 1232},
    {'id': 'key3', 'filename': 'image3', 'filetype': 'svg', 'filesize': 1233},
]

def abort_if_image_doesnt_exist(image_id):
    if not any(d['id'] == image_id for d in images_l):
        abort(404, message="Image {} doesn't exist".format(image_id))

# API Resources
class ImageMetadata(Resource):
    def get(self, image_id):
        abort_if_image_doesnt_exist(image_id)
        for d in images_l:
            if d['id'] == image_id:
                return d
        return {}

class ImageMetadataList(Resource):
    def get(self):
        return images_l 

# build api routes
api.add_resource(ImageMetadataList, '/v1/image')
api.add_resource(ImageMetadata, '/v1/image/<image_id>')

if __name__ == '__main__':
    application.run(host='0.0.0.0')

