from google.cloud import firestore
import firebase_admin
from firebase_admin import auth
import os

GOOGLE_APPLICATION_CREDENTIALS = os.environ.get(
    'GOOGLE_APPLICATION_CREDENTIALS')
default_app = firebase_admin.initialize_app()

clientID = 'test'

user = auth.create_user(email='user@example.com',
                        email_verified=False,
                        password='7ChurchAges!',
                        disabled=False)
print('Sucessfully created new user: {0}'.format(user.uid))

firestore_client = firestore.Client()
doc_write = firestore_client.collection('users').document(user.uid)
doc_write.set({u'client': clientID, u'admin': False})
