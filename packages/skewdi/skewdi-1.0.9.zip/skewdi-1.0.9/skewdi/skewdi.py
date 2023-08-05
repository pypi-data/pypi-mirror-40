import requests, bs4

def validateUrl(url):
    import re
    regex = re.compile(
        r'^https?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return url is not None and regex.search(url)


def fetchAnchor(website):

	links = []

	if validateUrl(website):

		domain = ""

		if website[-1] == "/":
			domain = website[:-1]
		else:
			domain = website

		try:

			r = requests.get(website)

		except:

			return links.append("Error in Fetching Website")

		soup = bs4.BeautifulSoup(r.text, "html.parser")

		elem = soup.findAll('a')

		for link in elem:
			
			if link.has_attr('href'):
				if "http" not in link['href']:
					links.append(domain + "/" +  link.get('href'))
				else:
					links.append(link['href'])
	else:
		links.append("Bad URL")

	return links

def fetchPara(website):
	links = []

	if validateUrl(website):

		try:

			r = requests.get(website)
		except:
			links.append("Error in Fetching Website")

		soup = bs4.BeautifulSoup(r.text, "html.parser")

		elem = soup.findAll('p')

		for link in elem:
			links.append(link.get_text())

	else:
		links.append("Bad URL")

	return links

def author():
	return "Samprit Sarkar\n(sam123)"