import webbrowser

class Movie():
	"""Movie class, is the abstraction for creating instances of a movie, setting as properties: the movie title, the storyline, the yoytube trailer and the poster image"""
	def __init__(self,title,storyline,poster_image_url,trailer_url,year):
		self.title = title
		self.storyline = storyline
		self.poster_image_url = poster_image_url
		self.trailer_youtube_url = trailer_url
		self.year = year
	#Method for showing the trailer of the movie
	def show_trailer(self):
		webbrowser.open(self.trailer_url)