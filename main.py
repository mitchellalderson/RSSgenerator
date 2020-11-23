from feedgen.feed import FeedGenerator
import audio_metadata
from requests import get
import tempfile

test1 = {
    "name": "test",
    "mediaLink":
    "https://storage.googleapis.com/elfpodstore/Audio/untitled.mp3",
    "selfLink": "testURLself"
}


def ingest(event, context):
    file = event
    getLocalFile = get(file['mediaLink'])
    LocalFile = tempfile.NamedTemporaryFile(suffix='.mp3')
    LocalFile.write(getLocalFile.content)
    LocalFile.seek(0)

    fileMeta = audio_metadata.load(LocalFile.name)
    print("Artist name is: " + str(fileMeta.tags['artist']))
    print(fileMeta)
    fg = FeedGenerator()

    fg.id('http://lernfunk.de/media/654321')
    fg.title("Evening Light Fellowship Archive")
    fg.author({
        'name': 'Evening Light Fellowship',
        'email': 'Mitch@example.com'
    })
    fg.link(href="https://elf.church/", rel='alternate')
    fg.logo('https://storage.googleapis.com/elfpodstore/ELF_LOGO.png')
    fg.subtitle('Podcast Archive of Evening Light Fellowship Services')
    fg.link(href="https://elf.church/", rel='self')
    fg.language('en')
    fg.generator('Faraway Southwest LLC RSS Generator')
    atomfeed = fg.atom_str(pretty=True)  # Get the ATOM feed as string
    rssfeed = fg.rss_str(pretty=True)  # Get the RSS feed as string
    #fg.atom_file('atom.xml')  # Write the ATOM feed to a file
    #fg.rss_file('rss.xml')  # Write the RSS feed to a file

    print("file output complete")


#ingest(test1, "null")