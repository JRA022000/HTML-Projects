 # Plant Manager
Video Demo:  https://youtu.be/YY-MSsY8IS0

Description:

This is a web application design to help me and my wife better manage our growing plant population. I choose this project because I find myself more interested
in web development than I ever expected and wanted to contine practicing with flask, jinja, html, and python for web development. Additionally, I really enjoy
working with databases and using SQLite, so I wanted to ensure that there was an opportunity to utilize a DB as well.

Upon startup, the browser opens an index page which provides an overview of all the plants currently in the database. The database stores 9 different attributes
for each plant which give significant data points to use for managing the care of the plants as well as searching the database for the plants. Each plant has
four text based attributes, including nickname, species, subspecies, and purchase source. Additionally, there are 5 datetime elements, which record the date
of purchase, the date of last watering, date of last fertilization, date of last checked for pests, and date of last application of pest management.

There are a number of additional pages also built into the application. There is a page for adding plants, updating care of plants, searching for plants, and
seeing if there are any plants which may need immeadiate care. Additionally, there is an apology page which can render in the event of an error.

The add plant page allows for adding a new plant by nickname, a drop down for species, an entry for subspecies, and place of purchase. Upon clicking the submit
button, an db command is executed to add the plant to the database. By default, the date of purchase, last watering date, last fertilization date, last pest check
date and last pest management date are defaulted to today as those efforts are usually completed the date of purchase.

The search page allows a user to search nickname, species via a drop down, subspecies, source, by checking if a plant was watered within a certain number of days,
and by checking if a plant was fertilized within a certain number of days. Additionally, the days watered and fertilized and be combined within any of the other
search fields. Upon clicking search, revelant results are updated to the page.

The Add care pages allows for the database to be updated for the fields of last watered, last fertilized, last checked for pests and last applied pest management.
The user picks from a plant currently in the database using the nickname and then can check boxes for each of the other fields. Upon clicking submit, the database
will be updated to reflect the current date for all of those fields.

The alerts page runs four seperate checks against the database to see if plants have been watered withn 7 days, checked for pests with 7 days, had pest management
applied within 8 weeks. There is a special condition which checks for fertilization with 7 days if in the growing season, and within 1 month if out of the growing
season. After the checks are run against the database, the plants which meet critrea for possibly needing care are displayed for the user.