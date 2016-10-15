0.6 - 15th October 2016
-----------------------
Release with latest tweaks ready for forking of project

0.4c - 8th January 2016
---
Remove the 'address' property from address objects in the 'addresses' array.

0.4b - 7th January 2016
---
Fixed typo on 'postalCode' field name.

0.4a - 2nd January 2016
---
Fixed up Procfile for Heroku deployment following refactoring.

0.4 - 2nd January 2016
---
This release is a significant refactor of the code and brings a more tidy API and landing page.

#### Web Site
* Updated landing page, added 'TryIt' page, added simple documentation and guidance for API
* Refactor web site code to be a Flask blueprint [(http://flask.pocoo.org/docs/0.10/blueprints/)](http://flask.pocoo.org/docs/0.10/blueprints/)

#### Core API
* Added all remaining ODS data items to data returned by the API
* Moved all resource endpoints to sit under /api route
* Added CORS support on all /api routes
* Added proper filtering on organisation name using the 'q=' query parameter (and deprecated /organisations/search route)
* Added X-Total-Count for total filtered results returned via /organisations route (to assist with pagination of results)
* Added /api and /api/info routes for additional information about resources and ODS metadata

#### Database
* Significant updates to the import tool which now uses SQLAlchemy to create the database and import the data
* Removed deprecated SQL scripts (due to use of SQLAlchemy in import)

#### Documentation
* Updated docs to reflect new data import method


0.3 - 10th November 2015
---
* Added remaining metadata for roles and relationships
* Added a simple landing page for users arriving at the site
* Added fake /organisations/<ods_code>/endpoints route to demonstrate endpoint repository functionality

0.2 - 6th November 2015
---
* Updated docs to try and help people get started / contribute to the project
* Added some parameters to some routes
* Slightly improved HATEOAS compliance


0.1 - 5th November 2015
---
Initial release of prototype API containing following features:

* View Basic API Documentation
* Search For Organisation By Name
* Get Specific Organisation By ODS Code
* Get List Of Roles
* Basic HATEOAS compliance