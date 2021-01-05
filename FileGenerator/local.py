"""Local Dev Entry Point."""

from main import ingest
from dotenv import load_dotenv

load_dotenv()

test1 = {"bucket": "rsscreatortest.appspot.com"}

ingest(test1, "null")