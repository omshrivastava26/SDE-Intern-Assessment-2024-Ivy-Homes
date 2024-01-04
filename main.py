#! /usr/bin/env python3

import pickle, json
from datetime import date
from colorama import Fore, Back
from optparse import OptionParser
from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep, time, strftime, localtime

def get_arguments(*args):
    parser = OptionParser()
    for arg in args:
        parser.add_option(arg[0], arg[1], dest=arg[2], help=arg[3])
    return parser.parse_args()[0]

movies = 20
review_count = 10

class IMDb:
    genre_link = "https://www.imdb.com/search/title/"
    genre_parameter = "genres"
    review_link = "reviews"
    review_filter_prefix = "?sort=submissionDate&dir=desc&ratingFilter=0"
    top_offset = 100
    sleep_duration = 0.5
    def __init__(self):
        self.browser = webdriver.Firefox()
    def getGenres(self):
        self.browser.get(IMDb.genre_link)
        genre_tag = [tag for tag in self.browser.find_elements(By.TAG_NAME, "span") if tag.get_attribute("class") == "ipc-accordion__item__title" and tag.text.strip() == "Genre"][0]
        self.browser.execute_script(f"window.scrollTo(0,{genre_tag.location['y']-IMDb.top_offset});")
        sleep(IMDb.sleep_duration)
        genre_tag.click()
        return [tag.text.strip() for tag in genre_tag.find_element(By.XPATH, "..").find_element(By.XPATH, "..").find_element(By.XPATH, "..").find_elements(By.TAG_NAME, "button")]
    def getTopMovies(self, genre, movies):
        self.browser.get(f"{IMDb.genre_link}?{IMDb.genre_parameter}={genre}")
        movie_headings = [tag for tag in self.browser.find_elements(By.TAG_NAME, "h3") if tag.get_attribute("class") == "ipc-title__text"]
        movie_rankings = {int(tag.text.strip().split('. ')[0]): [tag.text.strip().split('. ')[1], tag.find_element(By.XPATH, "..").get_attribute("href").split('?')[0]] for tag in movie_headings if '.' in tag.text}
        return [movie_rankings[rank] for rank in range(1, movies+1)]
    def getLatestReview(self, movie, reviews):
        self.browser.get(f"{movie}{IMDb.review_link}{IMDb.review_filter_prefix}")
        review_title_tags = [tag for tag in self.browser.find_elements(By.TAG_NAME, 'a') if tag.get_attribute("class") == "title"][:reviews]
        reviews = []
        for review_title_tag in review_title_tags:
            review = {}
            review_tag = review_title_tag.find_element(By.XPATH, "..")
            try:
                review["Rating"] = int([tag for tag in review_tag.find_elements(By.TAG_NAME, "div") if tag.get_attribute("class") == "ipl-ratings-bar"][0].text.strip('/')[0])
            except:
                review["Rating"] = '-'
            review["By"] = [tag for tag in review_tag.find_elements(By.TAG_NAME, "span") if tag.get_attribute("class") == "display-name-link"][0].text
            review["Date"] = [tag for tag in review_tag.find_elements(By.TAG_NAME, "span") if tag.get_attribute("class") == "review-date"][0].text
            if len([tag for tag in review_tag.find_elements(By.TAG_NAME, "span") if tag.get_attribute("class") == "spoiler-warning"]) > 0:
                show_spoiler_content_tag = [tag for tag in review_tag.find_elements(By.TAG_NAME, "div") if tag.get_attribute("class") == "expander-icon-wrapper spoiler-warning__control"][0]
                self.browser.execute_script(f"window.scrollTo(0,{show_spoiler_content_tag.location['y']-IMDb.top_offset});")
                sleep(IMDb.sleep_duration)
                show_spoiler_content_tag.click()
                review["Spoiler"] = True
            else:
                review["Spoiler"] = False
            review["Review"] = [tag for tag in review_tag.find_elements(By.TAG_NAME, "div") if tag.get_attribute("class") == "content"][0].text
            try:
                review["Useful Upvotes"] = [tag for tag in review_tag.find_elements(By.TAG_NAME, "div") if tag.get_attribute("class") == "actions text-muted"][0].text.split(' ')[0]
                review["Total Upvotes"] = [tag for tag in review_tag.find_elements(By.TAG_NAME, "div") if tag.get_attribute("class") == "actions text-muted"][0].text.split(' ')[3]
            except:
                review["Useful Upvotes"] = [tag for tag in review_tag.find_element(By.XPATH, "..").find_element(By.XPATH, "..").find_elements(By.TAG_NAME, "div") if tag.get_attribute("class") == "actions text-muted"][0].text.split(' ')[0]
                review["Total Upvotes"] = [tag for tag in review_tag.find_element(By.XPATH, "..").find_element(By.XPATH, "..").find_elements(By.TAG_NAME, "div") if tag.get_attribute("class") == "actions text-muted"][0].text.split(' ')[3]
            reviews.append(review)
        return reviews
    def close(self):
        self.browser.quit()

