echo "BUILD START"

# Install necessary packages
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

# Run Migrations (Creates the database tables)
python manage.py migrate 

# Collect static files
python manage.py collectstatic --noinput --clear

echo "BUILD END"