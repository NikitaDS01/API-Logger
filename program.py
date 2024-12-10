import logging
import asyncio
from datetime import datetime
import tempfile

from app import create_app
from app.bot import bot


if __name__ == "__main__":
    create_app().run()