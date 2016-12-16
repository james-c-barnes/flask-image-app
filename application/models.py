from application import db

class Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    notes = db.Column(db.String(128), index=True, unique=False)
    
    def __init__(self, notes):
        self.notes = notes

    def __repr__(self):
        return '<Data %r>' % self.notes

class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(128), index=True, unique=False)
    filetype = db.Column(db.String(128), index=False, unique=False)
    height = db.Column(db.Integer(), index=False, unique=False)
    width = db.Column(db.Integer(), index=False, unique=False)
    # created = db.Column(db.Date(), index=False, unique=False)
    # updated = db.Column(db.Date(), index=False, unique=False)

    def __init__(self, filename, filetype, height, width):
        self.filename = filename
        self.filetype = filetype
        self.height = height
        self.width = width
        # self.created =  datetime now here
        # self.updated =  datetime now here

    def __repr__(self):
        return '<Image %r>' % self.filename

