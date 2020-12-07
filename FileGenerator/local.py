"""Local Dev Entry Point."""

from main import ingest
from dotenv import load_dotenv

load_dotenv()

test1 = {"bucket": "elfpodstore"}

ingest(test1, "null")