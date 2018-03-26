import json
import webbrowser
import requests
import time


class Media:

	def __init__(self, title="No Title", author="No Author", releaseyear = "No Year", json = None):
		if json is None:
			self.title = title
			self.author = author
			self.releaseyear = releaseyear
		else:
			if 'kind' in json:
				self.title = json['trackName']

			elif json['wrapperType'] == 'audiobook':
				self.title = json['collectionName']

			self.author = json["artistName"]
			self.releaseyear = int(json["releaseDate"][:4])
			if 'trackViewUrl' in json:
				self.url = json["trackViewUrl"]
			elif 'collectionViewUrl' in json:
				self.url = json["collectionViewUrl"]
			else:
				self.url = None

	def __str__(self):
		return "{} by {} ({})".format(self.title, self.author, self.releaseyear)

	def __len__(self):
		return 0



class Song(Media):
	def __init__(self, title="No Title", author="No Author", releaseyear = "No Year", album= "No Album", genre= "No Genre", tracklength = 0, json = None):
		super().__init__(title, author, releaseyear, json)
		if json is None:
			self.album = album
			self.genre = genre
			self.tracklength = tracklength
		else:
			self.album = json['collectionName']
			self.genre = json['primaryGenreName']
			self.tracklength = int(json["trackTimeMillis"])

	def __str__(self):
		return super().__str__() + "[{}]".format(self.genre)

	def __len__(self):
		return int(self.tracklength) / 1000


class Movie(Media):
	def __init__(self, title="No Title", author="No Author", releaseyear = "No Year", rating = "No Rating", movielength = 0, json = None):
		super().__init__(title, author, releaseyear, json)
		if json is None:
			self.rating = rating
			self.movielength = movielength
		else:
			self.rating = json["contentAdvisoryRating"]
			self.movielength = int(json["trackTimeMillis"])

	def __str__(self):
		return super().__str__() + "[{}]".format(self.rating)

	def __len__(self):
		return round((int(self.movielength)/1000.00)/60.00) #convert & round to mins


def open_and_parse(filename = 'sample_json.json'):
	with open(filename, 'r') as file:
		sample_json = json.load(file)

	media_objects = []

	for item in sample_json:
		if item['wrapperType'] == "track":
			if item['kind'] == "song":
				print("appending song")
				media_objects.append(Song(json = item))
			else:
				print("appending movie")
				media_objects.append(Movie(json = item))
		else:
			print("appending other")
			media_objects.append(Media(json = item))
	# print(media_objects)

	return media_objects



def getiTunesResult(term, limit = 30):
	baseurl = "https://itunes.apple.com/search"
	params = {}
	params["term"] = term
	params["limit"] = limit
	return requests.get(baseurl, params).json()["results"]


def makeQuery(query):
	results = {'songs': [], 'movies': [], 'others': []}
	for item in getiTunesResult(query):
		if 'kind' in item:
			if item['kind'] == 'song':
				results['songs'].append(Song(json = item))
			elif item['kind'] == 'feature-movie':
				results['movies'].append(Movie(json = item))
		else:
			results['others'].append(Media(json = item))
	return results

def isInteger(word):
	try:
		int(word)
		return True
	except ValueError:
		return False


if __name__ == "__main__":

	query = input("Enter a search term or \'exit\' to quit: ")

	while(query != "exit"):

		cnt = 0
		querydict = {}
		resultdict = makeQuery(query)

		time.sleep(0.5)


		print("SONGS:")
		for song in resultdict['songs']:
			cnt += 1
			querydict[cnt] = song
			print(cnt, song)

		time.sleep(0.5)

		if len(resultdict['songs']) == 0:
			print("Couldn't find songs with query: {}".format(query))

		time.sleep(0.5)


		print("\nMOVIES: ")
		for movie in resultdict['movies']:
			cnt += 1
			querydict[cnt] = movie
			print(cnt, movie)
		
		time.sleep(0.5)

		if len(resultdict['movies']) == 0:
			print("Couldn't find movies with query: {}".format(query))

		time.sleep(0.5)


		print("\nOTHER MEDIA: ")
		for medium in resultdict['others']:
			cnt += 1
			querydict[cnt] = medium
			print(cnt, medium)
		time.sleep(0.5)

		if len(resultdict['others']) == 0:
			print("Couldn't find other media with query: {}".format(query))

		time.sleep(0.5)
		next = input("\nEnter a number for more info, or a new search term, or exit: ")
		while isInteger(next):
			if int(next) > 0 and int(next) <= cnt:
				if querydict[int(next)].url != None:
					print("Launching", querydict[int(next)].url, "in browser\n")
					webbrowser.open(querydict[int(next)].url)
				else:
					print("Cannot launch due to lack of URL")
				next = input("Enter a number for more info, or a new search term, or exit: ")
			else:
				next = input("invalid input. enter a corresponding number or a new search term: ")
		time.sleep(0.5)
		query = next











