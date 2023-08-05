# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['ergal']

package_data = \
{'': ['*']}

install_requires = \
['colorama>=0.4.0,<0.5.0', 'requests>=2.20,<3.0', 'xmltodict>=0.11.0,<0.12.0']

setup_kwargs = {
    'name': 'ergal',
    'version': '0.1.7',
    'description': 'The Elegant and Readable General API Library',
    'long_description': "ergal\n=====\n\nEver dealt with a bunch of API clients? Whether they be methods in your own code, or an abundance of external libraries, dealing with multiple APIs in one application can get messy.\n\nergal, the Elegant and Redable General API Library, is the solution to your API client problems. By using API profiles stored in a lightweight SQLite database, the user can access any API with ease by supplying just a few key details.\n\nGoals\n-----\n\n- Abstract API handling\n- Clean up codebases\n- Win\n\nStandard Installation\n---------------------\n\n    pip install ergal\n\n### Requirements\n- [Python 3.7](https://www.python.org/downloads/)\n\nQuickstart\n-----------\n\n### Profile Creation\nBefore we can access an API (we'll use `httpbin.com` in this case), we have to add an `API Profile`. To create an `API profile`, we'll use the `Profile` class from `ergal.profile`.\n\n    >>> from ergal.profile import Profile\n    >>> profile = Profile('HTTPBin', base='https://httbin.org')\n\nA new row has been created in the local `ergal.db` database to house the API profile's information.\n\nNow that the profile has been created, we'll need to add an endpoint, and to do so, we'll use the `add_endpoint` method, and supply it with a `name`, `path`, and `method`.\n\n    >>> profile.add_endpoint('Get JSON', '/json', 'get')\n    Endpoint 'Get JSON' for HTTPBin added at ab0b5ffa9fa95c6.\n\nWith an endpoint added, we can make the call. To do that, we'll use the `call` method. All we need to supply is the name of the endpoint we just added, and ergal will do the rest.\n\n    >>> profile.call('Get JSON')\n    <big dict of response data>\n\nHooray! Now we can do whatever we want with our cleaned up and easy-to-work-with dictionary of response data.\n\n\nContribution\n------------\n\nThe biggest priority of this project is to make API handling simple, both on the client's side and ergal's side. That said, some protocol can get pretty complex. We've got a few major improvements on our roadmap, and contribution is always appreciated.\n\nAs per most open source projects, submitted code needs to be continuous with the rest in style, it needs to be as succinct and readable as it can be, and it has to serve a real purpose according to the objectives of this project.\n\n### Feature Ideas\n\n#### OAuth 1.0a and OAuth 2\nOAuth 2 is obviously the priority here, given its increase in popularity, however, we want to provide as much compatability as possible. ergal is supposed to be a one-stop solution!\n\n#### Useful HTML Parsing\nThough virtually every API uses JSON or XML to send response data, what may be useful is the parsing of HTML in the context of a scraping library. In the same sense, often times lots of code needs to be written to support scrapers of multiple sites, so having HTML compatability would be useful.\n\n#### Targetted Parsing (being implemented in v0.1.7)\nOne of the original feature ideas for ergal was the targetted parsing of responses, i.e. one could specify on a given endpoint what data should be returned. This would, of course, further eliminate what parsing needs to be done on the client's end by abstracting it within ergal.\n\n#### Response Analytics and Caching\nThis feature would enable the user to store the contents of responses in the local `ergal.db` database, as well as record analytical data about the activity of a given endpoint or API, i.e. number of calls, status codes, load times, etc.\n\n### Development Setup\n\n    git clone https://github.com/elliott-maguire/ergal\n    cd ergal\n    pyenv local 3.7.1\n    poetry install\n\n### Development Requirements\n- [Python 3.7](https://www.python.org/downloads/)\n- [poetry](https://github.com/sdispater/poetry) (a package/version manager for humans)\n\n### Recommended Tools\n- [pyenv](https://github.com/pyenv/pyenv) (preferred venv manager)\n",
    'author': 'Elliott Maguire',
    'author_email': 'etgmag@comcast.net',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
