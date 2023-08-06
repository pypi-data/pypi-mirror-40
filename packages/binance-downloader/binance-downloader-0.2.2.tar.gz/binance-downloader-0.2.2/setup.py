# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['binance_downloader']

package_data = \
{'': ['*']}

install_requires = \
['dateparser>=0.7.0,<0.8.0',
 'logbook>=1.4,<2.0',
 'pandas>=0.23,<0.24',
 'requests>=2.21,<3.0',
 'tables>=3.4,<4.0',
 'tqdm>=4.28,<5.0']

entry_points = \
{'console_scripts': ['kline-binance = binance_downloader.cli:main']}

setup_kwargs = {
    'name': 'binance-downloader',
    'version': '0.2.2',
    'description': 'CLI to download k-line (candlestick/OHLC) data from Binance API',
    'long_description': 'Binance Downloader\n==================\n\n[![Build Status](https://travis-ci.com/anson-vandoren/binance-downloader.svg?branch=master)](https://travis-ci.com/anson-vandoren/binance-downloader)\n\nPython tool to download Binance Candlestick (k-line) data from REST API\n\nOriginally forked from [bullsignals/binance-downloader](https://github.com/bullsignals/binance-downloader),\nthat project does not seem to be maintained any longer and I wanted to actually make use\nof this project and allow others to contribute. At this point, I have re-written almost\nall the code from scratch, but would like to thank the original authors for their ideas\nthat got me started.\n\n\n\nInstallation\n-----------\n\n### Prerequisites\nYou will need Poetry installed in order to install this package and run from the command line.\nPoetry is a Python package and dependency manager that makes installation and distribution\nreally easy. Installation instructions [can be found here](https://poetry.eustace.io/docs/#installation)\nfor macOS/Linux/Windows\n- Verify Poetry installation\n```console\n$ poetry --version\nPoetry 0.12.10\n```\n\n### Download and install\n##### Clone the repository\n```console\n$ git clone https://github.com/anson-vandoren/binance-downloader.git\n$ cd binance-downloader\n```\n##### Activate your virtual environment\nPoetry will try to automatically enable a virtual environment for you if it detects\nyou are not already using one.\n> If you already use virtualenvwrapper (or similar), go ahead and make (or switch to)\n> your working environment beforehand:\n>\n>```console\n>$ mkvirtualenv binance-downloader\n>```\n>or\n>```console\n>$ workon binance-downloader\n>```\n\n##### Install dependencies\n```console\n$ poetry install\nInstalling dependencies from lock file\n\nPackage operations: 12 installs, 0 updates, 0 removals\n\n  - Installing six (1.12.0)\n  - Installing certifi (2008.11.29)\n  - Installing chardet (3.0.4)\n  - Installing idna (2.8)\n  - Installing numpy (1.15.4)\n  - Installing python-dateutil (2.7.5)\n  - Installing pytz (2018.7)\n  - Installing urllib3 (1.22)\n  - Installing logbook (1.4.1)\n  - Installing pandas (0.23.4)\n  - Installing requests (2.21.0)\n  - Installing tqdm (4.28.1)\n  - Installing binance-downloader (0.2.0)\n```\n\n\nUsing the Command Line Interface\n-----------------------------\n##### Show available options\n```console\n$  kline-binance --help\nusage: kline-binance [-h] [--start START] [--end END] [--dtfmt DATE_FORMAT]\n                     symbol interval\n\nCLI for downloading Binance Candlestick (k-line) data in bulk\n\npositional arguments:\n  symbol               (Required) Binance symbol pair, e.g. ETHBTC\n  interval             (Required) Frequency interval in minutes(m); hours(h);\n                       days(d); weeks(w); months(M); All possibles values: 1m\n                       3m 5m 15m 30m 1h 2h 4h 6h 8h 12h 1d 3d 1w 1M\n\noptional arguments:\n  -h, --help           show this help message and exit\n  --start START        Start date to get data (inclusive). Format: yyyy/mm/dd\n  --end END            End date to get data (exclusive). Format: yyyy/mm/dd\n  --dtfmt DATE_FORMAT  Format to use for dates (DMY, MDY, YMD, etc). Default:\n                       YMD\n```\n\n##### Downloading data\n```console\n$  kline-binance XRPBTC 1m --start 2016-01-01 --end now\n[2019-01-02 05:12:40.941301] NOTICE: api: First available kline starts on {from_ms_utc(period_start)}\n[2019-01-02 05:12:40.941867] NOTICE: api: Downloading 620 chunks...\nDownload : 100%|█████████████████████████████████████████████████| 620/620 [00:48<00:00, 12.73 chunk/s]\nWrite CSV: 100%|███████████████████████████████████████████████████| 100/100 [00:14<00:00,  7.04 pct/s]\n[2019-01-02 05:13:44.784379] NOTICE: db: Done writing ./downloaded/2019-01-01_211330_XRPBTC_1m.csv for 612794 lines\n```\n\nLicense\n-------\nThis code is made available under the MIT License. See LICENSE file for detail.\n',
    'author': 'Anson VanDoren',
    'author_email': 'anson.vandoren@gmail.com',
    'url': 'https://github.com/anson-vandoren/binance-downloader.git',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.5',
}


setup(**setup_kwargs)
