from flask import Blueprint
import pandas as pd
from .models import PPD
from . import db
from datetime import date

utils = Blueprint('cli',__name__,cli_group='utils')


@utils.cli.command('import')
def import_csv():
    print("Fetching data from web, adding to database")
    # Read the CSV in chunks
    chunksize = 10000  # Number of rows per chunk
    counter = 0

    for chunk in pd.read_csv('http://prod.publicdata.landregistry.gov.uk.s3-website-eu-west-1.amazonaws.com/pp-complete.csv', chunksize=chunksize):

        chunk['date'] = pd.to_datetime(chunk['date']).dt.date
        filtered_chunk = chunk.loc[chunk['date'] >= date(2018,1,1)]

        for index, row in filtered_chunk.iterrows():
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
            if counter % 100 == 0:
                db.session.commit()

        print(f'Added {counter} records')
