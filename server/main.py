from __init__ import create_app
from flask import send_from_directory
app, celery = create_app()
app.app_context().push()

@app.route('/')
def index():
    return 'Backend'

# @app.route('/')
# def serve():
#     return send_from_directory(app.static_folder, 'index.html')

# @app.route('/<path:path>')
# def static_files(path):
#     return send_from_directory(app.static_folder, path)

if __name__ == '__main__':
    app.run(debug=True)
    # celery.worker_main(argv=['worker', '-l', 'info', '-E'])
