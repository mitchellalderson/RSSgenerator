"""Generates RSS feed from directory of files."""

from feedgen.feed import FeedGenerator
import audio_metadata
from requests import get
import tempfile
from google.cloud import storage, firestore
import os
import ast
import datetime

Client_Id = ''
Client_URL = ''
Channel_Title = ''
Logo_URL = ''
Channel_Subtitle = ''
Itunes_Category = ''
XML_Upload_Location = ''
Channel_Author = ''
Itunes_Author = ''
XML_Name = ''
GOOGLE_APPLICATION_CREDENTIALS = os.environ.get(
    'GOOGLE_APPLICATION_CREDENTIALS')


def ingest(event, context):
    """Get Client Config."""
    path = context['resource']
    path_parts = path.split('/documents/')[1].split('/')
    Client_Id = path_parts[0]

    firestore_client = firestore.Client()

    client_config = firestore_client.collection(Client_Id).document(
        'config').get()
    Client_URL = client_config._data['Client_URL']
    Channel_Title = client_config._data['Channel_Title']
    Logo_URL = client_config._data['Logo_URL']
    Channel_Subtitle = client_config._data['Channel_Subtitle']
    Itunes_Category = client_config._data['Itunes_Category']
    XML_Upload_Location = client_config._data['XML_Upload_Location']
    Channel_Author = client_config._data['Channel_Author']
    Itunes_Author = client_config._data['Itunes_Author']
    XML_Name = client_config._data['XML_Name']
    """Get file list."""
    client_doc = firestore_client.collection(Client_Id).document('fileStore')

    files = client_doc.collection('songSpecial').stream()
    FileList = {}
    for file in files:
        FileList.update({file.id: file.to_dict()})
    """Generate XML from file FileList."""
    fg = FeedGenerator()
    fg.load_extension('podcast')
    fg.id(Client_URL)
    fg.title(Channel_Title)
    fg.author(Channel_Author)
    fg.link(href=Client_URL, rel='alternate')
    fg.logo(Logo_URL)
    fg.subtitle(Channel_Subtitle)
    fg.link(href=Client_URL, rel='self')
    fg.language('en')
    fg.generator('Faraway Southwest LLC RSS Generator')
    fg.podcast.itunes_explicit('no')
    fg.podcast.itunes_category(Itunes_Category)
    fg.podcast.itunes_author(Itunes_Author)

    #atomfeed = fg.atom_str(pretty=True)  # Get the ATOM feed as string

    #fg.atom_file('atom.xml')  # Write the ATOM feed to a file

    for FileListItem in FileList:

        fe = fg.add_entry()
        fe.id(FileList[FileListItem]['PublicURL'])
        fe.title(FileList[FileListItem]['title'])
        fe.description(FileList[FileListItem]['artist'])
        fe.published(FileList[FileListItem]['UploadDate'])
        fe.enclosure(FileList[FileListItem]['PublicURL'],
                     str(FileList[FileListItem]['filesize']), 'audio/mpeg')

    rssfeed = fg.rss_str(pretty=True)  # Get the RSS feed as string

    storage_client = storage.Client()

    uploadBucket = storage_client.bucket(XML_Upload_Location)
    uploadBlob = uploadBucket.blob(XML_Name)

    localUploadFile = tempfile.NamedTemporaryFile(suffix='.xml')
    localUploadFile.write(bytes(rssfeed))
    localUploadFile.seek(0)

    # Write the RSS feed to a file
    metadata = 'no-cache, max-age=0'
    uploadBlob.cache_control = metadata
    uploadBlob.upload_from_file(localUploadFile)
    localUploadFile.close()


#TODO: probably need some aditional of memory cleanup?