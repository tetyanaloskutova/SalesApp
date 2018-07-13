# Regular updates from CRM

1. Get CRM extract SA Sales by Owner - Tableau Build 2 in EXCEL format
2. Verify that the header looks like this:
Filter Summary	
"Sales Leads:
     Country: Equals South Africa;Zambia;Zimbabwe;Lesotho;Swaziland;Mozambique;Botswana;Angola;Namibia;Congo, The Democratic Republic Of The;Malawi;Madagascar;Seychelles;Comoros;Mauritius      Status: Equals Open;Lost;Won      Created On: On or After 01/04/2014 Sales Leads -> Potential Customer (Contact):
 "																								
Owner	Status	Account	Countries	Owner	Service Group	Reference #	Created On	Est. Revenue	Est. Revenue (GBP)	Name	Contact	Country	Est. Revenue (USD)	Est. Decision Date	Sales Lead Owner	Sales Lead Title	Sales Lead	Full Name (Service Line PM)	Name (Originating Lead)	Full Name (Owning User)	Actual Close Date	Probability	Probability of WIN

3. Rename the file CRM_Leads.xlsx and put the file into data\ folder on web server and run salesaccounts\import_leads

#Fields updated on import from CRM:
['Sales Originator'])
['Service Group']
['Contact']
['Country']
['Est. Revenue (USD)'])
['Est. Decision Date'], 
['Sales Lead Owner'])
['Full Name (Service Line PM)'])
['Full Name (Owning User)'])
		
		
# Irregular updates
Irregular updates can be done as follows:
1. Check the location of the \data folder on the server using http://salesapp.pythonanywhere.com/salesaccounts/get_current_directory/
2. Accounts belonging to Top 40. Put Top40_load.xlsx into \data folder on the webserver and run salesaccounts\import_leads
3. Service leads could be imported in the same way


# Exports 
Run salesaccounts\export_leads and download the file from \data folder (Check the location of the \data folder on the server using http://http://salesapp.pythonanywhere.com/salesaccounts/get_current_directory/)

# Rights
Admin rights are required for:
1. Import
2. Export
3. Creation of new users

Site admin (pythonanywhere user) is required to access the website structure

# Code updates
The code is open source and hosted at https://github.com/tetyanaloskutova/SalesApp
Update from the repository: 
1. git pull
or
2. git reset --hard
   git pull

# Running the Site
Site must be run from .virtualenvs salesapp.pythonanywhere.com/bin/source activate
Free service at PythonAnywhere means that every three months, the site would be disabled unless the admin logs in to re-activate the subscription. As a side effect, this re-login offloads the virtual environtment, which has to be reloaded again. To do so.
1) Log in to BASH console (preferrable using the existing console)
2) Naviga to salesapp/.virtualenvs. The approximate list of commands follow:
9:58 ~/salesapp.pythonanywhere.com/static (master)$ cd ..
09:59 ~/salesapp.pythonanywhere.com (master)$ cd ..
09:59 ~ $ ls
README.txt  data  salesapp.pythonanywhere.com
10:00 ~ $ cd .virtualenvs/
10:00 ~/.virtualenvs $ ls
3. Activate virtualenvironment:
11:13 ~/.virtualenvs $ source salesapp.pythonanywhere.com/bin/activate
4. Check that the virtual environment is activated (its name would appear in brackets in the command-line prompt):
(salesapp.pythonanywhere.com) 11:14 ~/.virtualenvs $ 
