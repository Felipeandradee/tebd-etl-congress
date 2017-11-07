import datetime

import populate
from dw_models import db

print(f'Script started at: {datetime.datetime.now()}')
with db.atomic() as transaction:

    try:
        print(f'Populate year started at: {datetime.datetime.now()}')
        populate.year()
        db.commit()
        print(f'Populate year finished at: {datetime.datetime.now()}')

        print(f'Populate congress started at: {datetime.datetime.now()}')
        populate.congress()
        db.commit()
        print(f'Populate congress finished at: {datetime.datetime.now()}')

        print(f'Populate autor started at: {datetime.datetime.now()}')
        populate.autor()
        db.commit()
        print(f'Populate autor finished at: {datetime.datetime.now()}')

        print(f'Populate admissions started at: {datetime.datetime.now()}')
        populate.admissions()
        db.commit()
        print(f'Populate admissions finished at: {datetime.datetime.now()}')

    except Exception as e:
        db.rollback()
        print('Error: ', e)

print(f'Script finished at: {datetime.datetime.now()}')
