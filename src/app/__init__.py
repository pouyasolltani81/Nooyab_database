# myproject/__init__.py
from django.db.backends.mysql.base import DatabaseWrapper

def disable_database_version_check(self):
    # Override the version check to do nothing.
    return

DatabaseWrapper.check_database_version_supported = disable_database_version_check
