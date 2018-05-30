# Regular updates from CRM

1. Get CRM extract
2. Verify that the header looks like this:
txtFilterSummary	txtFilterSummaryValue																																																			
Filter Summary	"Sales Leads:
     Country: Equals South Africa;Zambia;Zimbabwe;Lesotho;Swaziland;Mozambique;Botswana;Angola;Namibia;Congo, The Democratic Republic Of The;Malawi;Madagascar;Seychelles;Comoros;Mauritius      Status: Equals Open;Lost;Won      Created On: On or After 01/04/2014 Sales Leads -> Potential Customer (Contact):
 "																																																			
																																																				
Table0_Header0	Table0_Header1	Table0_Header2	Table0_Header3	Table0_Header4	Table0_Header5	Table0_Header6	Table0_Header8	Table0_Header10	Table0_Header12	Table0_Header13	Table0_Header14	Table0_Header15	Table0_Header17	Table0_Header19	Table0_Header20	Table0_Header21	Table0_Header22	Table0_Header23	Table0_Header24	Table0_Header25	Table0_Header27	Table0_Header29	Table0_Header30	Table0_Group0_Header0	Table0_Details1	Table0_Details2	Table0_Details3	Table0_Details4	Table0_Details5	Table0_Details6	Table0_Details8	Table0_Details10	Table0_Details12	Table0_Details13	Table0_Details14	Table0_Details15	Table0_Details17	Table0_Details19	Table0_Details20	Table0_Details21	Table0_Details22	Table0_Details23	Table0_Details24	Table0_Details25	Table0_Details27	Table0_Details29	Table0_Details30	Table0_Group0_Footer0	Table0_Group0_Footer11	Table0_Group0_Footer12	Table0_Footer11	Table0_Footer12
Owner	Status	Account	Countries	Owner	Service Group	Reference #	Created On	Est. Revenue	Est. Revenue (GBP)	Name	Contact	Country	Est. Revenue (USD)	Est. Decision Date	Sales Lead Owner	Sales Lead Title	Sales Lead	Full Name (Service Line PM)	Name (Originating Lead)	Full Name (Owning User)	Actual Close Date	Probability	Probability of WIN	


3. Put the update into C:\Users\tetyana.loskutova\Documents\Control Risks\Sales App and rename the file to 'ExtractCRM.csv'
4. Run Documents/..../Sales%20App/Get%20data.ipynb until the extract is exported into Excel
5. If the resulting file (CRM_leads.xlsx) does not contain 'Sales Originator' field, rename 'Owner' to 'Sales Originator'
6. Put the file into data\ folder on web server and run salesaccounts\import_leads

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


Site must be run from .virtualenvs salesapp.pythonanywhere.com/bin/source activate