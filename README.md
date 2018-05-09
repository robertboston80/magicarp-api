# magicarp-api

## About project

Magicarp Api is a micro-framework, built on top of Flask and it's blueprints.
Main goal is remove burden of starting new project and just allow developer to
jump into endpoints creation. This is achieved by providing default setup that
is easy to use, however at will can be replaced or extended.

Main features are:
    - routing that is capable of understanding versions
    - input/output schema (lousily based upon JSON-schema) that enforces very
      strict and verbose error handling on input/output
    - self discovery and self documentation
    - hassle free defaults for cosmological constants like logging, error
      handling and uses sessions handling

## Installation && Usage

### Install

Via pypi:

    `pip install magicarp-api`

Or from source code:

    `git@github.com:Drachenfels/magicarp-api.git`

### Usage

After pip install, create `api/server.py` that will contain following code:

```
    from magicarp.server_tools import create_app

    app = create_app()
```

And then according to flask documentation, application can be started as:

```
    #!/usr/bin/env bash

    export FLASK_APP=api.server
    flask run
```

On default magicarp exposes endpoint that maps all urls and ping that reply
with pong. The earlier helps with discovery (and debug) the later allows to
health check api server (for CI, tests or debug).

In order to get new endpoints, you have to register new blueprint(s) that
describes them. It has to be done before server is up, for example good place
might be __init__ of main sub-package. Note: in theory it is possible, but in
practice bad idea to manipulate routing once server is running.


In `api/__init__.py`:

```
    from magicarp.routes import routing

    from api.routes import v1, non_versioned

    routing.register_version((1,), v1.blueprints)
    routing.register_version(None, non_versioned.blueprints)
```

First argument is version, if we specify None it means endpoint is not
versioned (and always available), if version is what we expect, argument
supposed to be tuple that is 1 to 3 elements long, each of them as positive
integer.

Second argument is a list of `Blueprints`, magicarp's Blueprints are extension
of standard Blueprints provided by Flask.

Following example that was presented so far your directory tree can be among those lines:

```
 |
 |-> bin/
        |
        | -> start_app.sh
 |
 |-> api/
        |
        | -> __init__.py
        | -> server.py
        |
        | -> v1
            |
            | -> __init__.py
            | -> user.py
            | -> product.py
        |
        | -> non_versioned
            |
            | -> __init__.py
            | -> postcode.py
```

In `api/v1/__init__.py` we need to define list of blueprints, for example:

```
    from . import user, product

    blueprints = (
        user.blueprint,
        product.blueprint,
    )
```

In `api/non_versioned/__init__.py` we need to define list of blueprints, for example:

```
    from . import postcode

    blueprints = (
        postcode.blueprint,
    )
```

Where blueprint is defined as follows:

In `api/v1/user.py`:

```
    from flask import Blueprint, request, url_for

    from magicarp import router, endpoint, response

    from api import business_logic, schema


    class CreateUser(endpoint.BaseEndpoint):
        # this defines url for endpoint, keep in mind that prefix and namespace
        # are taken into account automatically, so in our case this particular
        # url it will be expanded to /1/user/
        url = '/'

        # name of endpoint, has to be unique, per blueprint, used in case you
        want to override endpoint from previous version
        name = 'create_config'

        # optional input schema, all incomming data will be validated and
        # sanitised against it
        input_schema = schema.accept.user.User

        # optional output schema, whatever action method returns will be
        # injected into this schema (and may cause exception if it makes no or
        # little sense)
        output_schema = schema.reply.general.ResourceCreated

        # response is handling http response code and general wrapping of
        response, it's optional
        response = response.create_response

        # which methods this endpoint serves
        methods = ['POST']

        # syntactic sugar, when we set input schema, instance of schema
        # populated with data from request will be passed to method action() as
        # input_schema, by changing argument_name we can modify it to something
        # more readable
        argument_name = 'user_schema'

        # this is where the business logic should live
        def action(self, user_schema):  # pylint: disable=arguments-differ
            # assumption here is that our business logic create_user accepts
            # all fields from user_schema, and returns dictionary
            dct_user = business_logic.user.create_user(
                **user_schema.as_dictionary())

            # because blueprint is only extension of flask, we can use it for
            # functions like url_for and etc
            details_url = "{}.{}".format(request.blueprint, 'get_user_by_uid')

            # add extra fields to dictionary that business logic has returned
            dct_user.update({
                "message": "Configuration created.",
                "url": url_for(details_url, uid=configuration['uid']),
            })

            # by returning dct_user, we allow our output_schema to retrieve
            # whatever it needs and fullfill contract on what was promised to
            # be a reply (or throw exception if unable to do so)
            return instance


    blueprint = router.Blueprint(
        __name__, namespace='/user', routes=[
            CreateUser(),
        ])
```

That shortly describes how to add new endpoints. However one may ask question
what is input_schema, output_schema, responses and etc. How to register my own
error handlers and etc.

If you want to learn more, head to api-scaffold that demo's majority of the features available in the framework:

    * https://github.com/Drachenfels/api-scaffold

### Notes on versioning

One of new additions to Flask's blueprint is idea of namespace, if given namespace is shared on same version, their endpoints are merged together. But if they are occupy different versions, it's when inheritance kicks in.

Imagine following structure:

```
    v1:
        /user
            - /U-A
            - /U-B
        /product
            - /P-A
            - /P-B

    v2:
        /user
            - /U-B (override version v1)

    v3:
        /user
            - /U-C

        /product
            - /P-A
            - /P-C
```

Endpoints visible for a flask will be:

    * /1/user/U-A
    * /1/user/U-B
    * /1/product/P-A
    * /1/product/P-B

    * /2/user/U-A
    * /2/user/U-B (override version v1)

    * /3/user/U-A
    * /3/user/U-B (override version v1)
    * /3/user/U-C
    * /3/product/P-A
    * /3/product/P-C

Because there is gap in product namespace on v2, inheritance was broken and v3 will behave like it never existed.

## Issues:

To report feature requests or issues, visit:

    * https://github.com/Drachenfels/magicarp-api/issues


## Notes:

Project is still in active development and is not yet production ready, expected timeframe for being feature complete is end of June 2018.
