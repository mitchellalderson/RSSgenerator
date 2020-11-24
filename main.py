from feedgen.feed import FeedGenerator
import audio_metadata
from requests import get
import tempfile
from google.cloud import storage
#import os
#import memory_profiler
#os.environ[
#'GOOGLE_APPLICATION_CREDENTIALS'] = '/Users/mitchellalderson/Documents/WebDev/RSS/rsscreatortest-2e1edcb21dfc.json'

storage_client = storage.Client()


def ingest(event, context):

    file = event
    bucket_name = file['bucket']
    print("bucket name: " + bucket_name)

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
    fg.id("https://elf.church/")
    fg.title("Evening Light Fellowship Archive")
    fg.author({
        'name': 'Evening Light Fellowship',
        'email': 'Mitch@example.com'
    })
    fg.link(href="https://elf.church/", rel='alternate')
    fg.logo('https://storage.googleapis.com/elfpodxml/Logo.png')
    fg.subtitle('Podcast Archive of Evening Light Fellowship Services')
    fg.link(href="https://elf.church/", rel='self')
    fg.language('en')
    fg.generator('Faraway Southwest LLC RSS Generator')
    fg.podcast.itunes_explicit('no')
    fg.podcast.itunes_category('Religion & Spirituality', 'Christianity')

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
        fe.enclosure(str(FileListItem), 0, 'audio/mpeg')
        LocalFile.close()
    rssfeed = fg.rss_str(pretty=True)  # Get the RSS feed as string
    uploadBucket = storage_client.bucket('elfpodxml')
    uploadBlob = uploadBucket.blob('rss.xml')

    localUploadFile = tempfile.NamedTemporaryFile(suffix='.xml')
    localUploadFile.write(bytes(rssfeed))
    localUploadFile.seek(0)
    # Write the RSS feed to a file

    uploadBlob.upload_from_file(localUploadFile)


#test1 = {"bucket": "elfpodstore"}

#ingest(test1, "null")