==================
Flask Behind Proxy
==================


Provide a middleware for Flask application, to fix redirection issue when the application runs behind a reverse proxy, like Nginx.

The redirection issue is that, when your website is HTTPS and a *view* returns a 301/302 reponse, the new URL mistakenly becomes HTTP.

This resolution requires you to configure Nginx so that it passes a custom header, to inform the scheme (HTTPS) of the original request. To do that, you just need to setup like this in your Nginx virtualhost config:

.. code-block:: nginx

    location / {
        include         proxy_params;
        proxy_pass      http://localhost:8000;
    }

This is the common setup for Nginx on Debian/Ubuntu. Nginx on other distros may not have *proxy_params* file, you can add configuration like this:

.. code-block:: nginx

    location / {
        proxy_pass       http://localhost:8000;
        proxy_set_header Host              $http_host;
        proxy_set_header X-Real-IP         $remote_addr;
        proxy_set_header X-Forwarded-For   $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

Currently, *Flask Behind Proxy* is only tested with Nginx web server.

Other implementation
--------------------

Other implementation is `Flask Reverse Proxy <https://github.com/wilbertom/flask-reverse-proxy>`_. It is based on a header name that is not "standard" (in my sense, it is the name chosen by Debian/Ubuntu maintainer). I chose to make a new software myself, instead of contributing to *Flask Reverse Proxy*, because **wilbertom** seems not to be very reactive, and I want to have a clean code, without Python 2 backward compatibility, and newer tool (like *pyproject.toml* file).
