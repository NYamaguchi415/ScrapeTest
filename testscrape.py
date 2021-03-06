from bs4 import BeautifulSoup
from urllib2 import urlopen


BASE_URL = "http://www.chicagoreader.com"

def get_category_links(section_url):
	soup = make_soup(section_url)
	boccat = soup.find("dl", "boccat")
	category_links = [BASE_URL + dd.a["href"] for dd in boccat.findAll("dd")]
	return category_links

def get_category_winner(category_url):
	soup = make_soup(category_url)
	category = soup.find("h1", "headline").string
	winner = [h2.string for h2 in soup.findAll("h2", "boc1")]
	runners_up = [h2.string for h2 in soup.findAll("h2", "boc2")]
	return {"category": category,
			"category_url": category_url,
			"winner": winner,
			"runners_up": runners_up}

def make_soup(url):
	html = urlopen(url).read()
	return BeautifulSoup(html, "lxml")

def write_to_db(category):
        #Open the database conection
        db = MySQLdb.connect("localhost","root","party123","scraping")
        #prepare a cursor object using the cursor method
        cursor = db.cursor()
        sql = "INSERT into chicago_scrape (category) values ('%s')\
        %(category)"
        #execute SQL query using execute() method.
        cursor.execute(sql,(category))
        #disconnect from the server
        db.commit()
        db.close

section_url = "http://www.chicagoreader.com/chicago/best-of-chicago-2011-food-drink/BestOf?oid=4106228"

links = get_category_links(section_url)

for link in links:
	category_details = get_category_winner(link)
	category = category_details["category"]
	category_url = category_details["category_url"]
	winner = category_details["winner"]
	runners_up = category_details["runners_up"]
	print category
	write_to_db(category)
	


