import asyncio
import sys

import uvloop
uvloop.install()


__version__ = '0.6'

if sys.version_info.minor < 7:
    # alias for previous python versions
    asyncio.create_task = asyncio.ensure_future
