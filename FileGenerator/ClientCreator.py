from google.cloud import storage, firestore
import os

Client_Id = 'EveningLight'
Client_URL = 'https://elf.church/'
Channel_Title = 'Evening Light Fellowship Song Specials'
Logo_URL = 'https://storage.googleapis.com/elfpodxml/Logo.png'
Channel_Subtitle = 'Podcast Archive of Evening Light Fellowship Song Specials'
Itunes_Category = 'Religion & Spirituality'
XML_Upload_Location = 'elfpodxml'
Channel_Author = 'Evening Light Fellowship'
Itunes_Author = 'Evening Light Fellowship'
XML_Name = 'localdev.xml'
GOOGLE_APPLICATION_CREDENTIALS = os.environ.get(
    'GOOGLE_APPLICATION_CREDENTIALS')

firestore_client = firestore.Client()
doc_write = firestore_client.collection(Client_Id).document('config')
doc_write.set({
    u'Client_Id': Client_Id,
    u'Client_URL': Client_URL,
    u'Channel_Title': Channel_Title,
    u'Logo_URL': Logo_URL,
    u'Channel_Subtitle': Channel_Subtitle,
    u'Itunes_Category': Itunes_Category,
    u'XML_Upload_Location': XML_Upload_Location,
    u'Channel_Author': {
        'name': Channel_Author
    },
    u'Itunes_Author': Itunes_Author,
    u'XML_Name': XML_Name,
})
