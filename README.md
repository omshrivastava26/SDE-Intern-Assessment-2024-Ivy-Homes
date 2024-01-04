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