from enum import Enum


class Singleton:
    """
    Decorator for add singleton pattern support

    @author: Alexander Escalona Fernández 
    """

    def __init__(self, decorated):
        """
        :param decorated: class to convert to singleton 
        """
        self._decorated = decorated

    def instance(self):
        """
        :return: the singleton instance of decorated 
        """
        try:
            return self._instance
        except AttributeError:
            self._instance = self._decorated()
            return self._instance

    def __call__(self):
        raise TypeError('Singletons must be accessed through `instance()`.')

    def __instancecheck__(self, inst):
        return isinstance(inst, self._decorated)


@Singleton
class ServiceLocator:
    """
    Implementation of service locator pattern. It represents the Registry of service locator and as such is a Singleton.

    @author: Alexander Escalona Fernández
    """

    def __init__(self):
        """
        Initialize the registry data structure.
        """
        self.services = {}

    def register(self, service, serviceImpl, serviceImplQualifier):
        """
        Register a service implementation with a given qualifier
        :param service: the marker interface to group implementations
        :param serviceImpl: the implementation of the given marker interface
        :param serviceImplQualifier: the qualifier string that identifies the implementation
        :return: 
        """
        if service not in self.services:
            self.services[service] = {}
        if serviceImplQualifier in self.services[service]:
            raise RuntimeError(
                'There is a ' + serviceImplQualifier + ' qualifier for ' + service + ' instance in service locator')
        self.services[service][serviceImplQualifier] = serviceImpl

    def lookup(self, service, qualifier=''):
        """

        :param service: the marker interface to group implementations
        :param qualifier: the qualifier string that identifies the implementation
        :return: the implementation of the given marker interface with the given qualifier
        """
        if service not in self.services:
            return None
        if qualifier not in self.services[service]:
            return None
        return self.services[service][qualifier]()


class Scope(Enum):
    PROTOTYPE = 1
    SINGLETON = 2


class ServiceProvider:
    """
    Decorator to populate the ServiceLocator

    @author: Alexander Escalona Fernández
    """

    def __init__(self, service, qualifier='', scope=Scope.PROTOTYPE):
        """

        :param service: the marker interface to group implementations
        :param qualifier: the qualifier string that identifies the implementation
        :param scope: the scope of instance, if prototype create one each time is requested, if singleton 
        the instance acts as a singleton
        """
        self._service = service
        self._qualifier = qualifier
        if isinstance(scope, Scope):
            self._scope = scope
        else:
            raise ValueError("The scope argument value is incorrect. Uses Scope enum class for set this parameter.")

    def __call__(self, provider):
        """

        :param provider: the implementation of the given marker interface, which will be registered
         in the Service Locator
        :return: 
        """

        def prototype(constructor):

            def factory():
                return constructor()

            return factory

        def singleton(instance):

            def _instance():
                return instance

            return _instance

        if self._scope == Scope.SINGLETON:
            ServiceLocator.instance().register(self._service, prototype(provider), self._qualifier)
        else:
            ServiceLocator.instance().register(self._service, singleton(provider()), self._qualifier)


class ServiceProxy(object):
    """
    Create a proxy for service implementation. The goal of this class is only lookup in the Service Locator
    registry when is needed.

    @author: Alexander Escalona Fernández
    """

    def __init__(self, service, qualifier=''):
        self._service = service
        self._qualifier = qualifier
        self._implementation = None

    def __getattr__(self, item):
        if object.__getattribute__(self, "_implementation") is None:
            setattr(self, "_implementation", ServiceLookup.lookup(self._service, self._qualifier))
        return getattr(object.__getattribute__(self, "_implementation"), item)


class ServiceLookup:
    """
    Facade to lookup implementation from service locator registry

    @author: Alexander Escalona Fernández
    """

    @staticmethod
    def lookup(service, qualifier=''):
        """
        Returns if exists, an implementation from Service Locator registry
        :param service: the marker interface to group implementations
        :param qualifier: the qualifier string that identifies the implementation
        :return: the implementation of the given marker interface with the given qualifier
        """
        return ServiceLocator.instance().lookup(service, qualifier)

    @staticmethod
    def proxy(service, qualifier=''):
        return ServiceProxy(service, qualifier)
