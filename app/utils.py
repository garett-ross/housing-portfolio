from flask import Blueprint
import pandas as pd
from .models import PPD
from . import db
from datetime import date

utils = Blueprint('cli',__name__,cli_group='utils')


@utils.cli.command('import')
def import_csv():
    try:
        df = pd.read_csv('http://prod.publicdata.landregistry.gov.uk.s3-website-eu-west-1.amazonaws.com/pp-complete.csv').tail(10000)
        df['date'] = pd.to_datetime(df['date']).dt.date
        print("Fetched data from web, adding to database")
    except:
        df = pd.read_csv('all_ppd_from_df.csv')
        df['date'] = pd.to_datetime(df['date']).dt.date
        print("Fetched data local file, adding to database")

    counter = 0
    for index, row in df.iterrows():
        record = PPD(
            utr=row['utr'],
            price=row['price'],
            date=row['date'],
            postcode=row['postcode'],
            type=row['type'],
            old_new=row['old_new'],
            duration=row['duration'],
            paon=row['paon'],
            saon=row['saon'],
            street=row['street'],
            locality=row['locality'],
            town_city=row['town_city'],
            district=row['district'],
            county=row['county'],
            ppd_cat_type=row['ppd_cat_type'],
            record_status=row['record_status']
        )
        db.session.add(record)
        counter += 1
        print(f'Added {counter} records')
    db.session.commit()