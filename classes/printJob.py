from classes.printer import *
import datetime


class PrintJob(db.Entity):
    printed_on = Optional(Printer)
    """Printer this job was processed on."""
    permission_code = Optional('PermissionCode')
    job_id = Required(int)
    """ID from the job submission system. We use Jira. This will be the unique ID generated by jira. Only digits in our case."""
    job_name = Optional(str)
    """Optional custom job name from the submission system. We use PR-#### formatted names."""
    downloaded_at_date = Optional(datetime.datetime)
    print_started_date = Optional(datetime.datetime)
    print_finished_date = Optional(datetime.datetime)
    payment_link_generated_date = Optional(datetime.datetime)
    paid_date = Optional(datetime.datetime)
    weight = Optional(float)
    cost = Optional(float)
    print_status = Required(str)
    """PrintStatus Enum"""
    payment_status = Required(str)
    """PaymentStatus Enum"""
