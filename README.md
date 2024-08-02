# Backend:Designing an Automated Email Scheduling API

## Details of the project to be completed:
### Objective: 
The objective of this assignment is to design and implement an API that allows users to schedule emails for automatic delivery at specified times. This involves creating endpoints to accept payloads containing email details (recipient, subject, body) along with a schedule time, and implementing a backend process to handle the scheduling and sending of emails accordingly. The API will also include options for scheduling recurring emails on a daily, weekly, monthly, or quarterly basis, thereby automating the process of email delivery and ensuring that emails are sent as per user-defined schedules.




## Installation

Create a new folder and work in that directory.

```bash
  mkdir email_automation_backend
  cd email_automation_backend
```
Open the terminal and clone the repo    
```bash
  git clone https://github.com/okaditya84/Shipmnts-Task
```    

Create virtual env and activate it:
```bash
python -m venv env
env\Scripts\activate
```
Download the dependencies:
```bash
pip install -r requirements.txt
```

Create a .env file and replace your credentials:
```bash
EMAIL_FROM=<your_email_in_quotations>
EMAIL_USER=<your_email_in_quotations>
EMAIL_PASSWORD=<your_password_in_quotations>
```
Install redis:
```bash
curl -fsSL https://packages.redis.io/gpg | sudo gpg --dearmor -o /usr/share/keyrings/redis-archive-keyring.gpg

echo "deb [signed-by=/usr/share/keyrings/redis-archive-keyring.gpg] https://packages.redis.io/deb $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/redis.list

sudo apt-get update
sudo apt-get install redis
```
run redis on WSL

Run the celery client:
```bash
celery -A tasks worker --loglevel=info
```

### Steps to run:
Keep the activated env ready

```bash
python app.py
```

Test the Endpoints on Postman.
