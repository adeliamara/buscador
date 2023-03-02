from bs4 import BeautifulSoup
import requests

response = requests.get('http://www.ifpi.edu.br/')
print(response.status)