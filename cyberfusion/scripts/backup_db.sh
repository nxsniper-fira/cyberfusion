#!/bin/bash
set -e
DATE=$(date +%F_%H-%M-%S)
mkdir -p backup
cp backend/cyberfusion.db backup/cyberfusion_$DATE.db
echo "Backup created at backup/cyberfusion_$DATE.db"