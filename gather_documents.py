import requests
import csv
from bs4 import BeautifulSoup
from vardata import source_html


def gather_links_from_html(html):
  soup = BeautifulSoup(html, 'html.parser')
  links = soup.find_all('a')

  support_links = [link.get('href') for link in links]

  # add support links from other locales
  for locale in ['es', 'fr', 'de', 'zh-sg']:
    for link in links:
      link = link.get('href')
      link = link.replace('support.procore.com',
                          locale + '.support.procore.com')
      support_links.append(link)

  return support_links


def get_title_and_content(url):
  response = requests.get(url)
  soup = BeautifulSoup(response.text, 'html.parser')
  title = soup.find_all('h1', id='title')[0].text.strip()
  content = soup.find(class_='mt-content-container').text.strip()

  return {'title': title, 'content': content, 'url': url}


def get_all_titles_and_content(links):
  results = []
  for link in links:
    print("Link " + str(len(results) + 1) + "/" + str(len(links)))
    results.append(get_title_and_content(link))

  return results


def gather(filename):
  # Gather links
  print('Gathering links...')
  links = gather_links_from_html(source_html)

  ## Gather titles and content
  print('Gathering titles and content...')
  titles_and_content = get_all_titles_and_content(links)

  # Load the content of titles_and_content into a CSV with headers
  print('Writing CSV...')
  with open(filename, 'w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['title', 'content', 'url'])
    for title_and_content in titles_and_content:
      writer.writerow([
        title_and_content['title'], title_and_content['content'],
        title_and_content['url']
      ])
