#!/bin/bash
TARGET_DIR="/home/user/files"
find "$TARGET_DIR" -type f -mtime +3 -print -delete

