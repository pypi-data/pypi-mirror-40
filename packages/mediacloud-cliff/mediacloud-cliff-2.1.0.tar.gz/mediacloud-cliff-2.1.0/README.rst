Media CLoud CLIFF API Client
============================

This is a simple Python client for the `Media Cloud CLIFF-CLAVIN
geocoder <http://cliff.mediacloud.org>`__.

Usage
-----

If you just want to use this library to talk to a CLIFF server you have
running somewhere, first install it

::

    pip install mediacloud-cliff

Then instantiate and use it like this:

.. code:: python

    from cliff.api import Cliff
    my_cliff = Cliff('http://myserver.com:8080')
    my_cliff.parse_text("This is about Einstien at the IIT in New Delhi.")

This will return results like this:

.. code:: json

    {
      "results": {
        "organizations": [
          {
            "count": 1,
            "name": "IIT"
          }
        ],
        "places": {
          "focus": {
            "cities": [
              {
                "id": 1261481,
                "lon": 77.22445,
                "name": "New Delhi",
                "score": 1,
                "countryGeoNameId": "1269750",
                "countryCode": "IN",
                "featureCode": "PPLC",
                "featureClass": "P",
                "stateCode": "07",
                "lat": 28.63576,
                "stateGeoNameId": "1273293",
                "population": 317797
              }
            ],
            "states": [
              {
                "id": 1273293,
                "lon": 77.1,
                "name": "National Capital Territory of Delhi",
                "score": 1,
                "countryGeoNameId": "1269750",
                "countryCode": "IN",
                "featureCode": "ADM1",
                "featureClass": "A",
                "stateCode": "07",
                "lat": 28.6667,
                "stateGeoNameId": "1273293",
                "population": 16787941
              }
            ],
            "countries": [
              {
                "id": 1269750,
                "lon": 79,
                "name": "Republic of India",
                "score": 1,
                "countryGeoNameId": "1269750",
                "countryCode": "IN",
                "featureCode": "PCLI",
                "featureClass": "A",
                "stateCode": "00",
                "lat": 22,
                "stateGeoNameId": "",
                "population": 1173108018
              }
            ]
          },
          "mentions": [
            {
              "id": 1261481,
              "lon": 77.22445,
              "source": {
                "charIndex": 37,
                "string": "New Delhi"
              },
              "name": "New Delhi",
              "countryGeoNameId": "1269750",
              "countryCode": "IN",
              "featureCode": "PPLC",
              "featureClass": "P",
              "stateCode": "07",
              "confidence": 1,
              "lat": 28.63576,
              "stateGeoNameId": "1273293",
              "population": 317797
            }
          ]
        },
        "people": [
          {
            "count": 1,
            "name": "Einstien"
          }
        ]
      },
      "status": "ok",
      "milliseconds": 22,
      "version": "2.4.2"
    }

You can also just get info from the GeoNames database inside CLIFF:

.. code:: python

    from cliff.api import Cliff
    my_cliff = Cliff('http://myserver.com:8080')
    my_cliff.geonames_lookup(4943351)

This will give you results like this:

.. code:: json

    {
      "results": {
        "id": 4943351,
        "lon": -71.09172,
        "name": "Massachusetts Institute of Technology",
        "countryGeoNameId": "6252001",
        "countryCode": "US",
        "featureCode": "SCH",
        "featureClass": "S",
        "parent": {
          "id": 4943909,
          "lon": -71.39184,
          "name": "Middlesex County",
          "countryGeoNameId": "6252001",
          "countryCode": "US",
          "featureCode": "ADM2",
          "featureClass": "A",
          "parent": {
            "id": 6254926,
            "lon": -71.10832,
            "name": "Massachusetts",
            "countryGeoNameId": "6252001",
            "countryCode": "US",
            "featureCode": "ADM1",
            "featureClass": "A",
            "parent": {
              "id": 6252001,
              "lon": -98.5,
              "name": "United States",
              "countryGeoNameId": "6252001",
              "countryCode": "US",
              "featureCode": "PCLI",
              "featureClass": "A",
              "stateCode": "00",
              "lat": 39.76,
              "stateGeoNameId": "",
              "population": 310232863
            },
            "stateCode": "MA",
            "lat": 42.36565,
            "stateGeoNameId": "6254926",
            "population": 6433422
          },
          "stateCode": "MA",
          "lat": 42.48555,
          "stateGeoNameId": "6254926",
          "population": 1503085
        },
        "stateCode": "MA",
        "lat": 42.35954,
        "stateGeoNameId": "6254926",
        "population": 0
      },
      "status": "ok",
      "version": "2.4.2"
    }

Development
-----------

If you want to work on this API client, then first clone `the source
repo from GitHub <https://github.com/mitmedialab/CLIFF-API-Client>`__
and install the dependencies

::

    pip install -r requirements.pip

Then copy ``settings.config.sample`` to ``settings.config`` and put in
the url and port of your CLIFF server. Now you should be able to
develop!

Distribution
------------

1. Run ``python test.py`` to make sure all the test pass
2. Update the version number in ``cliff/__init__.py``
3. Make a brief note in the version history section in the README file
   about the changes
4. Run ``python setup.py sdist`` to test out a version locally
5. Then run ``python setup.py sdist upload -r pypitest`` to release a
   test version to PyPI's test server
6. Run ``pip install -i https://testpypi.python.org/pypi mediacloud``
   somewhere and then use it with Python to make sure the test release
   works.
7. When you're ready to push to pypi run
   ``python setup.py sdist upload -r pypi``
8. Run ``pip install mediacloud-cliff`` somewhere and then try it to
   make sure it worked.

Version History
---------------

-  **v2.1.0**: upgrade to CLIFF v2.4.2
-  **v2.0.2**: update examples in readme file
-  **v2.0.1**: init with url instead of host/port
-  **v2.0.0**: move to mediacloud naming, underscored method names,
   remove deprecated NLP endpoint
-  **v1.4.0**: upgrade to CLIFF v2.4.1, add support for extractContent
   endpoint
-  **v1.3.1**: updates for python3
-  **v1.3.0**: updates for python3, support for client-side text
   replacements
-  **v1.2.0**: points at CLIFF v2.3.0 (updates Stanford NER & has new
   plugin architecture)
-  **v1.1.0**: points at CLIFF v2.2.0 (adds ancestry to
   ``geonamesLookup`` helper)
-  **v1.0.2**: first release to PyPI
