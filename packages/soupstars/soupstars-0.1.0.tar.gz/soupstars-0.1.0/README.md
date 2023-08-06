# Soupstars

Soupstars makes it easy to build website parsers.

```
from soupstars import HttpBaseRecipe, ingredient

class FacebookRecipe(HttpBaseRecipe):
    @ingredient
    def title(self):
        return self.read().find('h2').text.strip()

fb = FacebookRecipe("https://www.facebook.com")

print(fb['title'])
# Connect with friends and the world around you
```

Install with pip.

```
pip install soupstars
```

There's a few prebuilt parsers, but they're not necessary maintained.

```
>> from soupstars.recipes.nytimes import NytimesArticleRecipe

>> article_url = "https://www.nytimes.com/2019/01/07/us/politics/trump-address-border-visit.html"
>> article = NytimesArticleRecipe(article_url)
>> article.json()
{
  "authors": "\"By Maggie Haberman, Michael M. Grynbaum and Eileen Sullivan\"",
  "published_at": "\"Jan. 7, 2019\"",
  "title": "\"Trump Wants to Deliver Prime-Time Address on Government Shutdown and Will Visit the Border\""
}
```
