from feedgen.feed import FeedGenerator
import audio_metadata
from requests import get
import tempfile
from google.cloud import storage
import os
from dotenv import load_dotenv
import ast
#from memory_profiler import profile
load_dotenv()
#os.environ[
#   'GOOGLE_APPLICATION_CREDENTIALS'] = '/Users/mitchellalderson/Documents/WebDev/RSS/rsscreatortest-2e1edcb21dfc.json'

Client_URL = os.environ.get('Client_URL')
Channel_Title = os.environ.get('Channel_Title')
Logo_URL = os.environ.get('Logo_URL')
Channel_Subtitle = os.environ.get('Channel_Subtitle')
Itunes_Category = os.environ.get('Itunes_Category')
XML_Upload_Location = os.environ.get('XML_Upload_Location')
Channel_Author = ast.literal_eval(os.environ.get('Channel_Author'))
Itunes_Author = os.environ.get('Itunes_Author')

storage_client = storage.Client()


def ingest(event, context):
    file = event
    bucket_name = file['bucket']
    #print("bucket name: " + bucket_name)

    blobs = storage_client.list_blobs(
        bucket_name,
        prefix='Audio/mp3/',
    )
    print("blobs:")
    FileList = []

    for blob in blobs:
        print(blob.name)
        FileList.append(blob.public_url)
    FileList.pop(0)
    FeedFileGen(FileList)


def FeedFileGen(FileList):

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
        getLocalFile = get(FileListItem)
        LocalFile = tempfile.NamedTemporaryFile(suffix='.mp3')
        LocalFile.write(getLocalFile.content)
        LocalFile.seek(0)

        fileMeta = audio_metadata.load(LocalFile.name)

        fe = fg.add_entry()
        fe.id(str(FileListItem))
        fe.title(str(fileMeta.tags['title']).strip('\'\[\]'))
        fe.description(str(fileMeta.tags['artist']).strip('\'\[\]'))
        fe.updated()
        fe.enclosure(str(FileListItem), 0, 'audio/mpeg')
        #fe.published('')
        LocalFile.close()
    rssfeed = fg.rss_str(pretty=True)  # Get the RSS feed as string

    uploadBucket = storage_client.bucket(XML_Upload_Location)
    uploadBlob = uploadBucket.blob('rss.xml')

    localUploadFile = tempfile.NamedTemporaryFile(suffix='.xml')
    localUploadFile.write(bytes(rssfeed))
    localUploadFile.seek(0)

    # Write the RSS feed to a file
    metadata = 'no-cache, max-age=0'
    uploadBlob.cache_control = metadata
    uploadBlob.upload_from_file(localUploadFile)
    localUploadFile.close()


#TODO: probably need some kind of memory cleanup?

#test1 = {"bucket": "elfpodstore"}

#ingest(test1, "null")