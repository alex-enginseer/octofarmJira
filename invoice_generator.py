from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from classes.class_imports import *
from pony.flask import Pony

WIDTH = letter[0]
HEIGHT = letter[1]
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


# Formats all the data from the print job into correct slots for the invoice
def write_jobs(c, print_jobs):
    vertical_cursor = JOB_VERTICAL_START
    for pj in print_jobs:
        quantity = 1
        c.drawString(JOB_QTY_INDENT, vertical_cursor, str(quantity))
        c.drawString(JOB_DESCRIPTION_INDENT, vertical_cursor, pj.job_name + " 3D Print Object")
        c.drawString(JOB_UNIT_PRICE_INDENT, vertical_cursor, str(pj.cost))
        c.drawString(JOB_LINE_PRICE_INDENT, vertical_cursor, str(pj.cost * quantity))
        vertical_cursor -= JOB_SPACING


# Creates our canvas and draws the invoice onto our .pdf from a .png version of the invoice
def canvas_setup():
    c = canvas.Canvas("hello.pdf", pagesize=letter)
    return c


def finalize_report(c):
    c.showPage()
    c.save()


# Entry function for invoice generator. The only function that should be accessed outside of this file
def create_invoice(permission_code_id):
    c = canvas_setup()
    write_header(c)
    print_jobs = PrintJob.Get_Jobs_For_Permission_Code(permission_code_id)
    write_jobs(c, print_jobs)
    finalize_report(c)


create_invoice(8)
