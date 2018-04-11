Using the sales_App:

The app could be built locally, the requirements are django (2.0) and djangorestframework (3.7.3). Building the app from git source would require the following actions:

python manage.py migrate
python manage.py makemigrations risktypes
python manage.py migrate risktypes
python manage.py createsuperuser
python manage.py test
python manage.py runserver

Further I explain how the app can be used on the existing server (local addresses added in brackets)
a) login at 
    http://salesapp.pythonanywhere.com/admin/ 
    (request login if necessary)

    Other pages won't work unless the user has logged in.


