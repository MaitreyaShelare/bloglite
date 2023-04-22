from celery import shared_task
from sqlalchemy import select
from jinja2 import Template
from weasyprint import HTML
from datetime import date, datetime, timedelta
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication



@shared_task(bind=True)
def exportBlogs(self, user_id):
    from models import Blog
    blogs = Blog.query.filter_by(user_id=user_id).all()

    # Create list of dictionaries containing blog data
    blogs_dict = []
    for blog in blogs:
        blog_dict = {
            'id': blog.id,
            'user_id': blog.user_id,
            'text': blog.text,
            'photo': blog.photo,
            'photo_mimetype': blog.photo_mimetype,
            'timestamp': blog.timestamp,
            'hidden': blog.hidden
        }
        blogs_dict.append(blog_dict)

    return blogs_dict

@shared_task
def daily_reminder():
    from __init__ import db
    from models import User, Blog

    # Get users who haven't posted a blog today                    
    today = date.today()
    users_without_blog_today = User.query.filter(User.id.notin_(
        Blog.query.with_entities(Blog.user_id)
            .filter(Blog.timestamp >= datetime.combine(today, datetime.min.time()),
                    Blog.timestamp < datetime.combine(today + timedelta(days=1), datetime.min.time()))
        )).all()

    for user in users_without_blog_today:
        sender_email = 'noreply@bloglite.com'
        sender_password = ''
        receiver_email = user.email
        subject = 'Your daily blogging reminder'

        message = MIMEMultipart()
        message['From'] = sender_email
        message['To'] = receiver_email
        message['Subject'] = subject
        message_text = "Hello {}, we hope you're doing well.\n\n Just a friendly reminder that it's been a while since you posted a blog.\n Please take a few minutes today to share your thoughts with our community.\n Your contributions are always valuable and appreciated.\n\nRegards,\nTeam Bloglite".format(user.name)
        message.attach(MIMEText(message_text))
        
        # Connect to SMTP server and send email
        with smtplib.SMTP('localhost', 1025) as smtp:
            smtp.login(sender_email, sender_password)
            smtp.send_message(message)
            smtp.quit()

    return 'Daily Reminder Emails sent!'


@shared_task
def generate_and_send_report(user_data):
   
    # Generate the report for the current user 
    message = format_report("report.html", user_data)
    pdf_bytes = generate_report(message)

    # Attach the report to an email and send it to the user
    sender_email = 'noreply@bloglite.com'
    sender_password = ''
    subject = 'Your Monthly Report, '+ str(user_data['name'])

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = user_data['email']
    msg['Subject'] = subject

    body = 'Hi {},\n\nPlease find attached your monthly report.\n\nBest regards,\nTeam Bloglite'.format(user_data['name'])
    msg.attach(MIMEText(body, 'plain'))

    attachment = MIMEApplication(pdf_bytes, _subtype='pdf')
    attachment.add_header('Content-Disposition', 'attachment', filename='report.pdf')
    msg.attach(attachment)


    with smtplib.SMTP('localhost', 1025) as smtp:
        smtp.login(sender_email, sender_password)
        smtp.send_message(msg)
        smtp.quit()
      


def format_report(template_file, data={}):
    with open(template_file) as f:
        template = Template(f.read())
    return template.render(data=data)

def generate_report(message):
    html=HTML(string=message)
    return html.write_pdf()


@shared_task
def monthly_report():
    from __init__ import db
    from models import User

    users = (
        db.session.query(User).all()
    )
    
    user_data = {
        "users": [
            {
                "name": user.name,
                "email": user.email,
                "prev_month": (datetime.now() - timedelta(days=30)).strftime("%B"),
                "new_followers": user.new_followers_past_month(),
                "new_following": user.new_following_past_month(),
                "blogs_posted": user.blogs_posted_past_month(),
                "blogs_liked": user.blogs_liked_past_month(),
                "blogs_commented": user.blogs_commented_past_month(),
            }
            for user in users
        ]
    }

    for user in user_data['users']:
        generate_and_send_report.delay(user)

    return 'Monthly Report Emails sent!'
  