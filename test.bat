set DATABASE_URL=postgres://suresh:fsd@localhost:5432/casting_agency_test
python manage.py db upgrade
python manage.py seed
python test_app.py