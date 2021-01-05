"""Local Dev Entry Point."""

from main import ingest
from dotenv import load_dotenv

load_dotenv()

test1 = {"bucket": "rsscreatortest.appspot.com"}
context = {
    "event_id":
    '277d2c5b-1acd-43d8-94d1-57c219747be4-0',
    'event_type':
    'providers/cloud.firestore/eventTypes/document.write',
    'resource':
    'projects/rsscreatortest/databases/(default)/documents/mitchpodcast/fileStore/songSpecial/broken-shovel.mp3'
}

ingest(test1, context)