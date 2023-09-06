import yaml
import jira
from classes.printerModel import *
import os
from fpdf import FPDF 
from datetime import datetime

# importing configs
with open("config_files/config.yml", "r") as yamlFile:
    config = yaml.load(yamlFile, Loader=yaml.FullLoader)


@db_session
def start_queued_jobs():
    print("Checking for queued jobs...")
    queued_jobs = PrintJob.Get_All_By_Status(PrintStatus.IN_QUEUE)
    print(str(len(queued_jobs)) + " queued jobs found.")
    if len(queued_jobs) == 0:
        return

    jobs_started = 0  # Just used to track the number of jobs for logging.
    manual_jobs = 0
    printer_models = PrinterModel.Get_All()
    printers_by_count = Printer.Get_All_Printers_By_Count(True)
    for pm in printer_models:
        if pm.auto_start_prints:
            printers = list(filter(lambda p: p[0].printer_model.id == pm.id, printers_by_count))  # Get printers for this printer model
            jobs = list(filter(lambda j: j.printer_model.id == pm.id, queued_jobs))  # Get jobs for this printer model
            for printer in printers:
                # printer is a tuple: (printer, <print_count>)
                if len(jobs) == 0:  # We are out of jobs for this printer model
                    break
                printer_state = printer[0].Get_Printer_State()
                if printer_state[0:7] == 'offline':
                    print(printer[0].name + " : " + printer_state)
                    print("Printer is offline, attempting to reconnect automatically")
                    try:
                        printer[0].Connect_Printer()
                    except Exception as e:
                        print("Unable to connect to " + printer[0].name)
                        continue
                    time.sleep(5)
                    printer_state = printer[0].Get_Printer_State()
                    print(printer[0].name + " : " + printer_state)
                if printer_state == 'operational':
                    start_print_job(jobs.pop(0), printer[0])  # Removes the job from the list for this printer model
                    jobs_started += 1
        else:
            jobs = list(filter(lambda j: j.printer_model.id == pm.id, queued_jobs))  # Get jobs for this printer model
            manual_jobs += len(jobs)

    print(str(len(queued_jobs) - jobs_started - manual_jobs) + " auto start jobs still in queue.")
    print(str(manual_jobs) + " manual start jobs still in queue.")


@db_session
def find_open_printer(model):
    """Will return an available printer with the fewest total print jobs or None if one is not available."""
    printers = Printer.Get_All_Printers_By_Count_And_Model(model, True)
    for p in printers:
        if p[0].Get_Printer_State() == 'operational':
            return p[0]
    return None


@db_session
def check_for_finished_jobs():
    print("Checking for finished jobs...")
    finished_count = 0
    printers = Printer.Get_All_Enabled()
    for printer in printers:
        if not printer.printer_model.auto_start_prints:
            continue
        state, actual_print_volume = printer.Get_Printer_State(get_actual_volume=True)
        if state == 'finished':
            job = printer.Get_Current_Job()
            if job:
                job.Mark_Job_Finished()
                jira.send_print_finished(job)
                print(job.Get_Name() + " finished on " + printer.name + ".")
                finished_count += 1
                printer.Reconnect_Printer()
                if os.path.exists(job.Get_File_Name()):
                    os.remove(job.Get_File_Name())
            else:
                print(printer.name + " has finished job not found in DB.")
        elif state == 'needs_clearing':
            print(printer.name + " needs to be cleared.")
    print(str(finished_count) + " finished jobs found.")


def start_print_job(job, printer, comment_on_ticket=True):
    """
    Starts a print job on a printer and updates jira with print started comment. Also prints physical receipt.
    Returns True if successful, False if not.
    """
    upload_result = printer.Upload_Job(job)
    if upload_result.ok:
        job.printed_on = printer.id
        job.print_status = PrintStatus.PRINTING.name
        job.print_started_date = datetime.now()
        commit()
        if config["receipt_printer"]["print_physical_receipt"] is True:
            printReceipt(job)
        if comment_on_ticket:
            jira.send_print_started(job)
        print(job.Get_Name() + " started on " + printer.name + ".")
        return True
    else:
        print("Error uploading " + job.Get_Name() + " to " + printer.name + '. Status code: ' + str(upload_result.status_code))
        return False

def printReceipt(job):
    jobName = job.Get_Name(True)
    userName = job.user.Get_Name();
    printerName = job.printed_on.name if job.printed_on else ""
    
    pdf = FPDF('P', 'mm', (80, 42))
    pdf.set_margins(left = 0, right = 0, top = 0)
    pdf.set_auto_page_break(False)
    pdf.add_page()

    pdf.set_font("Courier", 'B', size = 30)
    pdf.set_xy(10, 0)
    pdf.cell(50, 10, txt = jobName, ln = 2, align = 'L', border = 0)
    fontSize = 20

    if (len(userName) <= 12):
        fontSize = 18
    elif (len(userName) <= 14):
        fontSize = 16
    elif (len(userName) <= 16):
        fontSize = 14
    elif (len(userName) <= 18):
        fontSize = 12
    elif (len(userName) <= 20):
        fontSize = 10
    elif(len(userName) > 20):
        fontSize = 10
        userName = userName[0:20]

    pdf.set_font("Courier", '', size = fontSize)
    pdf.set_xy(10, 10)
    pdf.cell(50, 10, txt = userName, ln = 2, align = 'L', border = 0)

    pdf.set_font("Courier", '', size = 8)
    pdf.set_xy(10, 20)
    pdf.cell(50, 10, txt = printerName, ln = 2, align = 'L', border = 0)

    fileName = os.getcwd() + "/receipts/" + job.Get_Name(True) + "_receipt.pdf"
    pdf.output(fileName)

    os.startfile(fileName, "print")
