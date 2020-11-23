from feedgen.feed import FeedGenerator
import audio_metadata

test1 = {
    "name": "test",
    "mediaLink":
    "https://storage.googleapis.com/elfpodstore/Audio/broken-shovel.mp3",
    "selfLink": "testURLself"
}


def ingest(event, context):
    file = event
    fileLocation = file['mediaLink']
    print(fileLocation)
    fileMeta = audio_metadata.load(fileLocation)
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