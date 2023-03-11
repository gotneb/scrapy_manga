from firebase_admin import initialize_app, credentials


# Fetch the service account key JSON file contents
key = 'utils/mangahub-db-firebase-adminsdk-4qhsc-afec3b5b9b.json'
cred = credentials.Certificate(key)

# Initialize the app with a service account, granting admin privileges
db_url = 'https://mangahub-db.firebaseio.com'
initialize_app(cred, {
    'databaseURL': db_url
})
