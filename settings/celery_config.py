from __future__ import absolute_import, unicode_literals

import os

from dotenv import load_dotenv

load_dotenv()

accept_content = ["json"]
enable_utc = False
task_serializer = "json"
timezone = "UTC"
task_track_started = True
worker_hijack_root_logger = False
worker_redirect_stdouts_level = "ERROR"
result_expires = 60 * 60 * 24
broker_url = os.getenv("CELERY_BROKER")
