import pathlib


class Vulcan:

    def __init__(self, services=[], root_dir=__file__):
        self._services = {}
        self._register_services(services)
        self._root_dir = root_dir

    def fetch(self, elements=[], context={}):
        results = []
        for element in elements:
            service = self._match_service(element)
            try:
                results.append(service.init(context))
            except Exception as e:
                raise VulcanFetchError("Failed to fetch from service", e)
        return results

    def _register_services(self, services):
        """Register services to Vulcan instance.
        services: List(VulcanService)
        """
        for (service_name, service) in services:
            self._services[service_name] = service(vulcan=self)

    def _match_service(self, service):
        return self._services.get(service)


def initialize(services=[], root_dir=__file__):
    return Vulcan(services, root_dir=root_dir)


# Errors
class VulcanFetchError(Exception):
    def __init__(self, message, errors):
        super().__init__(message)
        self.errors = errors
