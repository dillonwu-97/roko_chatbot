######################################################################
# Extracts tables from wikipedia
# Usage: 
# python wiki_table_extractor.py url output_txt
# E.g. horror video games list: 
# python wiki_table_extractor.py https://en.wikipedia.org/wiki/List_of_horror_video_games out.txt
# PLEASE NOTE:
# THE FORMATTING OF DIFFERENT WIKIPEDIA PAGES CAN BE SLIGHTLY DIFFERENT. 
# THE DEFAULT HEADER FORMATTING IN THIS SCRIPT IS TH, BUT PLEASE FEEL FREE TO TRY SOMETHING ELSE
######################################################################
from bs4 import BeautifulSoup
import argparse
import requests

# header Options: th, td
def make_tables(input, header='th', wikiclass = 'wikitable sortable'):
	url = requests.get(input).text
	soup = BeautifulSoup(url, 'html.parser')
	# soup = BeautifulSoup(url, 'lxml')
	# print(soup.prettify())
	# table = soup.find('table',{'class':'wikitable sortable'})
	# table = soup.find('table',{'class':'wikitable'})
	titles = []
	table = soup.find('table',{'class': wikiclass })
	test = soup.find_all('table', {'class':wikiclass})
	if wikiclass=='wikitable':
		for i in test:
			for j in i.find_all('tr'):
				tds=j.find_all(header)
				for td in tds[:1]:
					try:
						txt = td.text.strip()
						if txt!='Game':
							titles.append(txt)
					except:
						continue
	else:
	# print(table.prettify())
		for tr in table.find_all('tr'):
			# tds = tr.find_all('td')
			tds = tr.find_all(header)
			# print(tr)
			# temp = list(tds)
			for td in tds[:1]:
				titles.append(td.text.strip())
	return titles
	
def title_gen(url, name):
	titles = make_tables(url, wikiclass=name)
	if len(titles) < 2:
		titles = make_tables(url, 'td', name)
	return titles

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument("url", help = "url to extract tables from")
	parser.add_argument("output", help = "output txt file")
	args = parser.parse_args()

	try:
		titles = title_gen(args.url, 'wikitable sortable')
	except:
		titles = title_gen(args.url, 'wikitable')
	
	print(titles)
	with open(args.output, 'w+') as out:
		for title in titles:
			if '[' in title:
				try:
					title, junk = title.split('[')
				except:
					title = title
			out.write(title + '\n')


if __name__ == '__main__':
	main()
