from soupstars import HttpParser, parse


class NytimesArticleParser(HttpParser):
    default_host = "http://www.nytimes.com"
    default_route = "/2019/01/07/us/politics/trump-address-border-visit.html"

    @parse
    def title(self):
        return self.read().find('h1').text.replace("\"", "")

    @parse
    def authors(self):
        return self.read().find("p", attrs={"itemprop": "author creator"}).text.replace("\"", "")

    @parse
    def published_at(self):
        return self.read().find("time").text.replace("\"", "")
