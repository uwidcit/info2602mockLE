from flask_sqlalchemy import SQLAlchemy
import datetime
db = SQLAlchemy()

class Log(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    stdid = db.Column(db.String(10), nullable=False)
    stream = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime, default=datetime.datetime.now(), nullable=False)

    def toDict(self):
        return {
            'id': self.id,
            'stdid': self.stdid,
            'stream': self.stream,
            'date': self.date.strftime("%Y/%m/%d, %H:%M:%S")
        }