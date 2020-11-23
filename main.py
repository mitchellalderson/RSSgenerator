from feedgen.feed import FeedGenerator
import audio_metadata
from requests import get
import tempfile
from google.cloud import storage


def ingest(event, context):

    file = event
    bucket_name = file['bucket']
    storage_client = storage.Client()
    print("bucket name: " + bucket_name)

    blobs = storage_client.list_blobs(bucket_name, prefix='audio')
    print("blobs:")
    print(blobs)
    for blob in blobs:
        print(blob.name)

    getLocalFile = get(file['mediaLink'])
    LocalFile = tempfile.NamedTemporaryFile(suffix='.mp3')
    LocalFile.write(getLocalFile.content)
    LocalFile.seek(0)

    fileMeta = audio_metadata.load(LocalFile.name)

    fg = FeedGenerator()
    fg.load_extension('podcast')
    fg.id("https://elf.church/")
    fg.title("Evening Light Fellowship Archive")
    fg.author({
        'name': 'Evening Light Fellowship',
        'email': 'Mitch@example.com'
    })
    fg.link(href="https://elf.church/", rel='alternate')
    fg.logo('https://storage.googleapis.com/elfpodstore/Logo.png')
    fg.subtitle('Podcast Archive of Evening Light Fellowship Services')
    fg.link(href="https://elf.church/", rel='self')
    fg.language('en')
    fg.generator('Faraway Southwest LLC RSS Generator')
    fg.podcast.itunes_explicit('no')
    fg.podcast.itunes_category('Religion & Spirituality', 'Christianity')

    #atomfeed = fg.atom_str(pretty=True)  # Get the ATOM feed as string

    #fg.atom_file('atom.xml')  # Write the ATOM feed to a file

    fe = fg.add_entry()
    fe.id(str(file['mediaLink']))
    fe.title(str(fileMeta.tags['title']).strip('\'\[\]'))
    fe.description(str(fileMeta.tags['artist']).strip('\'\[\]'))
    fe.enclosure(str(file['mediaLink']), 0, 'audio/mpeg')

    rssfeed = fg.rss_str(pretty=True)  # Get the RSS feed as string
    #fg.rss_file('rss.xml')  # Write the RSS feed to a file


test1 = {
    "name": "test",
    "mediaLink":
    "https://storage.googleapis.com/elfpodstore/Audio/untitled.mp3",
    "selfLink": "testURLself"
}

#ingest(test1, "null")