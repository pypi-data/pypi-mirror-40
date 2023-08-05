# Repeat Queries


Smart Queries is a django package which helps django developer to avoid the N+1 queries issue by recording it and keeping a track of it per request.


### Quick start
-----------

1. Add "repeat_queries" to your INSTALLED_APPS setting like this::
    ```
    INSTALLED_APPS = [
        ...
        'repeat_queries',
    ]
    ```
2. Add 'repeat_queries.middleware.DuplicateQueryMiddleware', to your MIDDLEWARE settings like this ::
    ```
    MIDDLEWARE = [
        ...,
        'repeat_queries.middleware.DuplicateQueryMiddleware',
    ]
    ```

2. Include the repeat_queries URLconf in your project urls.py like this::
    For Django version > 2.0
    ```
    path('repeat_queries/', include('repeat_queries.urls')),
    ```
    For earlier versions
    ```
    url(r'^repeat_queries/', include('repeat_queries.urls')),
    ```

3. Run `python manage.py migrate` to create the repeat_queries models.

4. Start the development server, Hit any endpoint/view and visit http://127.0.0.1:8000/admin/ to see your data.


Contributing
------------

1. Check for open issues or open a fresh issue to start a discussion around a feature idea or a bug. 
2. Fork [the repository](https://github.com/siddhism/smart-queries/) on GitHub to start making your changes to the master branch (or branch off of it).
3. Write a test which shows that the bug was fixed or that the feature works as expected.
4. Send a pull request and bug the maintainer until it gets merged and published. :)
