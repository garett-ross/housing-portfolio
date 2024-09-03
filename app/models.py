from datetime import datetime
from . import db  # Import the db instance from your application module
from dataclasses import dataclass

@dataclass
class PPD(db.Model):
    __tablename__ = 'ppd'

    utr = db.Column(db.String(100), primary_key=True)
    price = db.Column(db.Integer, nullable=False)
    date = db.Column(db.Date, nullable=False)
    postcode = db.Column(db.String(10), nullable=True)
    type = db.Column(db.String(100), nullable=True)
    old_new = db.Column(db.String(100), nullable=True)
    duration = db.Column(db.String(100), nullable=True)
    paon = db.Column(db.String(100), nullable=True)
    saon = db.Column(db.String(100), nullable=True)
    street = db.Column(db.String(100), nullable=True)
    locality = db.Column(db.String(100), nullable=True)
    town_city = db.Column(db.String(100), nullable=True)
    district = db.Column(db.String(100), nullable=True)
    county = db.Column(db.String(100), nullable=True)
    ppd_cat_type = db.Column(db.String(100), nullable=True)
    record_status = db.Column(db.String(100), nullable=True)

    def __repr__(self):
        return f'<PPD {self.utr}>'
    
    def to_dict(self):
        return {
            "utr": self.utr,
            "price": self.price,
            "date": self.date.isoformat() if self.date else None,
            "postcode": self.postcode,
            "type": self.type,
            "old_new": self.old_new,
            "duration": self.duration,
            "paon": self.paon,
            "saon": self.saon,
            "street": self.street,
            "locality": self.locality,
            "town_city": self.town_city,
            "district": self.district,
            "county": self.county,
            "ppd_cat_type": self.ppd_cat_type,
            "record_status": self.record_status
        }
