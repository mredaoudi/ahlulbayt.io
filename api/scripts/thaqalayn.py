import requests

all_books = requests.get("https://www.thaqalayn-api.net/api/v2/allbooks")

print(all_books.status_code)