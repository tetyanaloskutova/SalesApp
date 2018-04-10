# Full path and name to your csv file 
csv_filepathname="/home/mitch/projects/wantbox.com/wantbox/zips/data/zipcodes.csv" 
# Full path to your django project directory 
your_djangoproject_home="/home/mitch/projects/wantbox.com/wantbox/" 
import sys,os 
sys.path.append(your_djangoproject_home) 
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
from salesaccounts import models

import csv dataReader = csv.reader(open(csv_filepathname), delimiter=',', quotechar='"') 
for row in dataReader: 
	# Ignore the header row, import everything else 
	serviceType = ServiceType() 
	serviceType.user_account = request.user
	serviceType.city = row[0] 
	serviceType.statecode = row[1] 
	serviceType.save()