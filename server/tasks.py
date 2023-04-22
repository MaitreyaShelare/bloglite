from celery import shared_task, group
from jinja2 import Template
from weasyprint import HTML
# import pandas as pd
# import time
# from flask import current_app, Response, jsonify
from datetime import date, datetime, timedelta
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication


# @shared_task
# def long_task():
#     print('Task complete!')
#     return 'Task complete!'

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

    users_with_blog_today = (
        db.session.query(Blog.user_id)
        .filter(Blog.timestamp >= date.today())
        .distinct()
        .subquery()
    )

    # Query for all users who are not in the above result
    users_without_blog_today = (
        db.session.query(User)
        .filter(~User.id.in_(users_with_blog_today))
        .all()
    )

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
        # message.attach(MIMEText('Hello {}, it\'s time to post a blog!'.format(user.name), 'plain'))

        # Connect to SMTP server and send email
        with smtplib.SMTP('localhost', 1025) as smtp:
            smtp.login(sender_email, sender_password)
            smtp.send_message(message)
            smtp.quit()

    return 'Daily Reminder Emails sent!'

# @shared_task
# def monthly_report():
#     # from __init__ import db
#     # from models import User, Blog, Like, Comment, user_followers, user_likes

#     # users_with_blog_today = (
#     #     db.session.query(Blog.user_id)
#     #     .filter(Blog.timestamp >= date.today())
#     #     .distinct()
#     #     .subquery()
#     # )

#     # # Query for all users who are not in the above result
#     # users_without_blog_today = (
#     #     db.session.query(User)
#     #     .filter(~User.id.in_(users_with_blog_today))
#     #     .all()
#     # )
#     data = {
#     "users": [
#         {
#             "name": "John Doe",
#             "age": 42,
#             "occupation": "Software Engineer",
#             "hobbies": ["Programming", "Reading", "Hiking"],
#             "email": "john.doe@example.com"
#         },
#         {
#             "name": "Jane Smith",
#             "age": 35,
#             "occupation": "Graphic Designer",
#             "hobbies": ["Painting", "Traveling", "Cooking"],
#             "email": "jane.smith@example.com"
#         },
#         {
#             "name": "Bob Johnson",
#             "age": 50,
#             "occupation": "Marketing Manager",
#             "hobbies": ["Golfing", "Watching Movies", "Fishing"],
#             "email": "bob.johnson@example.com"
#         }
#     ]
# }

#     for user in data['users']:
#         sender_email = 'noreply@bloglite.com'
#         sender_password = ''
#         receiver_email = user.email
#         subject = 'Your daily blogging reminder'

#         message = MIMEMultipart()
#         message['From'] = sender_email
#         message['To'] = receiver_email
#         message['Subject'] = subject
#         message_text = "Hello {}, we hope you're doing well.\n\n Just a friendly reminder that it's been a while since you posted a blog.\n Please take a few minutes today to share your thoughts with our community.\n Your contributions are always valuable and appreciated.\n\nRegards,\nTeam Bloglite".format(user.name)
#         message.attach(MIMEText(message_text))
        

#         # Connect to SMTP server and send email
#         with smtplib.SMTP('localhost', 1025) as smtp:
#             smtp.login(sender_email, sender_password)
#             smtp.send_message(message)
#             smtp.quit()

#     return 'Monthly Report Emails sent!'

@shared_task
def generate_and_send_report(user_data):
   
    # Generate the report for the current user 
    message = format_report("report.html", user_data)
    pdf_bytes = generate_report(message)

    # Attach the report to an email and send it to the user
    sender_email = 'noreply@bloglite.com'
    sender_password = ''
    # receiver_email = user.email
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
    from models import User, Blog, Like, Comment, user_followers, user_likes

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
  















    # df = pd.DataFrame.from_dict(blogs_dict)

    # csv_data = df.to_csv(index=False, header=True)
    # csv_name = f"{user.name}_blogs.csv"

    # print(csv_data)
    # return csv_data

    # return {'csv_data': csv_data, 'csv_name': csv_name}
    # response = {
    #     'csv_data': csv_data
    # }
    # return jsonify(response)
    # return {'csv_data': csv_data}
#     return Response(
#         csv_data,
        # mimetype="text/csv",
        # headers={"Content-disposition":
        #         f"attachment; filename={csv_name}"}
# )

    # csv_name = f"{user.name}_blogs.csv"

    # return Response(
    # csv_data,
    # mimetype="text/csv",
    # headers={"Content-disposition":
    #         "attachment; filename=blogs.csv"})
    

# @shared_task
# def exportBlogs(user_id):
#     # Create email message
#     sender_email = 'noreply@bloglite.com'
#     sender_password = ''
#     receiver_email = 'example@example.com'
#     subject = 'Exported blogs'

#     message = MIMEMultipart()
#     message['From'] = sender_email
#     message['To'] = receiver_email
#     message['Subject'] = subject
#     message.attach(MIMEText('Hi,\n\nPlease find attached your exported blogs file.\n\nBest regards,\nBloglite Team'))

#     # # Read CSV file
#     # with open('blogs.csv', 'rb') as csv_file:
#     #     csv_data = csv_file.read()

#     # # Attach CSV file
#     # csv_attachment = MIMEApplication(csv_data, Name='blogs.csv')
#     # csv_attachment['Content-Disposition'] = f'attachment; filename="blogs.csv"'
#     # message.attach(csv_attachment)

#     # Connect to MailHog and send email
#     with smtplib.SMTP('localhost', 1025) as smtp:
#         smtp.login(sender_email, sender_password)
#         smtp.send_message(message)
#         smtp.quit(message)
#         # smtp.sendmail(sender_email, receiver_email, message.as_string())

#     print('Email sent!')

# @celery.task
# def async_export_blogs(user_id):
#     user = User.query.filter_by(id=user_id).first()
#     blogs = Blog.query.filter_by(hidden=False).order_by(Blog.timestamp.desc()).all()
#     blog_ids = [blog.id for blog in blogs]
#     return 'Task complete!'

# @blog.route('api/blog/export/<int:blog_id>', methods=['GET'])
# @jwt_required()
# def export_blog(blog_id):
#     blog = Blog.query.filter_by(id=blog_id).first()
#     if blog:
#         blog_dict = {
#             'id': blog.id,
#             'user_id': blog.user_id,
#             'text': blog.text,
#             'photo': blog.photo,
#             'mimetype': blog.photo_mimetype,
#             'timestamp': blog.timestamp,
#             'hidden': blog.hidden
#         }
#         df = pd.DataFrame([blog_dict])
#         csv = df.to_csv(index=False, header=True)
#         return Response(
#             csv,
#             mimetype="text/csv",
#             headers={"Content-disposition":
#                      "attachment; filename=blog.csv"})
#     else:
#         return jsonify(error="Error in Blog Export"), 404