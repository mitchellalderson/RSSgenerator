from google.cloud import storage, firestore
import os

Client_Id = 'mitchpodcast'
Client_URL = 'https://farawaysouthwest.com'

Itunes_Category = 'Technology'
XML_Upload_Location = 'archangelrss'
Channel_Author = 'Mitch Alderson'
Itunes_Author = 'Mitch Alderson'

fileTypes = {
    'podcast': {
        'Channel_Title': 'Mitch Learns Stuff',
        'Logo_URL':
        'https://storage.googleapis.com/elfpodxml/mitchpodcastlogo.png',
        'Channel_Subtitle': 'Curiosity killed the cat, not us.',
        'XML_Name': 'mitchpodcastrss.xml',
        'Itunes_Category': 'Technology'
    }
}

###############################################

GOOGLE_APPLICATION_CREDENTIALS = os.environ.get(
    'GOOGLE_APPLICATION_CREDENTIALS')

firestore_client = firestore.Client()
doc_write = firestore_client.collection(Client_Id).document('config')
doc_write.set({
    u'Client_Id': Client_Id,
    u'Client_URL': Client_URL,
    u'Itunes_Category': Itunes_Category,
    u'XML_Upload_Location': XML_Upload_Location,
    u'Channel_Author': {
        'name': Channel_Author
    },
    u'fileTypes': fileTypes,
    u'Itunes_Author': Itunes_Author,
})
