# Bloglite


Awarded Certificate of Appreciation from IIT Madras for this project.

<p align="center">
	<img src="Best Project.png">
</p>

## Demo
https://www.youtube.com/watch?v=200HUhU0C84
## How to Run this Project?

1. Install Node and Vue CLI.
2. Copy node_modules folder into bloglite folder.
3. Open your IDE and create a Virtual Environment with all Libraries given in server/requirements.txt. 
4. Run backend code by navigating to server directory and running main.py
5. Run frontend code by navigating to bloglite folder and typing "npm run serve" in new terminal.
6. Run Celery Worker by typing "celery -A main.celery worker --loglevel=INFO" in new terminal.
7. Run Celery Beat by typing "celery -A main.celery beat --loglevel=INFO" in new terminal.
8. Run Mailhog SMTP Server by typing "Mailhog" in new terminal.
   

