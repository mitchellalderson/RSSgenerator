from feedgen.feed import FeedGenerator


def ingest(event, context):
    file = event

    fg = FeedGenerator()


fg.id('http://lernfunk.de/media/654321')
fg.title(file.name)
fg.author({'name': 'John Doe', 'email': 'john@example.de'})
fg.link(href=file['mediaLink'], rel='alternate')
fg.logo('http://ex.com/logo.jpg')
fg.subtitle('This is a cool feed!')
fg.link(href='http://larskiesow.de/test.atom', rel='self')
fg.language('en')
atomfeed = fg.atom_str(pretty=True)  # Get the ATOM feed as string
rssfeed = fg.rss_str(pretty=True)  # Get the RSS feed as string
fg.atom_file('atom.xml')  # Write the ATOM feed to a file
fg.rss_file('rss.xml')  # Write the RSS feed to a file

print(f"Processing file: {file['name']}.")
