"""Local Dev Entry Point."""

from main import ingest
from dotenv import load_dotenv

load_dotenv()

test1 = {"bucket": "rsscreatortest.appspot.com"}
context = {
    "resource":
    "projects/rsscreatortest/databases/(default)/documents/localdevtest/fileStore/songSpecial/cayuga-summer.mp3"
}

ingest(test1, context)