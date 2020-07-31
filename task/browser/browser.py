from collections import deque
import os
import sys

from bs4 import BeautifulSoup
from colorama import init, Fore
import requests


# write your code here
r = None
current = ''
stack = deque()


def parse(html_page):
    soup = BeautifulSoup(html_page, 'html.parser')
    anchor_tags = soup.find_all('a')
    init()
    for anchor_tag in anchor_tags:
        anchor_tag.string = f"{Fore.BLUE}{anchor_tag.string}"
    tags = soup.select("h, p, ul, ol")
    return "\n".join([tag.get_text() for tag in tags])


def read_page(page_name):
    with open(page_name) as page_file:
        print(page_file.read())


def write_page(page_name, response):
    with open(page_name, 'w') as page_file:
        if response:
            parsed_response = parse(response.content)
            page_file.write(parsed_response)
            print(parsed_response)
        else:
            error = f"{response.status_code}\n{response.raise_for_status()}"
            page_file.write(error)
            print(error)


dir_path = sys.argv[1]
if not os.path.exists(dir_path):
    os.makedirs(dir_path)


while True:
    address = input()

    if address == 'exit':
        break

    if address == 'back' and len(stack) > 1:
        current = stack.pop()
    else:
        page_path = os.path.join(dir_path, address)
        if not os.path.exists(page_path):
            url_halves = address.rsplit('.', 1)
            if len(url_halves) != 2:
                print('error: not a valid url')
                continue

            url_head_halves = url_halves[0].split("://", 1)
            page_path = os.path.join(dir_path, url_head_halves[-1])
            r = requests.get(address if len(url_head_halves) == 2 else "https://" + address)

        stack.append(current)
        current = page_path

    read_page(current) if r is None else write_page(current, r)
