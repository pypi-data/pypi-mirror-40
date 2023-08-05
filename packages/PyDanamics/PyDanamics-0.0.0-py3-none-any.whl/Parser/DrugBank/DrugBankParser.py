import re
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from bs4 import BeautifulSoup


def download(url, file_name):
    # open in binary mode
    with open(file_name, "wb") as file:
        # get request
        response = requests.get(url)
        # write to file
        file.write(response.content)

URL = "https://www.drugbank.ca/structures/small_molecule_drugs/DB08916.sdf"

download(URL, "file_name.sdf")