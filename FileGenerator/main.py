"""Generates RSS feed from directory of files."""

from feedgen.feed import FeedGenerator
import audio_metadata
from requests import get
import tempfile
from google.cloud import storage, firestore
import os
import ast
import datetime

Client_Id = os.environ.get('Client_Id')
Client_URL = os.environ.get('Client_URL')
Channel_Title = os.environ.get('Channel_Title')
Logo_URL = os.environ.get('Logo_URL')
Channel_Subtitle = os.environ.get('Channel_Subtitle')
Itunes_Category = os.environ.get('Itunes_Category')
XML_Upload_Location = os.environ.get('XML_Upload_Location')
Channel_Author = ast.literal_eval(os.environ.get('Channel_Author'))
Itunes_Author = os.environ.get('Itunes_Author')
XML_Name = os.environ.get('XML_Name')
GOOGLE_APPLICATION_CREDENTIALS = os.environ.get(
    'GOOGLE_APPLICATION_CREDENTIALS')

storage_client = storage.Client()


def ingest(event, context):
    """Read bucket, get file listing, write file listing to database."""
    bucket_name = event['bucket']
    print("bucket name: " + bucket_name)

    blobs = storage_client.list_blobs(bucket_name)
    print("blobs:")

    firestore_client = firestore.Client()
    client_doc = firestore_client.collection(Client_Id).document('fileStore')

    for blob in blobs:

        doc_ref = client_doc.collection('songSpecial').document(blob.name)
        doc = doc_ref.get()
        if doc.exists:
            print(blob.name + " song already logged")
        else:
            print(blob.name + " added to database")

            getLocalFile = get(blob.public_url)
            LocalFile = tempfile.NamedTemporaryFile(suffix='.mp3',
                                                    delete=False)
            LocalFile.write(getLocalFile.content)
            LocalFile.seek(0)
            fileMeta = audio_metadata.load(LocalFile.name)

            doc_write = client_doc.collection('songSpecial').document(
                blob.name)
            if 'title' in fileMeta.tags:
                doc_write.set({
                    u'name':
                    blob.name,
                    u'PublicURL':
                    blob.public_url,
                    u'title': (str(fileMeta.tags['title']).strip('\'\[\]')),
                    u'artist': (str(fileMeta.tags['artist']).strip('\'\[\]')),
                    u'filesize':
                    int(fileMeta['filesize']),
                    u'UploadDate': (datetime.datetime.today())
                })
            LocalFile.close()
            os.unlink(LocalFile.name)

    files = client_doc.collection('songSpecial').stream()
    FileList = {}
    for file in files:
        FileList.update({file.id: file.to_dict()})
    FeedFileGen(FileList)


def FeedFileGen(FileList):
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