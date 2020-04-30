# Django CMS Forms

![Test pipeline](https://github.com/sim1234/cms_forms/workflows/Test%20pipeline/badge.svg)
[![codecov](https://codecov.io/gh/sim1234/cms_forms/branch/master/graph/badge.svg?token=SP8ZN53C11)](https://codecov.io/gh/sim1234/cms_forms)
[![pypi](http://img.shields.io/pypi/v/django-cms-forms.svg?style=flat-square)](https://pypi.python.org/pypi/django-cms-forms/)

Source: [https://github.com/sim1234/cms_forms/](https://github.com/sim1234/cms_forms/)


## Installation 

 - Install `django-cms-forms` package.
 - Add `cms_forms` to `INSTALLED_APPS` django setting.
 - Add `path("forms/", include("cms_forms.urls"))` to your main url config.

## Configuration

Configure this package by setting these variables in your django settings.
All settings are optional. The default values can be imported from `cms_forms.config_defaults`.

`CMS_FORMS_REGISTER_PLUGINS`: bool - A flag indicating if the package should register to cms all plugins mentioned in the following lists.

`CMS_FORM_PLUGINS`: List[str] - List of dot delimited paths to form plugins. 

`CMS_FIELD_PLUGINS`: List[str] - List of dot delimited paths to form field plugins. 

`CMS_WIDGET_PLUGINS`: List[str] - List of dot delimited paths to field widget plugins.

`CMS_CHOICE_OPTION_PLUGINS`: List[str] - List of dot delimited paths to choice option plugins.

`CMS_CHOICE_FIELD_PLUGINS`: List[str] - List of dot delimited paths to choice field plugins.

`CMS_BUTTON_PLUGINS`: List[str] - List of dot delimited paths to button plugins.


## Documentation

TODO


## Contributing

Feel free to propose any change, as long as it tested and passes the repo checks.

Here is a simple guide to development installation of the project:

```
git clone https://github.com/sim1234/cms_forms.git && cd cms_forms
apt-get install python3.8 docker docker-compose  # these are system requirements
python3.8 -m venv venv && source venv/bin/activate
export PYTHONPATH=$PYTHONPATH:$(pwd)/examples
export DJANGO_SETTINGS_MODULE=installation.settings
pip install -r requirements-test.txt
flake8 .
black --line-length 120 .
pytest --cov cms_forms tests
docker-compose down && docker volume prune -f && docker-compose up --build --abort-on-container-exit # run selenium tests
```
 
The project  is automatically built on tag push and a new release is published.
 
