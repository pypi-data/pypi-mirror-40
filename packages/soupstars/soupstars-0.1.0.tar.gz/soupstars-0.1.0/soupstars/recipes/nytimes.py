from soupstars import HttpBaseRecipe, ingredient


class NytimesArticleRecipe(HttpBaseRecipe):
    @ingredient
    def title(self):
        return self.read().find('h1').text.replace("\"", "")

    @ingredient
    def authors(self):
        return self.read().find("p", attrs={"itemprop": "author creator"}).text.replace("\"", "")

    @ingredient
    def published_at(self):
        return self.read().find("time").text.replace("\"", "")
