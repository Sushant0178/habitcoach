echo "BUILD START"

# Install necessary packages from requirements.txt
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

# Collect static files for production
python manage.py collectstatic --noinput --clear

echo "BUILD END"
