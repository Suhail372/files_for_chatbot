
from dataclasses import dataclass, asdict, field
import pandas as pd
import argparse
import os
import sys
from bs4 import BeautifulSoup
import requests
import csv
import json


@dataclass
class Business:
    """holds business data"""

    name: str = None
    address: str = None
    website: str = None
    phone_number: str = None


def extract_names_and_addresses():
    # Read the CSV file

    file_name = 'google_maps_data_Schools_in_Ameerpet_Hyderabad.csv'
    df = pd.read_csv(file_name)

    # Extract names and addresses as lists
    names = df['name'].tolist()
    addresses = df['address'].tolist()

    return names, addresses
def get_response(url):
    try:
        response = requests.get(url, allow_redirects=True)
        response.raise_for_status()  # Raise an exception for 4xx and 5xx status codes
        return response
    except requests.exceptions.Timeout:
        print(f"Timeout error: {url}")
    except requests.exceptions.TooManyRedirects:
        print(f"Too many redirects: {url}")
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
    return None


def getlinks(url):

    # Fetch the HTML content of the website
    response = requests.get(url)

    # Check if the request was successful
    if response and response.status_code == 200:
        # Parse the HTML content
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find all h3 elements with class 'card-title'
        card_titles = soup.find_all('h3', class_='card-title')

        # Extract hrefs from the links within each h3 element
        hrefs = [title.find('a')['href'] for title in card_titles]
        names = [name.text.strip() for name in card_titles]

        return hrefs, names
    else:
        print("Failed to fetch page:", url)
        return []


def navigate_all_pages(baseurl):
    all_hrefs = []
    all_names = []
    page_number = 1

    while True:
        page_url = f"{baseurl}?page={page_number}"
        hrefs, names = getlinks(page_url)

        # If no hrefs found, it might indicate end of pagination
        if not hrefs:
            break

        all_hrefs.extend(hrefs)
        all_names.extend(names)
        page_number += 1

    return all_hrefs, all_names

def extract_substring(text):
    # Find the index of the colon
    colon_index = text.find(":")

    # If colon is found, extract substring from index after colon to end of string
    if colon_index != -1:
        substring = text[colon_index + 3:].strip()
        cleaned_text = substring.replace("\r", "").replace("\n", "")

        return cleaned_text
    else:
        return None

def extract_data(url, name):
    
    def extract_telephone(soup):
        tel_badge_urls=[]
        tel_badge_urls = soup.find_all('a', href=lambda href: href and "tel:" in href)
        if tel_badge_urls:
            return tel_badge_urls[1]['href']
        else:
            return "Telephone number not found"

    def extract_card_data(soup):
        card_data = {}
        specified_ids = ["fee", "location", "faculty", "sports", "amenities"]
        divs = soup.find_all('div', class_='card')
        for id in specified_ids:
            div = soup.find('div', id=id)
            if div:
                # Capitalize the card ID
                card_id = id.capitalize()
                if card_id == "Amenities":
                    # Extract text from <i> tags with class "fa fa-check"
                    amenities_text = [item.next_sibling.strip() for item in div.find_all('i', class_='fa fa-check')]
                    card_data[card_id] = ', '.join(amenities_text)
                else:
                    card_text = [item.text.strip() for item in div.find_all('p')]
                    if card_id == "Faculty":
                        faculty_text = ' '.join(card_text)
                        faculty_text = ' '.join(faculty_text.split())  # Remove consecutive white spaces
                        card_data[card_id] = faculty_text
                    else:
                        card_data[card_id] = ', '.join(card_text)
            else:
                # Add the ID with a value of None if it's not present in the HTML
                card_data[id.capitalize()] = None
        card_data["Location"] = card_data["Location"].replace("Andhra Pradesh", "Telangana")
        return card_data

    def extract_ul_data(soup):
        ul_data = []
        ul = soup.find('ul', class_="displayBlock")
        li_elements = ul.find_all('li')
        for li in li_elements:
            br_ting = li.find('b')
            if br_ting:
                if ":" in br_ting.text.strip():
                    ul_data.append(extract_substring(br_ting.text.strip()))
                else:
                    ul_data.append(br_ting.text.strip())
            else:
                if ":" in li.text.strip():
                    ul_data.append(extract_substring(li.text.strip()))
                else:
                    ul_data.append(li.text.strip())
        return ul_data

    response = requests.get(url, allow_redirects=True)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract data from <ul> elements
        ul_data = extract_ul_data(soup)

        # Extract data from specific cards
        card_data = extract_card_data(soup)

        # Extract telephone number
        telephone_number = extract_telephone(soup)

        # Save to JSON
        json_data = {
            "Name": name,
            "Since": ul_data[0],
            "Category": ul_data[1],
            "Strength": ul_data[2],
            "Years": ul_data[3],
            "Board": ul_data[4],
            "Phone No": telephone_number,
            **card_data,  # Include card data in JSON
             # Include ul_data in JSON
        }

        # Save to CSV
        csv_data = [name] + ul_data[:5] + [telephone_number] + list(card_data.values())

        print("JSON data:", json_data)

        return json_data, csv_data
    else:
        print("Failed to fetch page:", url)
        return None



def main():
    
    base = "https://yellowslate.com/schools/hyderabad/gachibowli"
    links, names = navigate_all_pages(base)
    all_data_json = []
    all_data_csv=[]
    print("DOne this")
    c=0
    for link, name in zip(links, names):
        c+=1
        try:
            json_data,csv_data = extract_data(link, name)
        except:
            print(c)
        if json_data:
            all_data_json.append(json_data)
        if csv_data:
            all_data_csv.append(csv_data)

    # Save all data to JSON file
    with open("all_schools_data_miyapur.json", "w") as json_file:
        json.dump(all_data_json, json_file, indent=4)

    # Save all data to CSV file
    with open("all_schools_data_miyapur.csv", "w", newline="") as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(["Name", "Since", "Category", "Strength", "Years", "Board","Phone No", "Fee", "Location", "Faculty", "Sports", "Amenities"])
        c=0
        for data in all_data_csv:
            c+=1
            try:
                csv_writer.writerow(data)
            except:
                print(c)

    print("All data saved successfully.")

if "__main__":
    main()
