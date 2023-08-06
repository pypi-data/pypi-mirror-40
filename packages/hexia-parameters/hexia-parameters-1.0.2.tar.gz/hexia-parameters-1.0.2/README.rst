================
Hexia Parameters
================

Hexia Parametersges is a Django app to provide the ability to change specific site parameters from admin.
This will allow the user to change background images, site title etc by specifying the parameter and then using
the parameter within the Django templates.  

Detailed documentation is needs writing.

Quick start
-----------

1. pip install hexia-parameters

2. Add "hexia_parameters" and dependencies to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'hexia_pages',
    ]

3. Add "hexia_parameters" to your coontext processors

    'OPTIONS': {
        'context_processors': [
            ...
            'hexia_parameters.context_processors.hexia_parameters',
        ],
    }


4. Run `python manage.py migrate` to create the hexia_parameters models.

5. Add the parameters you want generated to settings.py

    HEXIA_PARAMETERS_LIST = [
        'Site_Title',
        'Tag_Line',
        'Banner',
        'Video',
    ]

6. Run `python manage.py initialise_hexia_parameters` to create these records

7. Start the development server and visit http://127.0.0.1:8000/admin/
   to enter initial values.

8. Add a parameter your templates.

    {{ Site_Title.text }}
