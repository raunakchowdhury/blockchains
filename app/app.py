from app import app #imports the app from the app package

'''
make sure you set the env variable as such:
$ export FLASK_APP=app.py
$ export FLASK_ENV=development #enables the debugger
$ flask run
'''

if __name__ == '__main__':
    app.run(debug=True)
