from reportlab.pdfgen import canvas
from classes.class_imports import *
from pony.flask import Pony

set_sql_debug(False)  # Shows the SQL queries pony is running in the console.
db.bind(provider='sqlite', filename='octofarmJira_database.sqlite', create_db=True)  # Establish DB connection.
db.generate_mapping(create_tables=True)

job = PrintJob.get(permission_code=8)


def hello(c):
    c.drawString(100, 100, "Hello World")


c = canvas.Canvas("hello.pdf")
hello(c)
c.showPage()
c.save()
