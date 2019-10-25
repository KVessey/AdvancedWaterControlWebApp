# tables.py

from flask_table import Table, Col

class Results(Table):
    id = Col('Id', show=False)
    name = Col('Plant Name')
    water_needed = Col('Water Needed')
    last_watered = Col('Last Watered')
    plant_type = Col('Plant Type')
