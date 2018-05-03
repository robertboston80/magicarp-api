import collections

from flask import Blueprint as FlaskBlueprint

from magicarp import exceptions


class Blueprint(FlaskBlueprint):
    def __init__(  # pylint: disable=too-many-arguments
            self, name, namespace='/', routes=None,
            static_folder=None, static_url_path=None, template_folder=None,
            subdomain=None, url_defaults=None, root_path=None):

        if not namespace.startswith('/'):
            raise exceptions.RoutingConfigurationError(
                "Namespace in blueprint has to start with forward slash")

        url_prefix = namespace[1:]

        super().__init__(
            name=name, import_name=name, url_prefix=url_prefix,
            static_folder=static_folder, static_url_path=static_url_path,
            template_folder=template_folder, subdomain=subdomain,
            url_defaults=url_defaults, root_path=root_path)

        self.routes = {}
        self.excludes = []
        self.namespace = namespace

        if routes is not None:
            self.extend(routes)

    def __iter__(self):
        for value in self.routes.values():
            yield value

    def as_list(self):
        return list(self.routes.values())

    def get_endpoint_by_name(self, name):
        return self.routes[name]

    def exclude(self, routes):
        for route in routes:
            name = getattr(route, 'name', str(route))

            if name in self.excludes:
                raise exceptions.RoutingConfigurationError(
                    "Route {} was excluded twice.".format(route.name))

            self.excludes.append(name)

        return self

    def extend(self, routes):
        for route in routes:
            self.add_route(route)

        return self

    def add_route(self, route):
        if route.name in self.routes:
            raise exceptions.DuplicateRouteException(
                "Given route {} is already set on Blueprint".format(
                    route.name))

        self.routes[route.name] = route


class Url(object):
    url = '/'

    def add(self, part):
        if part.startswith('/'):
            part = part[1:]

        if not part.endswith('/'):
            part += '/'

        if part == '/':
            return

        self.url += part

    def as_full_url(self):
        if self.url.endswith('/'):
            return self.url

        return self.url + '/'


class Router(object):
    def __init__(self):
        self.versions = {}
        self.locked = False

    def _validate_version(self, version):
        if version is None:
            return

        if len(version) < 1:
            raise exceptions.RoutingConfigurationError(
                "Version requires to be a tuple-like object with "
                "at least one integer-like value, got: {}".format(version))

        for ver_number in version:
            try:
                int(ver_number)
            except (TypeError, ValueError):
                raise exceptions.RoutingConfigurationError(
                    "One of version numbers is not integer-like value, "
                    "got: {}".format(ver_number))

    def _validate_blueprints(self, blueprints):
        if not isinstance(blueprints, collections.Iterable):
            raise exceptions.RoutingConfigurationError(
                "Registering version requires to pass collection of "
                "blueprints that is iterable")

        not_a_blueprint = [
            blpr for blpr in blueprints if not isinstance(blpr, Blueprint)]

        if not_a_blueprint:
            raise exceptions.RoutingConfigurationError(
                "One of the blueprints on collection of blueprints is "
                "not a subclass of magicarp.router.Blueprint")

    def lock(self):
        self.locked = True

    def unlock(self):
        self.locked = False

    def _check_lock(self):
        if self.locked is True:
            raise exceptions.RoutingConfigurationError(
                "It's impossible to register new routes after app was "
                "already created")

    def _normalise_version(self, version):
        # to have an easy way to compare and sort versions we normalise then
        # into having always 3 elements, where missing elements will be always
        # -1
        if version is None:
            return None

        if len(version) < 2:
            version = (version[0], -1)

        if len(version) < 3:
            version = (version[0], version[1], -1)

        return tuple([int(ver) for ver in version])

    def register_version(self, version, blueprints):
        self._check_lock()

        self._validate_version(version)
        self._validate_blueprints(blueprints)

        normalised_version = self._normalise_version(version)

        self.versions[normalised_version] = blueprints

    def _merge_blueprints(
            self, blueprints, versionless_blueprints=None,
            previous_version=None):
        version = {}
        excludes = []
        # this is helper variable to be not forced to deepcopy versionless
        # blueprints
        namespace_processed = []

        for blueprint in blueprints:
            if blueprint.namespace not in version:
                version[blueprint.namespace] = {
                    '__master_blueprint__': blueprint,
                }

            version[blueprint.namespace].update(blueprint.routes)

            excludes = blueprint.excludes

            if versionless_blueprints and \
                    blueprint.namespace in versionless_blueprints:
                for name, endpoint in \
                        versionless_blueprints[blueprint.namespace].items():
                    if name in excludes or name == '__master_blueprint__':
                        continue

                    version[blueprint.namespace][name] = endpoint

                    namespace_processed.append(blueprint.namespace)

            if previous_version and \
                    blueprint.namespace in previous_version:

                for name, route in \
                        previous_version[blueprint.namespace].items():

                    if name in version[blueprint.namespace] or \
                            name in excludes:
                        continue

                    version[blueprint.namespace][name] = route

        if versionless_blueprints:
            for namespace, endpoints in versionless_blueprints.items():
                if namespace in namespace_processed:
                    continue

                version[namespace] = {}

                for name, endpoint in endpoints.items():
                    version[namespace][name] = endpoint

        return version

    def get_normalised_blueprints(self):
        """Rules:

         - versionless blueprints are always attached, but can be overriden or
            excluded
         - blueprints from previous versions are joined only if there is
           matching namespace and non-matching name of the endpoint
         - versionless blueprints never override anything, but can be overriden
        """
        versionless_blueprints = \
            self.versions.pop(None) if None in self.versions else []

        versions = list(self.versions.keys())
        versions.sort()

        tree = []

        if versionless_blueprints:
            tree.append({
                'version': None,
                'namespaces': self._merge_blueprints(versionless_blueprints),
            })

        # first resolve inheritance and extends/overrides/exclusions
        for version in versions:
            tree.append({
                'version': version,
                'namespaces': self._merge_blueprints(
                    self.versions[version],
                    tree[0]['namespaces'] if tree else {},
                    tree[-1]['namespaces'] if len(tree) > 1 else {}
                ),
            })

        # at this stage we should all inheritance resolved and we should be
        # working with semi-complex list of versions with namespaces holding
        # endpoints

        # all that needs to be done is to register each leaf as endpoint with
        # its master blueprint

        normalised_blueprints = []

        for version, blp in [
                (dct['version'], dct['namespaces']) for dct in tree]:

            version_as_string = '' if version is None else '.'.join(
                [str(ver) for ver in version if ver != -1])

            for namespace, endpoints in blp.items():
                url = Url()

                if version_as_string:
                    url.add(version_as_string)

                url.add(namespace)

                url_prefix = url.as_full_url()[:-1]

                master_blueprint = endpoints.pop('__master_blueprint__')

                for name, endpoint in endpoints.items():
                    url = Url()
                    url.add(endpoint.url)

                    master_blueprint.add_url_rule(
                        url.as_full_url(), name, endpoint,
                        methods=endpoint.methods)

                normalised_blueprints.append((master_blueprint, url_prefix))

        return normalised_blueprints
