Vitals
======

Contents
--------

1. Folder: Api_server

2. Bash script: vitals.sh

3. Python script: Flask_notify.py

DB initialization
-----------------

1. Go to folder api-server

2. Execute db_create.py

3. Execute db_migrate.py

4. Confirm app.db has been created in the api-server folder


How to Use? Execution order?
----------------------------

1. Clone vitals folder to local computer

2. Enter app-server folder (cd vitals/api-server)

3. execute run.py (python run.py) [This will set up a localhost server]

4. Enter the vitals folder (cd vitals)

5. execute vitals.sh (bash vitals.sh)


Expected outcome
----------------

1. As the bash script (vitals.sh) is executed, health vitals data is generated (randomized, for POC) and posted on the browser. 

2. Once the data is posted, a rule-engine is executed to assess if an emergency notif is to be sent.

3. All the health-vitals data is stored vitals table (in app.db), SOS message, if any, in SOS table (in app.db), notifications, if any, in notifications table (in app.db)

4. To retrieve information from sqlite3 db in json format, visit (http://127.0.0.1:5000/Trial) in your browser. Here, it is built to retrieve the first row from the vitals table (from app.db)


Viewing Dashboard
-----------------
1. Visit http://127.0.0.1:5000/index (To view the team of fire-fighters and incoming SOS Notifications)

2. On clicking on any of the fire-fighter's names, it will display their entire vitals-chart.


