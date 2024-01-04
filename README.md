# IMDb-Scrapper
A Python Program that scraps IMDb's top 20 Movies from each Genre and their Latest 10 User Reviews.

## Requirements
Programming Language = Python3<br />
Modules/Packages Used:
* pickle (for dumping the data)
* json (for dumping the data)
* datetime (for saving the dumped data with current date and time if no file name specified)
* colorama (highlighting different texts on screen with different colors)
* optparse (to get the command line arguments)
* selenium (to scrap the data)
* time (for saving the dumped data with current date and time if no file name specified and delays)
<!-- -->
Go to [Mozilla's Firefox Driver for Selenium](https://github.com/mozilla/geckodriver/releases) and download *geckodriver* for your system and put it in a path that is included in your **PATH** environment variable.

## Data Structure
During the execution, the data scrapped from IMDb's Website is stored in *data* variable.<br />
It is a dictionary, whose *keys* are **Genres** and *values* are **lists of Movie Data**.<br />
And the Movie Data is Further a Dictionary, with *keys* **Name**, **Link** and **Reviews**.<br />
**Name** and **Link** have *strings* as *values*. But **Reivews** are lists of Dictionary.<br />
This dictionary consists data like *Rating*, *By*, *Date*, *Content* and *Upvotes*
##Summary 
Considerations and Assumptions:
Web Scraping: The code relies on web scraping techniques, which are subject to changes in the IMDb website's structure. Any modifications to the website might break the script, requiring updates.

Browser Compatibility: The script uses the Firefox web driver for Selenium. Ensure that the appropriate version of the Firefox browser and the gecko driver executable are installed.

Sleep Duration: The sleep_duration variable is used to introduce delays during web interactions. The optimal value may vary based on network conditions, and the script assumes a reasonable delay for elements to load.

Data Structure: The script structures the scraped data into a dictionary, with genres as keys and a list of movie details as values. The script also includes movie reviews as a nested list within the movie details.

File Dumping: The script allows the user to specify the output file name, format (CSV, JSON, or PICKLE), number of top movies, and number of reviews. The script assumes default values if not provided.

User Input Handling: The script uses the OptionParser module for handling command-line arguments. It assumes that users will provide appropriate inputs and provides default values if some options are not specified.
