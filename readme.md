# Generic Study Database

## Description  
This script was developed to support internal data mining of clinical study through limited means. Primarily it must read a data dump from clinical study management system and create a sql database based on the initial dump and insert data from that and subsequent dumps. There is no known glossary and data are not required to remain formatted consistently.  
  
This script and modules will perform the following:  
* Read data dump (flat, wide table) from clinical study management software.
* Create tables in disease database based on previous table.
* Insert available investigators, lab tests ...etc.
* Select from available timepoints as clinical study evolves.
* Insert actual data.  

