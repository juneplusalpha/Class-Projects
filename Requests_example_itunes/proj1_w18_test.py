import unittest
import proj1_w18 as proj1

class TestMedia(unittest.TestCase):
	def testConstructor(self):
		m1 = proj1.Media()
		m2 = proj1.Media("1999", "Prince")
		self.assertEqual(m1.title, "No Title")
		self.assertEqual(m1.author, "No Author")
		self.assertEqual(m2.title, "1999")
		self.assertEqual(m2.author, "Prince")

	def testMethods(self):
		m2 = proj1.Media("Title", "Author")
		self.assertEqual(m2.__str__(), "Title by Author (No Year)")
		self.assertEqual(m2.__len__(), 0)

class TestSong(unittest.TestCase):
	def testConstructor(self):
		song1 = proj1.Song()
		song2 = proj1.Song("test Title", "test Author", "2011", "SomeAlbum", "SomeGenre", "256734")

		self.assertEqual(song1.title, "No Title")
		self.assertEqual(song2.title, "test Title")
		self.assertEqual(song1.genre, "No Genre")
		self.assertEqual(song2.genre, "SomeGenre")
		self.assertEqual(song1.tracklength, 0)
		self.assertEqual(song2.tracklength, "256734")
		self.assertIsInstance(song1, proj1.Song)

	def testMethods(self):
		t2 =proj1.Song("Title", "author", "1999", "album", "genre", "200300")
		self.assertEqual(t2.__str__(), 'Title by author (1999)[genre]')
		self.assertEqual(t2.__len__(), 200.3)


class TestMovie(unittest.TestCase):
	def testConstructor(self):
		movie1 = proj1.Movie()
		movie2 = proj1.Movie("test Title", "test Author", "2011", "PG", "256734")
		self.assertIsInstance(movie1, proj1.Movie)
		self.assertEqual(movie1.title, "No Title")
		self.assertEqual(movie2.title, "test Title")
		self.assertEqual(movie1.releaseyear, "No Year")
		self.assertEqual(movie2.releaseyear, "2011")
		self.assertEqual(movie2.rating, "PG")
		self.assertEqual(movie2.movielength, "256734")

	def testMethods(self):
		t2 =proj1.Movie("Title", "author", "2000")
		self.assertEqual(t2.__str__(), 'Title by author (2000)[No Rating]')
		self.assertEqual(t2.__len__(), 0)


class TestTask2(unittest.TestCase):
	def testJson(self):
		medialist = proj1.open_and_parse()
		media1 = medialist[0]
		media2 = medialist[1]
		media3 = medialist[2]

		self.assertIsInstance(media1, proj1.Movie)
		self.assertIsInstance(media2, proj1.Song)
		self.assertIsInstance(media3, proj1.Media)

		self.assertEqual(media3.title, "Bridget Jones's Diary (Unabridged)")
		self.assertEqual(media3.author, "Helen Fielding")
		self.assertEqual(media3.releaseyear, 2012)

		self.assertEqual(media2.title, "Hey Jude")
		self.assertEqual(media2.author, "The Beatles")
		self.assertEqual(media2.releaseyear, 1968)
		self.assertEqual(media2.album, "TheBeatles 1967-1970 (The Blue Album)")
		self.assertEqual(media2.genre, "Rock")

		self.assertEqual(media1.title, "Jaws")
		self.assertEqual(media1.author, "Steven Spielberg")
		self.assertEqual(media1.releaseyear, 1975)
		self.assertEqual(media1.rating, "PG")

		self.assertEqual(media1.__str__(), 'Jaws by Steven Spielberg (1975)[PG]')
		self.assertEqual(media1.__len__(), round(7451455/1000/60))

		self.assertEqual(media2.__str__(), 'Hey Jude by The Beatles (1968)[Rock]')
		self.assertEqual(media2.__len__(), 431333/1000)

		self.assertEqual(media3.__str__(), "Bridget Jones's Diary (Unabridged) by Helen Fielding (2012)")

class TestiTunes(unittest.TestCase):

	def testQuery(self, query = None):
		result = proj1.makeQuery(query)

		for i in range(len(result['songs'])):
			self.assertIsInstance(result['songs'][i], proj1.Song)
			self.assertNotIsInstance(result['songs'][i], proj1.Movie)
			self.assertIsNotNone(result['songs'][i].album)
			self.assertIsNotNone(result['songs'][i].genre)
			self.assertIsNotNone(result['songs'][i].tracklength)
		for i in range(len(result['movies'])):
			self.assertIsInstance(result['movies'][i], proj1.Movie)
			self.assertNotIsInstance(result['movies'][i], proj1.Song)
			self.assertIsNotNone(result['movies'][i].rating)
			self.assertIsNotNone(result['movies'][i].movielength)
		for i in range(len(result['others'])):
			self.assertIsInstance(result['others'][i], proj1.Media)


	def testCommonWords(self):
		self.testQuery("baby")
		self.testQuery("love")

	def testUniqueWords(self):
		self.testQuery("moana")
		self.testQuery("helter skelter")

	def testNonsenseQueries(self):
		self.testQuery("$@#!")

	def testBlankQuery(self):
		self.testQuery("")


unittest.main(verbosity=2)
