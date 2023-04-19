from __init__ import create_app
app, celery = create_app()
app.app_context().push()

@app.route('/')
def index():
    return 'Backend'

if __name__ == '__main__':
    app.run(debug=True)
   
