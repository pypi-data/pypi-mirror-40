import feedparser
from audiobooker.scrappers import AudioBook, BookAuthor, BookGenre, \
    AudioBookSource


class LoyalBooksAudioBook(AudioBook):
    """
    """

    def __init__(self, title="", authors=None, description="", genres=None,
                 book_id="", runtime=0, url="", rss_url="",
                 language='english', json_data=None):
        """

        Args:
            title:
            authors:
            description:
            genres:
            book_id:
            runtime:
            url:
            rss_url:
            language:
            json_data:
        """
        AudioBook.__init__(self, title, authors, description, genres,
                           book_id, runtime, url, language)
        self.rss_url = rss_url or url + "/feed"
        if json_data:
            self.from_json(json_data)
        self.raw = json_data or {}

    @property
    def rss_data(self):
        """

        Returns:

        """
        return feedparser.parse(self.rss_url)

    @property
    def streamer(self):
        """

        """
        for stream in self.rss_data["entries"]:
            try:
                yield stream['media_content'][0]["url"]
            except Exception as e:
                print(e)
                continue

    @property
    def authors(self):
        """

        Returns:

        """
        return [BookAuthor(json_data=a) for a in self._authors]

    @property
    def genres(self):
        """

        Returns:

        """
        return [BookGenre(json_data=a) for a in self._genres]

    def from_json(self, json_data):
        """

        Args:
            json_data:
        """
        AudioBook.from_json(self, json_data)
        self.rss_url = json_data.get("url_rss", self.rss_url)

    def __repr__(self):
        """

        Returns:

        """
        return "LoyalBooksAudioBook(" + str(self) + ", " + self.book_id + ")"


class LoyalBooks(AudioBookSource):
    pass
