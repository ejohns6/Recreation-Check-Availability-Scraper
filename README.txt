A webscraper for Assateague Island National Seashore Campground via the Recreation website

V 1.0

Installation:
-Need python 3
-Need packages:
	-csv
	-beatifulsoup4
	-selenium

To Change for any website this line:

url = 'https://www.recreation.gov/camping/campgrounds/232507/availability'

You will also need to change the range(6) on line 44 if you change it for another website

Currently need to change range(12) to change the time which currently does about 1 month in 3 days

To-Do:
-URL to be entered either with argument line or input
-Will Change so that this does not need to be done
-Will Change so that this can be changed on the argument line or input
-User input on which place to look for a specific camp site
-Error for walkin. Due to it changes format after the first 10 days