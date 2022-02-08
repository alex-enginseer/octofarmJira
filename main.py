import jira
import schedule
import time
import octoprint

jira.getGcode()
octoprint.eachNewFile()
octoprint.PrintIsFinished()

delay = 1

print("PRINT MONITORING SYSTEM LOOP STARTED")
schedule.every(delay).minutes.do(jira.getGcode)
schedule.every(delay).minutes.do(octoprint.eachNewFile)
schedule.every(delay).minutes.do(octoprint.PrintIsFinished)

while 1:
    schedule.run_pending()
    time.sleep(1)
