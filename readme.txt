Using the app:

The app could be built locally, the requirements are django (2.0) and djangorestframework (3.7.3). Building the app from git source would require the following actions:

python manage.py migrate
python manage.py makemigrations risktypes
python manage.py migrate risktypes
python manage.py createsuperuser
python manage.py test
python manage.py runserver

Further I explain how the app can be used on the existing server (local addresses added in brackets)
a) login at 
    http://daana.pythonanywhere.com/admin/ 
    (request login if necessary)

---	(http://127.0.0.1:8000/admin/)

    Other pages won't work unless the user has logged in.


b) Navigate to 
    http://daana.pythonanywhere.com/risktypes/

---	(http://127.0.0.1:8000/risktypes/)
    This is the root of the app. 

c) Use  RiskType page to create a new RiskType (just name and description
    http://daana.pythonanywhere.com/risktypes/risktype
---	(http://127.0.0.1:8000/risktypes/risktype) NOTE NO SLASH at the end of address


d) Use RiskField page to create Riskfields for the RiskType:
    http://daana.pythonanywhere.com/risktypes/riskfield

---	(http://127.0.0.1:8000/risktypes/riskfield) NOTE NO SLASH at the end of address

    Create different types of fields for this particular risk type. Note, that the page does not check the logic of field attributes. For enum type enum_values should be a SEMICOLON separated list of strings, e.g. "field; enum; non-value". It is a major flaw of the App that it does not verify the inputs on this page but it was not explicitly mentioned in the task and I ran out of time :)


And, finally the API endpoint:

e) After a risktype exists, it's field input page can be loaded at 
http://daana.pythonanywhere.com/risktypes/index/{pk}/ - replace {pk} with the ID of your risktype

---	(http://127.0.0.1:8000/risktypes//index/{pk}/)  
The page provides validations for the data entry based on what is available in HTML. The page is not linked to the data table and does not submit. For the future potential integration with the data entry part, see DB.jpg

