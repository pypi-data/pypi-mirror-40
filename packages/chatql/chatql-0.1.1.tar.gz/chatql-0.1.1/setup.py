# -*- coding: utf-8 -*-
from distutils.core import setup

package_dir = \
{'': 'src'}

packages = \
['chatql', 'chatql.matcher']

package_data = \
{'': ['*']}

install_requires = \
['flask[server]>=1.0,<2.0',
 'graphene>=2.1,<3.0',
 'line-bot-sdk[line]>=1.8,<2.0',
 'mongoengine>=0.16.3,<0.17.0']

setup_kwargs = {
    'name': 'chatql',
    'version': '0.1.1',
    'description': '',
    'long_description': '# ChatQL\nGraphQL based chat engine\n\n## Dependencies\nThis module depend following system environment.\n\n- python >= 3.6\n- mongodb >= 4.0\n\nFollowing dependency python modules are installed when `pip install`.\n\n- graphene >= 2.1\n- mongoengine >= 0.16.3\n\n## Demo\nYou clone this repository and run following commands.\n\nAfter, you can access GraphQL interface `POST localhost:8080/graphql`.\n\nPlease check response by GraphQL tool (ex: [GraphiQL](https://electronjs.org/apps/graphiql)).\n```\ndocker build ./demo -t chatql\ndocker run -p 8080:5000 -it chatql\n```\n\n## TODO\n- Application Function\n    - [ ] Response Generator with Template Engine\n    - [ ] Extract Entity with Template Matching\n    - [ ] Non Text Query\n    - [ ] Intent Estimator with Machine Learning\n    - [ ] Extract Entity with Machine Learning\n- Document\n    - [ ] API Docs \n    - [ ] Conditions Pattern Docs\n    - [ ] Response Docs\n\n## License\nMIT License.',
    'author': 'katsugeneration',
    'author_email': 'katsu.generation.888@gmail.com',
    'url': 'https://github.com/katsugeneration',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
