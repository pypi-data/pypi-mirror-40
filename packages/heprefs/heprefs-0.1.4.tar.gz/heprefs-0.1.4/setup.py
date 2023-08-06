# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['heprefs']

package_data = \
{'': ['*']}

install_requires = \
['arxiv>=0.3.1,<0.4.0', 'click>=7.0,<8.0', 'feedparser>=5.2,<6.0']

extras_require = \
{':python_version < "3.5"': ['typing>=3.6,<4.0']}

entry_points = \
{'console_scripts': ['heprefs = heprefs.heprefs:heprefs_main']}

setup_kwargs = {
    'name': 'heprefs',
    'version': '0.1.4',
    'description': 'A commandline helper tool for high-energy physics referencing.',
    'long_description': 'heprefs: CLI for high-energy physics references\n===============================================\n\n![screen shot](https://user-images.githubusercontent.com/776101/36547606-8aa5d438-17ee-11e8-9ddb-64a5a4e7d2f5.gif)\n\nDo you think the commands are too long? Simply configure your shell by editing  `.zshrc`; for example,\n\n```:.zshrc\nfunction xa()      { if [ $# != 0 ]; then for i in $*; do heprefs abs $i; done; fi }\nfunction xx()      { if [ $# != 0 ]; then for i in $*; do heprefs pdf $i; done; fi }\nfunction xget()    { if [ $# != 0 ]; then for i in $*; do heprefs get -o $i; done; fi }\nfunction xsource() { if [ $# != 0 ]; then for i in $*; do heprefs source -u $i; done; fi }\n```\n\n(or see below) and you will just type `xget 1802.07720 1708.00283` etc. to download multiple PDFs!\n\n### Set up\n\nFor Python 2 or 3.\n\n#### Install\n\n```console\n$ pip install git+https://github.com/misho104/heprefs.git\n\nCollecting git+https://github.com/misho104/heprefs.git\n  Cloning https://github.com/misho104/heprefs.git to /private/tmp/pip-wjd8srsu-build\n...\nSuccessfully installed arxiv-0.1.1 click-6.7 feedparser-5.2.1 heprefs-0.1.0 requests-2.13.0\n```\n\nor you can install specific version by, e.g.,\n\n```console\n$ pip install git+https://github.com/misho104/heprefs.git@v0.1.0       # for v0.1.0\n$ pip install git+https://github.com/misho104/heprefs.git@development  # for development version\n```\n\n#### Upgrade\n\n```console\n$ pip install git+https://github.com/misho104/heprefs.git --upgrade\n```\n\n#### Uninstall\n\n```console\n$ pip uninstall heprefs\n```\n\n\n### Usage\n\n#### Open abstract pages by a browser\n\n```console\n$ heprefs abs 1505.02996               # arXiv\n$ heprefs abs hep-th/9711200           # arXiv (old style)\n$ heprefs abs ATLAS-CONF-2017-018      # CERN Document Server\n$ heprefs abs 10.1038/nphys3005        # DOI (inspireHEP)\n$ heprefs abs "fin a Ellis"            # inspireHEP (first result is only shown)\n\n$ heprefs abs 9709356                  # equivalent to \'hep-ph/9709356\'\n```\n\n#### Open PDF by browser, or Download PDF file\n\nPDF may not be found for CDS or inspireHEP queries.\n\n```console\n$ heprefs pdf 1505.02996               # arXiv\n$ heprefs pdf ATLAS-CONF-2017-018      # CERN Document Server\n\n$ heprefs get 10.1038/nphys3005        # DOI (inspireHEP)\n$ heprefs get "fin a Ellis"            # inspireHEP (first result)\n\n$ heprefs get -o "fin a Giudice"       # open the PDF file\n```\n\n#### Show information\n\n```console\n$ heprefs authors 1505.02996\n$ heprefs first_author hep-th/9711200\n$ heprefs title 10.1038/nphys3005\n$ heprefs short_info ATLAS-CONF-2017-018\n```\n\n\n### Advanced usage\n\n#### Specify search engine\n\nThere are three **types**: arXiv, inspireHEP, and CDS. They are automatically guessed, but you can specify a type:\n\n```console\n$ heprefs abs -t arxiv 1505.02996           # arXiv\n$ heprefs abs -t cds   "top asymmetry"      # CDS\n$ heprefs abs -t ins   "top asymmetry"      # inspireHEP\n\n$ heprefs abs        ATLAS-CONF-2017-018    # guessed as CDS search\n$ heprefs abs -t ins ATLAS-CONF-2017-018    # forced to use inspireHEP\n```\n\n#### Commands are too long?\n\nIn your `.zshrc`, `.bashrc`, etc...\n\n```:.zshrc\nalias xa=\'heprefs abs\'\nalias xx=\'heprefs pdf\'\nalias xget=\'heprefs get\'\n```\n\nor if you want to handle multiple arguments,\n\n```:.zshrc\nfunction xa()      { if [ $# != 0 ]; then for i in $*; do heprefs abs $i; done; fi }\nfunction xx()      { if [ $# != 0 ]; then for i in $*; do heprefs pdf $i; done; fi }\nfunction xget()    { if [ $# != 0 ]; then for i in $*; do heprefs get -o $i; done; fi }\nfunction xsource() { if [ $# != 0 ]; then for i in $*; do heprefs source -u $i; done; fi }\n```\n\n\n\n(You may want to use inspire search as well, though this is not a feature of this software.)\n\n```:.zshrc\nfunction browser() {\n  google-chrome $* &             # on Linux\n  # open $* -a Google\\ Chrome    # on macOS\n}\n\nfunction fin() {\n  local query; if [ $# != 0 ]; then; for i in $*; do; query="$query+$i"; done; fi\n  query=`echo $query | sed \'s/^\\+//\'`\n  browser http://inspirehep.net/search\\?p=fin+$query &\n}\n\nfunction insp() {\n  local query; if [ $# != 0 ]; then; for i in $*; do; query="$query+$i"; done; fi\n  query=`echo $query | sed \'s/^\\+//\'`\n  browser http://inspirehep.net/search\\?p=$query &\n}\n```\n\nand now you can invoke\n\n```console\n$ xa 1505.02996\n$ xget 9709356\n$ fin a Giudice and Masiero\n$ fin bb hep-th/9711200\n$ insp relaxion\n```\n\n\n#### Debug command for developers\n\n```console\n$ heprefs debug 1505.02996\n```\n',
    'author': 'Sho Iwamoto (Misho)',
    'author_email': 'webmaster@misho-web.com',
    'url': 'https://github.com/misho104/heprefs',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*',
}


setup(**setup_kwargs)
