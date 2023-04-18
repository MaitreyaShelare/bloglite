from celery import Celery, shared_task
import pandas as pd
import time
from flask import current_app, Response, jsonify

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication


# celery = Celery(__name__, broker='redis://localhost:6379/0', backend='redis://localhost:6379/0')

# if __name__ == '__main__':
#     celery.worker_main(argv=['worker', '-l', 'info', '-E'])

@shared_task
def long_task(duration):
    
    print(f'Starting task for {duration} seconds')
    time.sleep(duration)
    print('Task complete!')
    return 'Task complete!'

@shared_task
def exportBlogs(user_id):
    from models import User, Blog
    user = User.query.filter_by(id=user_id).first()
    blogs = Blog.query.filter_by(user_id=user_id).all()

    # Create list of dictionaries containing blog data
    blogs_dict = []
    for blog in blogs:
        blog_dict = {
            'id': blog.id,
            'user_id': blog.user_id,
            'text': blog.text,
            'photo': blog.photo,
            'mimetype': blog.photo_mimetype,
            'timestamp': blog.timestamp,
            'hidden': blog.hidden
        }
        blogs_dict.append(blog_dict)

    # Create DataFrame from blogs_dict
    df = pd.DataFrame.from_dict(blogs_dict)

    csv_data = df.to_csv(index=False, header=True)
    csv_name = f"{user.name}_blogs.csv"

    # Create email message
    message = MIMEMultipart()
    message['From'] = 'noreply.bloglite@gmail.com'
    message['To'] = user.email
    message['Subject'] = f'Exported blogs for {user.name}'
    message.attach(MIMEText(f'Hi {user.name},\n\nPlease find attached your exported blogs file.\n\nBest regards,\nBloglite Team'))

    # Attach CSV file
    csv_attachment = MIMEApplication(csv_data.encode('utf-8'), Name=csv_name)
    csv_attachment['Content-Disposition'] = f'attachment; filename="{csv_name}"'
    message.attach(csv_attachment)

    # Send email
    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.starttls()
        smtp.login('noreply.bloglite@gmail.com', 'bloglite1234')
        smtp.sendmail('noreply.bloglite@gmail.com', user.email, message.as_string())

    return f"Exported {len(blogs)} blogs for user {user.name} to email {user.email}"


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