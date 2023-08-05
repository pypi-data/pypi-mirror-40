# -*- coding: utf-8 -*-
from distutils.core import setup

modules = \
['flask_behind_proxy']
setup_kwargs = {
    'name': 'flask-behind-proxy',
    'version': '0.1.0',
    'description': 'Flask middleware to fix HTTPS redirection behind reverse proxy.',
    'long_description': '==================\nFlask Behind Proxy\n==================\n\n\nProvide a middleware for Flask application, to fix redirection issue when the application runs behind a reverse proxy, like Nginx.\n\nThe redirection issue is that, when your website is HTTPS and a *view* returns a 301/302 reponse, the new URL mistakenly becomes HTTP.\n\nThis resolution requires you to configure Nginx so that it passes a custom header, to inform the scheme (HTTPS) of the original request. To do that, you just need to setup like this in your Nginx virtualhost config:\n\n.. code-block:: nginx\n\n    location / {\n        include         proxy_params;\n        proxy_pass      http://localhost:8000;\n    }\n\nThis is the common setup for Nginx on Debian/Ubuntu. Nginx on other distros may not have *proxy_params* file, you can add configuration like this:\n\n.. code-block:: nginx\n\n    location / {\n        proxy_pass       http://localhost:8000;\n        proxy_set_header Host              $http_host;\n        proxy_set_header X-Real-IP         $remote_addr;\n        proxy_set_header X-Forwarded-For   $proxy_add_x_forwarded_for;\n        proxy_set_header X-Forwarded-Proto $scheme;\n    }\n\nCurrently, *Flask Behind Proxy* is only tested with Nginx web server.\n\nOther implementation\n--------------------\n\nOther implementation is `Flask Reverse Proxy <https://github.com/wilbertom/flask-reverse-proxy>`_. It is based on a header name that is not "standard" (in my sense, it is the name chosen by Debian/Ubuntu maintainer). I chose to make a new software myself, instead of contributing to *Flask Reverse Proxy*, because **wilbertom** seems not to be very reactive, and I want to have a clean code, without Python 2 backward compatibility, and newer tool (like *pyproject.toml* file).\n',
    'author': 'Nguyễn Hồng Quân',
    'author_email': 'ng.hong.quan@gmail.com',
    'url': 'https://bitbucket.org/hongquan/flask-behind-proxy/',
    'py_modules': modules,
    'python_requires': '>=3.4,<4.0',
}


setup(**setup_kwargs)
