#!/usr/bin/python3
"""This script will create a unique FileStorage instance."""
import models.engine.file_storage as fs

storage = fs.FileStorage()
storage.reload()
