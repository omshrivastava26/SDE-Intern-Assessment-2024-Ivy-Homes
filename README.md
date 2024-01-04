# SDE-Intern-Assessment-2024-Ivy-Homes
Considerations and Assumptions:
Web Scraping: The code relies on web scraping techniques, which are subject to changes in the IMDb website's structure. Any modifications to the website might break the script, requiring updates.

Browser Compatibility: The script uses the Firefox webdriver for Selenium. Ensure that the appropriate version of the Firefox browser and the geckodriver executable are installed.

Sleep Duration: The sleep_duration variable is used to introduce delays during web interactions. The optimal value may vary based on network conditions, and the script assumes a reasonable delay for elements to load.

Data Structure: The script structures the scraped data into a dictionary, with genres as keys and a list of movie details as values. The script also includes movie reviews as a nested list within the movie details.

File Dumping: The script allows the user to specify the output file name, format (CSV, JSON, or PICKLE), number of top movies, and number of reviews. The script assumes default values if not provided.

User Input Handling: The script uses the OptionParser module for handling command-line arguments. It assumes that users will provide appropriate inputs and provides default values if some options are not specified.
