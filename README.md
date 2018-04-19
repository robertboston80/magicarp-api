# magicarp-api

## About project

Magicarp is a set of building blocks that will allow anyone to run complex
restful api in matter of minutes. It's not complete framework (don't think
about it as a Django) but more like tools build upon Flask. Certain design
decision have been made for you and all that is left to prepare business logic
that actually delivers value.

Example features that part of this:

 - Flask app factory that allows further customisation
 - certain subsystems preliminary configured and ready to use:

    * logging
    * user-session handling
    * exception handling

 - routing
 - schema for input/output (self documentation is part of the goal)
 - validation and sanitisation of incoming data

## Installation

`pip install magicarp-api`

NOTE: application is aimed to by python 3.5+ only
