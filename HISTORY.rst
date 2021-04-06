=======
History
=======

0.10.0 (2021-04-06)
-------------------

* ListResponses now behave like lists
* Changed how api routes are processed
    * In the old versions the objector has a map of all routes that are available and how the may back to objects
    * Now each model declares the routes by itself and which object will be returned
    * In this release the old map, and the old methods are still present, they will be removed in a future release
* Changed the timesheet endpoint of the invoice model to timesheet_pdf for clearer distinction between timesheet_pdf and the new method timesheet_activities
* Renamed HourlyRates model to AccountHourlyRates
* Added verify method to Session model
* Implemented AccountInternalHourlyRates model
* Added getall method to ProjectPaymentSchedule model
* Added more optional parameters to other methods


0.9.0 (2020-12-24)
-------------------

* Reworked response classes
    * Split ListingResponse into 2 separate classes
    * ListResponse for unpaged response data
    * PageListResponse for paginated response data
    * Renamed JsonResponse to ObjectResponse
* Implemented taggings endpoint
* Added *clickup* remote service
* Cleaned up tests

0.8.1 (2020-11-17)
------------------

* Removed Project from Schedules (only used for Absences)
* Cleanup tests
* Added deal parameter to project create and update
* Implemented invoice send_email endpoint
* Implemented hourly rates endpoint


0.8.0 (2020-06-28)
------------------

* New Readme
* Add return types to documentation (for default configuration of moco instance only)
* Implement Purchase model
* Allow overwrite of http headers from model classes
* Fix some typos in method names (offer item generator) and parameter (user holidays)


0.7.2 (2020-06-05)
------------------

* Implement update_status endpoint of offer model

0.7.1 (2020-05-30)
------------------

* Create new Releases with bumpversion
* Implemented tags parameter in invoice creation

0.7.0 (2020-05-27)
------------------

* Implemented Planning Entries
* Add credit/debit number to Company
* Add footer to Company
* Add deal property to Project objector model

0.6.3 (2020-04-29)
------------------

* Cleanup
* Fixed example code in documentation
* Fixed various typos
* Implemented contact lookup by phone number and term

0.6.2 (2020-03-24)
------------------

* Query strings conversion into lower case

0.6.1 (2020-03-18)
------------------

* Implement support for days parameter in User holidays
* Implement Purchase Categories

0.6.0 (2020-03-07)
------------------

* Implemented Paging of Listing Models
* Implemented the creation of fixed price projects
* Implement Project Payment Schedules for fixed price projects
* More Documentation and even more code cleanup

0.5.0 (2020-02-29)
------------------

* Implement authentication via email and password (note that the class constructor also changed, if you do not want that continue to ues the previus version (0.4.1))
* Create readthedocs documentation (see https://moco-wrapper.readthedocs.io)
* Error Responses are now converted into actual Exceptions that are raised
* Code Cleanup

0.4.1 (2020-02-24)
------------------

* Implemented impersonation
* Fixed makefile (make test does work now if you have the required packages installed)
* Created documentation see (https://moco-wrapper.readthedocs.io/en/latest/)
* Added named arguments requestor and objector to moco_instance constructor (Setting the requestor via moco.http is no longer possible, user moco.requestor)
* Removed cli component


0.4.0 (2020-02-19)
------------------

* Finished reworking all the integration tests
* Prefixed Employment, Holiday and Presense with "User" for clarification
* Moved duplicated methods id_generator and create_random date into base class
* Implented additional requestor that only tries once to request the api endpoint (no retrying)
* Main moco object moved to namespace moco_wrapper.moco
* Changed author email


0.3.0 (2020-02-17)
------------------

* Create github workflow to automaticly deploy to PyPI
* Implement an objector to control how the json responses get converted back into python objects (some endpoints return data that contain reserved python keywords, this was implemented to circumvent that)
* More Tests and more type hinting
* Write the history of the last versions
* Change the order of things in this history file
* Implement offer creation

0.2.3 (2020-02-09)
------------------

* Implement FileResponses for downloading pdf files from api
* Implement invoice class api changes
* More tests

0.2.2 (2020-01-12)
------------------

* Start implementing type hinting
* Switch to support python3 only
* Remove company delete method, as it is not support by the api
* More Tests

0.2.1 (2020-01-10)
------------------

* More tests

0.1.0 (2019-09-04)
------------------

* First release on PyPI.
