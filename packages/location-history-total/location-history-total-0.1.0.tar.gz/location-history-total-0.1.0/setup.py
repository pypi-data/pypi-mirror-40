# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['location_history_total']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'location-history-total',
    'version': '0.1.0',
    'description': 'Given a Takeout of Google Location History, generate a CSV of work history.',
    'long_description': "# location-history-total\nGiven a Takeout of Google Location History, generate a CSV of work history.\n\nRequires Python 3.6+.\n\n# Example usage\n\n1. Create a document with your points of interest:\n\n    ```\n    # Format is lat, long, radius\n    # '#' can be used to comment a line out\n    38.8100121,-104.6792472, 0.04\n    39.1355552,-121.3484781, 0.1\n    ```\n    \n    Google Maps will be handy for determining the latitude and longitude of places.\n\n2. Use Google Takeout to export your location history.\n\n   - Current link is https://takeout.google.com/settings/takeout?hl=en\n   - Support link is https://support.google.com/accounts/answer/3024190?hl=en\n\n3. (Optional) Determine the time period(s) you're intested in and get the Unix timestamps of the start and stop dates.\n\n3. Run the script. Assuming your POIs are in `area.txt`, your location history is at `history.json`, and a date range of 1 Oct 2018-1 Mar 2019:\n\n    ```\n    # Dump information to screen\n    ./extact2.py history.json --area=area.txt --time=1538373600,1551423600 \n    \n    # Or to a CSV\n    ./extact2.py history.json --area=area.txt --time=1538373600,1551423600 --output=results.csv\n    ```\n    \n    \n",
    'author': 'Ryan Morehart',
    'author_email': 'ryan@moreharts.com',
    'url': 'https://github.com/traherom/location-history-total',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
