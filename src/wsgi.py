import predictor as service

# This is just a simple wrapper for gunicorn to find your app.
# If you want to change the algorithm file, simply change "predictor" above to the
# new file.

# Automatically calling wsgi:app by gunicorn
app = service.app #Connect to flask