if __name__ == "__main__":
    arguments = get_arguments(('-w', "--write", "write", "Name of the File for the Data to be Dumped (Default=Current Date and Time)"),
                              ('-f', "--format", "format", "Format for the file to be saved to (CSV, JSON, PICKLE)"),
                              ('-m', "--movies", "movies", f"Number of Top Movies to scrap from each Genres (1-50, Default={movies})"),
                              ('-r', "--reviews", "reviews", f"Number of Recent Reviews to scrap from each Movie (1-25, Default={review_count})"))
    if not arguments.write:
        arguments.write = f"{date.today()} {strftime('%H_%M_%S', localtime())}"
    if not arguments.format or arguments.format.lower() not in ["csv", "json", "pickle"]:
        arguments.format = "pickle"
        print("Dump File Format = PICKLE")
    else:
        arguments.format = arguments.format.lower()
    if arguments.movies:
        movies = int(arguments.movies)
    if arguments.reviews:
        review_count = int(arguments.reviews)
    if movies > 50:
        print(f"{Fore.YELLOW}[*] Scrapping TOP 50 Movies from each Genre")
        movies = 50
    if review_count > 25:
        print(f"{Fore.YELLOW}[*] Scrapping Top 25 Recent Reviews from each Movie")
        review_count = 25
    scrapper = IMDb()
    print(f"[+] Getting Genres")
    t1 = time()
    genres = scrapper.getGenres()
    t2 = time()
    print(Fore.CYAN)
    print('\n'.join(genres))
    print(Fore.RESET)
    print(f"[:] Done in {t2-t1:.2f} seconds")
    data = {}
    for genre in genres:
        data[genre] = []
        print(f"\n[+] Current Genre = {Fore.CYAN}{genre}{Fore.RESET}")
        t1 = time()
        top_movies = scrapper.getTopMovies(genre, movies)
        t2 = time()
        print(Fore.GREEN)
        print('\n'.join([f"\t{index+1}. {top_movies[index][0]}" for index in range(len(top_movies))]))
        print(Fore.RESET)
        print(f"[:] Time Taken = {t2-t1:.2f} seconds")
        T1 = time()
        for movie in top_movies:
            movie_data = {}
            movie_data["Name"] = movie[0]
            movie_data["Link"] = movie[1]
            print(f"\n[+] Getting Review for Movie {movie[0]}")
            t1 = time()
            reviews = scrapper.getLatestReview(movie[1], review_count)
            for review in reviews:
                print('\n'.join(f"{Fore.GREEN}{key}{Fore.WHITE}: {Fore.CYAN}{value}{Fore.RESET}" for key, value in review.items()))
                print()
            movie_data["Reviews"] = reviews
            t2 = time()
            data[genre].append(movie_data)
            print(f"[:] Time Taken = {t2-t1:.2f} seconds")
        T2 = time()
        print(f"[:] Total Time Taken to scrap TOP {review_count} Recent Reviews from movie {movie[0]} = {T2-T1:.2f} seconds")
    print(f"[:] Closing the Browser")
    scrapper.close()
    print(f"[+] Closed the Browser")
    print(f"\n[:] Dumping Data to File {arguments.write}")
    if arguments.format == "pickle":
        with open(arguments.write, 'wb') as file:
            pickle.dump(data, file)
    else:
        with open(arguments.write, 'w') as file:
            if arguments.format == "csv":
                file.write("Genres")
                file.write('\n'.join([f"{index},{genre}" for index, genre in enumerate(genres)]))
                for genre, top_movies in data.items():
                    file.write('\n\n')
                    file.write(genre)
                    file.write('\n')
                    for index, movie in enumerate(top_movies):
                        file.write(f"Movie,{movie['Name']}\n")
                        file.write(f"Link,{movie['Link']}\n")
                        file.write("Reviews\n")
                        for review in movie["Reviews"]:
                            file.write('\n'.join([f"{key},{value}" for key, value in review.items()]))
                        file.write('\n')
            else:
                json.dump(data, file)
    print(f"[+] Dumped Data to File {arguments.write}")