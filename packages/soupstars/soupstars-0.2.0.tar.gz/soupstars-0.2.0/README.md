# Soupstars

[![Build Status](https://travis-ci.com/tjwaterman99/soupstars.svg?branch=master)](https://travis-ci.com/tjwaterman99/soupstars) [![Documentation Status](https://readthedocs.org/projects/soupstars/badge/?version=latest)](https://soupstars.readthedocs.io/en/latest/?badge=latest) [![Coverage Status](https://coveralls.io/repos/github/tjwaterman99/soupstars/badge.svg)](https://coveralls.io/github/tjwaterman99/soupstars)

Soupstars makes it easy to build website parsers.

```python
from soupstars import HttpParser, parse

class FacebookParser(HttpParser):

    default_host = "https://www.facebook.com"

    @parse
    def title(self):
        return self.read().find('h2').text.strip()

fb = FacebookParser("/")
fb.json() # { "title": "connect with friends and the world around you" }
```

# Installation

The easiest way to get started is to install with pip.

```bash
pip install soupstars
```

You can play around with one of the prebuilt parsers directly.

```python
>>> from soupstars.parsers.nytimes import NytimesArticleParser
>>> article = NytimesArticleParser("2019/01/09/us/politics/government-shutdown-trump-senate.html")
>>> article['title']  # Trump storms out of white house meeting with democrats
```

If you have docker, you can run a web api to serve the parsers. Clone this repo and start the containers.

```bash
$ docker-compose up
```

Parsers are served at `/parsers/{parser_package}/{parser_module}`, and any json data will be used to initialize the parser.

```bash
curl -X GET 0.0.0.0:5000/parsers/nytimes/article \
  -H "Content-Type: application/json" \
  -d '{"url": "/2019/01/10/us/politics/trump-wall-texas-border.html"}'

  {
    "data": {
      "authors": "By Michael Tackett",
      "published_at": "Jan. 10, 2019",
      "title": "Trump, Heading to the Border, Suggests He Will Declare an Emergency to Fund the Wall"
    }
  }
```

To integrate the parsers with an existing flask app, register the `soupstars_blueprint`.

```python
from soupstars import soupstars_blueprint

def create_app():
    app = Flask(__name__)
    app.register_blueprint(soupstars_blueprint)
```

# Developing

Make sure that you've installed docker-compose. Then start the containers.

```
docker-compose up -d
docker-compose ps
```

Tests should be ran from inside the container.

```
docker-compose run --rm test
```
