# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['docker_compose_expand']

package_data = \
{'': ['*'], 'docker_compose_expand': ['utils/*']}

install_requires = \
['jinja2>=2.10,<3.0', 'oyaml>=0.7.0,<0.8.0']

entry_points = \
{'console_scripts': ['docker-compose-expand = docker_compose_expand.cli:main']}

setup_kwargs = {
    'name': 'docker-compose-expand',
    'version': '0.1.0',
    'description': 'Expand your docker-compose.yml file',
    'long_description': '# Docker Compose Expand\n\nExpand your docker-compose.yml file with this tool.\n\n# Install\n\n```bash\n$ pip3 install --user docker-compose-expand\n```\n\n# Usage\n\nYour services in `docker-compose.yml` file.\n\n```yaml\nversion: "3"\nservices:\n  api:\n    image: ef9n/supervisord:0.1.0\n    restart: on-failure\n    ports:\n      - "9001:9001"\n\n  products:\n    image: ef9n/supervisord:0.1.0\n    restart: on-failure\n    ports:\n      - "9002:9001"\n\n  analysis:\n    image: ef9n/supervisord:0.1.0\n    restart: on-failure\n    ports:\n      - "9003:9001"\n\n  monitoring:\n    image: ef9n/supervisord:0.1.0\n    restart: on-failure\n    ports:\n      - "9004:9001"\n```\n\nInstead of using the `docker-compose` tool, define the same services in the `docker-compose-expand.yml` file and use the `docker-compose-expand` tool that generates the `docker-compose.yml` file for your expandable services.\n\n- You can define variables in `loop` field or `vars` field.\n\n- In the `loop` field, you can refer to a variable which is in the `vars` field.\n\n### Loop Field\n\n```yaml\nversion: "3"\nservices:\n  api:\n    image: ef9n/supervisord:0.1.0\n    restart: on-failure\n    ports:\n      - "9001:9001"\n\nexpand:\n  vars:\n  services:\n    - name: "{{ name }}"\n      service:\n        image: ef9n/supervisord:0.1.0\n        restart: on-failure\n        volumes:\n          - "/tmp/{{ name }}/:/opt/{{name}}/"\n        ports:\n          - "{{ port }}:9001"\n      loop:\n        - name: products\n          port: 9002\n        - name: analysis\n          port: 9003\n        - name: monitoring\n          port: 9004\n```\n\n### Vars Field\n\n```yaml\n# Vars Field\nversion: "3"\nservices:\n  api:\n    image: ef9n/supervisord:0.1.0\n    restart: on-failure\n    ports:\n      - "9001:9001"\n\nexpand:\n  vars:\n    supervisors:\n      - name: products\n        port: 9002\n      - name: analysis\n        port: 9003\n      - name: monitoring\n        port: 9004\n  services:\n    - name: "{{ name }}"\n      service:\n        image: ef9n/supervisord:0.1.0\n        restart: on-failure\n        volumes:\n          - "/tmp/{{ name }}/:/opt/{{name}}/"\n        ports:\n          - "{{ port }}:9001"\n      loop: "{{ supervisors }}"\n```\n\n# Examples\n\nLook up the [examples](https://github.com/f9n/docker-compose-expand/tree/master/examples) directory.\n\n# Credits\n\n- [Docker Compose](https://github.com/docker/compose)\n- [Ansible Yaml Standard](https://github.com/ansible/ansible)\n',
    'author': 'Fatih Sarhan',
    'author_email': 'f9n@protonmail.com',
    'url': 'https://github.com/f9n/docker-compose-expand',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.4,<4.0',
}


setup(**setup_kwargs)
