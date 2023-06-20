from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from classes.class_imports import *
from pony.flask import Pony

WIDTH, HEIGHT = letter
JOB_QTY_INDENT = 10
JOB_DESCRIPTION_INDENT = 40
JOB_UNIT_PRICE_INDENT = 300
JOB_LINE_PRICE_INDENT = 340
JOB_SPACING = 15
JOB_VERTICAL_START = HEIGHT - 30

set_sql_debug(False)  # Shows the SQL queries pony is running in the console.
db.bind(provider='sqlite', filename='octofarmJira_database.sqlite', create_db=True)  # Establish DB connection.
db.generate_mapping(create_tables=True)


def write_header(c):
    c.drawString(0, 782, "Header")


def write_jobs(c, print_jobs):
    vertical_cursor = JOB_VERTICAL_START
    for pj in print_jobs:
        quantity = 1
        c.drawString(JOB_QTY_INDENT, vertical_cursor, str(quantity))
        c.drawString(JOB_DESCRIPTION_INDENT, vertical_cursor, pj.job_name + " 3D Print Object")
        c.drawString(JOB_UNIT_PRICE_INDENT, vertical_cursor, str(pj.cost))
        c.drawString(JOB_LINE_PRICE_INDENT, vertical_cursor, str(pj.cost * quantity))
        vertical_cursor -= JOB_SPACING


def get_jobs(permission_code_id):
    print_jobs = []
    with db_session:
        query_result = PrintJob.select(permission_code=8)
        for p in query_result:
            print_jobs.append(p)
    return print_jobs


def canvas_setup():
    c = canvas.Canvas("hello.pdf", pagesize=letter)
    # width, height = letter
    return c


def create_invoice(permission_code_id):
    print_jobs = get_jobs(permission_code_id)
    c = canvas_setup()
    write_header(c)
    write_jobs(c, print_jobs)
    c.showPage()
    c.save()


create_invoice(8)
