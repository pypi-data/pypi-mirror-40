import requests, bs4
import re
import os
import threading

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

		domain = "http://"+website.split("/")[2]

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

def fetchImages(website, download=False, direc=None):
	links = []
	
	if validateUrl(website):

		if (download == True) and (direc == None):
			links.append("Enter a specific path in 'direc' key to download files!")
			return links
		elif (download == False) and (direc != None):
			links.append("Set 'download' key to True to download files!")
			return links
		elif (download == True) and (direc != None):
			if (not os.path.isdir(direc)):
				links.append("Enter a valid directory!")
				return links

		domain = "http://"+website.split("/")[2]

		try:
			r = requests.get(website)
		except:
			links.append("Error in Fetching Website")
			return links

		soup = bs4.BeautifulSoup(r.text, "html.parser")

		elem = soup.findAll('img')

		for link in elem:
			
			if link.has_attr('src'):
				if ("http" not in link['src']) and (link['src'][:2] != "//"):
					if link['src'][0] == "/":
						links.append(domain +  link.get('src'))
					else:
						links.append(domain + "/" +  link.get('src'))
				elif ("http" not in link['src']) and (link['src'][:2] == "//"):
					links.append("http:"+link.get('src'))
				else:
					links.append(link['src'])

		if (download == True) and (direc != None):
			for link in links:
				filename = link.split("/")[-1]
				t = threading.Thread(target=downloadImg, args = (link,filename,direc))
				t.start()
			return links
		else:
			return links


def downloadImg(link, fileName, dirName):
	try:
		req = requests.get(link, stream=True)
		fp = open(os.path.join(dirName, fileName), "wb")
		fp.write(req.content)
		fp.close()
	except:
		print("Error in Downloading the file : " + fileName)

def help(para=None):
	if para==None:
		print("\n:: Skewdi WebScrapper ::")
		print("::   Developer - Sam   ::\n")
		print("0 : fetchAnchor()")
		print("1 : fetchPara()")
		print("2 : fetchImages()")
		print("\nCall help() with the given number as a parameter, like - help(2)\n")
	elif para==0:
		print("\n-- fetchAnchor() --")
		print("\nCall this function like this - fetchAnchor('http://yourDomain.com')")
		print("It will return you all the hyperlinks available in the webpage in a list!\n")
	elif para==1:
		print("\n-- fetchPara() --")
		print("\nCall this function like this - fetchPara('http://yourDomain.com')")
		print("It will return you all the text inside <p> tag available in the webpage in a list!\n")
	elif para==2:
		print("\n-- fetchImages() --")
		print("\nCall this function like this - fetchImages('http://yourDomain.com')")
		print("It will return you all the Image link available in the webpage in a list!\n")
		print("Call this function like this - fetchImages('http://yourDomain.com' , download=True, direc='C:\\Users\\YourPathFolder')")
		print("It will return you the same list and it will download all the images to the perticular location provided by you.\n")
	else:
		print("Bad Option!")



def author():
	return "Samprit Sarkar"