#!/bin/bash
# entrypoint.sh
set -e  # Exit immediately if a command exits with a non-zero status

# Create staticfiles directory explicitly
echo "Creating staticfiles directory..."
mkdir -p /app/staticfiles
chmod 755 /app/staticfiles

# Run database migrations
echo "Running migrations..."
python manage.py migrate --noinput

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Verify static files were collected
echo "Verifying static files..."
ls -la /app/staticfiles

# Create superuser if it doesn't exist
echo "Creating superuser..."
python manage.py shell <<EOF
from django.contrib.auth import get_user_model
import os
User = get_user_model()
superuser = os.getenv("SUPERUSER_NAME")
password = os.getenv("SUPERUSER_PASSWORD")
if not User.objects.filter(username=superuser).exists():
  User.objects.create_superuser(superuser, f'{superuser}@example.com', password)
EOF

# Execute the command passed to the container
echo "Starting server..."
exec "$@"
