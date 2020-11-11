"""
This script is a crawler for the website "lawyers.findlaw.com".

It creates a file named results.txt which includes all the immigration lawyer firms in the USA
"""


from bs4 import BeautifulSoup
import requests
from requests.exceptions import MissingSchema

from lawyer import Lawyer

TEST_MODE = 1       # 1 for testing, 0 otherwise

url_all_states = "https://lawyers.findlaw.com/lawyer/practice/immigration-naturalization-law"
url_state = "https://lawyers.findlaw.com/lawyer/practicestateallcities/immigration-naturalization-law/"
url_city = "https://lawyers.findlaw.com/lawyer/firm/immigration-naturalization-law/"


def get_text_from_url(url, lawyer):
    """
    A function that returns the text retrieved from a specific url
    :param url:
    :return: text
    """
    try:
        html_doc = requests.get(url).content
    except MissingSchema:
        report_error(lawyer)
        return ""

    soup = BeautifulSoup(html_doc, 'html.parser')
    return soup.get_text()


def get_states(txt):
    """
    Reads the text as crawled from the webpage https://lawyers.findlaw.com/lawyer/practice/immigration-naturalization-law
    and returns all the states found
    :param txt:
    :return: a list with the states with lawyers
    """
    states = txt.split("Immigration Lawyers By State")[1]
    states = states.split("What Are The Requirements For U.S. Citizenship?")[0]
    states = states.split("\n")
    # filter removes empty states
    return list(filter(None, states))


def get_cities(txt):
    """
    Reads the text as crawled from the webpage of a specific state.
     path: /practicestateallcities/immigration-naturalization-law/<specific_state>
    and returns all the cities found

    :param txt:
    :return: a list with the cities scraped from the specific state
    """
    cities = txt.split("cities, listed alphabetically:")[1]
    cities = cities.split("What are the requirements for U.S. citizenship?")[0]
    cities = cities.split("\n")
    # filter removes empty cities
    return list(filter(None, cities))


def get_firms_details(firm_url, state, city):
    """
    Given the details of each lawyer firm included in the given url

    :param firm_url:
    :param state:
    :param city:
    :return: a list of objects of the class Lawyer
    """
    html_doc = requests.get(firm_url).content
    soup = BeautifulSoup(html_doc, 'html.parser')
    #res = soup.find_all("h2", class_="listing-details-header")
    firms = soup.find_all(id="standard_results")
    firms = str(firms).split('<h2 class="listing-details-header">')
    firms = firms[1:]
    lawyers = []    # list of objects
    for firm in firms:
        # create an object in class Lawyer
        lawyer = Lawyer()
        lawyer.state = state
        lawyer.city = city
        name = firm.split("</h2>", 1)
        lawyer.company_name = name[0]

        prof_url = firm.split('class="listing-desc-phone directory_profile" href="')[1].split('"', 1)
        lawyer.profile_url = prof_url[0]
        try:
            lawyer.website = firm.split('<a class="listing-desc-phone directory_website" href="')[1].split('"', 1)[0]
        except IndexError:
            lawyer.website = ""

        try:
            lawyer.phone = get_text_from_url(lawyer.profile_url, lawyer).split('"telephone": "', 1)[1].split('"', 1)[0]
        except:
            lawyer.phone = ""

        lawyers.append(lawyer)

    return lawyers


def report_error(lawyer):
    with open("error.txt", "a+") as f:
        f.write("\n----------------------------------\n")
        f.write(lawyer)



def main():
    text = get_text_from_url(url_all_states)
    states = get_states(text)

    # for each state retrieve the cities
    max_states = 3              # TESTING   ###############################
    for state in states:
        # convert state to acceptable format
        state = state.lower()
        state = "-".join(state.split(" "))

        new_url = url_state + state
        text = get_text_from_url(new_url)
        cities = get_cities(text)

        # for each city in the state
        max_cities = 5          # TESTING   ###############################
        for city in cities:

            # convert city to acceptable format
            city = city.lower()
            city = "-".join(city.split(" "))

            new_url_city = url_city + city + "/" + state
            print("results for state; {} and city: {}".format(state, city))
            for firm in get_firms_details(new_url_city, state, city):
                with open("results.txt", "a+") as f:
                    f.write("\n----------------------------------\n")
                    f.write(str(firm))
                print("----------------------------------")
                print(firm)

            ###################### FOR TESTING ONLY.....to be removed
            max_cities -= 1
            if max_cities == 0:
                break

        ###################### FOR TESTING ONLY.....to be removed
        max_states -= 1
        if max_states == 0:
            break



    # with open("temp.txt", "w") as f:
    #     f.write(states)


if __name__ == "__main__":
    main()

