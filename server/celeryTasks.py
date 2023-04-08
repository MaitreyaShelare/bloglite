# from celery import Celery
# from flask import current_app, Response, jsonify
# from models import Blog, User
# import pandas as pd
# import smtplib
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart
# from email.mime.application import MIMEApplication

# # celery = Celery(__name__, broker=current_app.config['CELERY_BROKER_URL'])
# celery = Celery(__name__, broker='redis://localhost:6379/0', backend='redis://localhost:6379/0')
# celery.conf.task_routes = {
#         'app.celeryTasks.*': {'queue': 'default'}
#     }

# @celery.task
# def exportBlogs(user_id):
#     user = User.query.filter_by(id=user_id).first()
#     blogs = Blog.query.filter_by(user_id=user_id).all()

#     # Create list of dictionaries containing blog data
#     blogs_dict = []
#     for blog in blogs:
#         blog_dict = {
#             'id': blog.id,
#             'user_id': blog.user_id,
#             'text': blog.text,
#             'photo': blog.photo,
#             'mimetype': blog.photo_mimetype,
#             'timestamp': blog.timestamp,
#             'hidden': blog.hidden
#         }
#         blogs_dict.append(blog_dict)

#     # Create DataFrame from blogs_dict
#     df = pd.DataFrame.from_dict(blogs_dict)

#     csv_data = df.to_csv(index=False, header=True)
#     csv_name = f"{user.name}_blogs.csv"

#     # Create email message
#     message = MIMEMultipart()
#     message['From'] = 'noreply.bloglite@gmail.com'
#     message['To'] = user.email
#     message['Subject'] = f'Exported blogs for {user.name}'
#     message.attach(MIMEText(f'Hi {user.name},\n\nPlease find attached your exported blogs file.\n\nBest regards,\nBloglite Team'))

#     # Attach CSV file
#     csv_attachment = MIMEApplication(csv_data.encode('utf-8'), Name=csv_name)
#     csv_attachment['Content-Disposition'] = f'attachment; filename="{csv_name}"'
#     message.attach(csv_attachment)

#     # Send email
#     with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
#         smtp.starttls()
#         smtp.login('noreply.bloglite@gmail.com', 'Bloglite@1234')
#         smtp.sendmail('noreply.bloglite@gmail.com', user.email, message.as_string())

#     return f"Exported {len(blogs)} blogs for user {user.name} to email {user.email}"


# # def exportBlogs(user_id):
# #     user = User.query.filter_by(id=user_id).first()
# #     blogs = Blog.query.filter_by(user_id=user_id).all()

# #     # Create list of dictionaries containing blog data
# #     blogs_dict = []
# #     for blog in blogs:
# #         blog_dict = {
# #             'id': blog.id,
# #             'user_id': blog.user_id,
# #             'text': blog.text,
# #             'photo': blog.photo,
# #             'mimetype': blog.photo_mimetype,
# #             'timestamp': blog.timestamp,
# #             'hidden': blog.hidden
# #         }
# #         blogs_dict.append(blog_dict)

# #     # Create DataFrame from blogs_dict
# #     df = pd.DataFrame.from_dict(blogs_dict)

# #     csv = df.to_csv(index=False, header=True)

# #     return Response(
# #             csv,
# #             mimetype="text/csv",
# #             headers={"Content-disposition":
# #                      "attachment; filename=blog.csv"})


#     # return f"Exported {len(blogs)} blogs for user {user.name} to {csv}"
#     # # Generate CSV file name
#     # file = f"{user.name}_blogs.csv"

#     # # Export CSV file
#     # df.to_csv(file, index=False, header=True)



#     # for blog in blogs:
#         # blog_dict = {
#         #     'id': blog.id,
#         #     'user_id': blog.user_id,
#         #     'text': blog.text,
#         #     'photo': blog.photo,
#         #     'mimetype': blog.photo_mimetype,
#         #     'timestamp': blog.timestamp,
#         #     'hidden': blog.hidden
#         # }
#     #     df = pd.DataFrame([blog_dict])
#     #     csv = df.to_csv(index=False, header=True)
#     #     return Response(
#     #         csv,
#     #         mimetype="text/csv",
#     #         headers={"Content-disposition":
#     #                  "attachment; filename=blog.csv"})
#     # else:
#     #     return jsonify(error="Error in Blog Export"), 404

# # def exportBlogs(user_id):
# #     # Query for user
# #     user = User.query.filter_by(id=user_id).first()

# #     # Query for blogs created by user
# #     blogs = Blog.query.filter_by(user_id=user_id).all()

# #     # Convert blogs to dictionary
# #     blogs_dict = [blog.to_dict() for blog in blogs]

# #     # Create DataFrame from blogs_dict
# #     df = pd.DataFrame.from_dict(blogs_dict)

# #     # Generate CSV file name
# #     file_name = f"{user.username}_blogs.csv"

# #     # Export CSV file
# #     df.to_csv(file_name, index=False)

# #     return f"Exported {len(blogs)} blogs for user {user.username} to {file_name}"
