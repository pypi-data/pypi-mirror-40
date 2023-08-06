import requests
import duckpy
from bs4 import BeautifulSoup

def letra(query):
	tr = 'a'
	query = query.replace('www.letras','m.letras')
	r = requests.get(query)
	soup = BeautifulSoup(r.text, "html.parser")
	a = soup.find('div',"lyric-cnt g-1")
	if a == None:
		a = soup.find('div',"lyric-tra_l")
		tr = soup.find('div',"lyric-tra_r")
	b = ''
	for i in a.find_all('p'):
		b += str(i).replace('<br/>','\n').replace('<p>','\n\n').replace('</p>','').replace('<span>','').replace('</span>','')
	b = b[2:]
	c = soup.find("div","lyric-title g-1")
	musica = c.find('h1').get_text()
	autor = c.find('a').get_text()
	ret = {'autor':autor,'musica':musica,'letra':b.replace('\n\n\n','\n\n'),'link':r.url}
	if 'a' not in tr:
		b = ''
		for i in tr.find_all('p'):
			b += str(i).replace('<br/>','\n').replace('<p>','\n\n').replace('</p>','').replace('<span>','').replace('</span>','')
		b = b[2:]
		ret['traducao'] = b.replace('\n\n\n','\n\n')
	return ret
def search(query):
	a = duckpy.search(query+' letras.mus')['results']
	results = []
	for i in a:
		if 'letras.mus' in i['url']:
			results.append(i['url'])
	return results
def auto(query):
	a = search(query)
	return letra(a[0])