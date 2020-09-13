###############################
# Run this file as follows:	  #
# python synonym.py input.txt #
###############################


from typing import Set, Optional, List
from nltk.corpus.reader import Synset
from nltk.corpus import wordnet as wn
import itertools
import requests
from bs4 import BeautifulSoup
import argparse
    

def read_file (file):
	make_syn = []
	for i in file:
		make_syn.append(i.rstrip())
	return make_syn


def synonyms(word):
    return_set=[]
    word_set = wn.synsets(word)
    for word in word_set:
    	for j in word.lemmas():
    		return_set.append(j.name()) 
    return return_set

def synonyms2 (word):
	response = requests.get('http://www.thesaurus.com/browse/{}'.format(word))
	soup = BeautifulSoup(response.text, 'lxml')
	print(soup.prettify())
	section = soup.find_all("a", class_="css-1xupnfh e1m1tvmx7") 
	# This is the tag for moderately relevant synonyms
	section = section + soup.find_all("a", class_="css-1vs6pqb etbu2a31")
	print(section)
	return_set = [i.text for i in section]
	return return_set


if __name__ == '__main__':
	# Crashes at 0 probably
	parser = argparse.ArgumentParser()
	parser.add_argument("input", help = "name of file with words")
	parser.add_argument("level", help = "number of layers deep to search the word")
	args = parser.parse_args()

	level = int(args.level)
	make_syn = [args.input]
	# f = open(args.input)
	# make_syn = read_file (f)
	for i in make_syn:
		words = [i]
		words2 = words.copy()
		while(level!= 0):
			level-=1
			for i in words:
				print(i)
				# temp = list(set(synonyms2(i) + synonyms(i)))
				temp = list(set(synonyms2(i)))
				for j in temp:
					words2.append(j)
			words = list(set(words2))
	words.sort()
	for i in words:
		print("\"%s\"," %i)