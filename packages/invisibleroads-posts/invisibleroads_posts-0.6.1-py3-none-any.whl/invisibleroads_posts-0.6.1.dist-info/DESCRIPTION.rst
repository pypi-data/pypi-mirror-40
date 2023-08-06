InvisibleRoads Posts
====================
Posts form the foundation for most of our web applications.

Prepare environment. ::

    export VIRTUAL_ENV=~/.virtualenvs/crosscompute
    virtualenv ${VIRTUAL_ENV}
    source ${VIRTUAL_ENV}/bin/activate

Install package. ::

    PYTHON_PACKAGE=~/Projects/invisibleroads-packages/posts
    NODE_PACKAGE=${PYTHON_PACKAGE}/node_modules/invisibleroads-posts

    cd ~/Projects
    git clone git@github.com:invisibleroads/invisibleroads-posts

    cd ${PYTHON_PACKAGE}
    ${VIRTUAL_ENV}/bin/pip install -e .

Create project. ::

    cd ~/Projects
    ${VIRTUAL_ENV}/bin/pcreate -s ir-posts xyz

Install project. ::

    cd ~/Projects/xyz
    ${VIRTUAL_ENV}/bin/pip install -e .

Launch development server. ::

    ${VIRTUAL_ENV}/bin/pserve development.ini

Launch production server. ::

    ${VIRTUAL_ENV}/bin/pserve production.ini

0.6
---
- Replace emphasis with highlighted

0.5
---
- Add base_url
- Add test fixtures for downstream packages
- Bundle css and js from website.dependencies with cache busting
- Define get_record_id
- Let templates override page_author, copyright_year, copyright_author
- Replace expiration_time with expiration_time_in_seconds

0.4
---
- Add confirmation_modal
- Add page_description
- Fix Python 3 compatibility

0.3
---
- Add extensible command line script

0.2
---
- Replace mako with jinja2

0.1
---
- Add posts scaffold

