# service-locator
Light python implementation of [service locator pattern](https://en.wikipedia.org/wiki/Service_locator_pattern) based on java [CDI](https://www.sitepoint.com/introduction-contexts-dependency-injection-cdi/) and [ServiceLoader](https://docs.oracle.com/javase/7/docs/api/java/util/ServiceLoader.html) api.

The [service locator pattern](https://en.wikipedia.org/wiki/Service_locator_pattern) is considered by some authors as an anti pattern, which recommend using [DI](https://en.wikipedia.org/wiki/Dependency_injection) (Dependency Injection), even so [Martin Fowler](https://martinfowler.com/articles/injection.html) recommends not demonizing it, and use it when it is convenient.

## Goals
* Define the **@ServiceProvider** [decorator](http://farmdev.com/src/secrets/decorator/index.html) to configure the [service locator registry](https://en.wikipedia.org/wiki/Service_locator_pattern) population by specifying a [marker interface](https://en.wikipedia.org/wiki/Marker_interface_pattern), an string [qualifier](https://docs.oracle.com/cd/E19798-01/821-1841/gjbck/index.html) and a [scope](https://en.wikipedia.org/wiki/Scope_(computer_science)).
* Define the **ServiceLocator** class, which is a [singleton](https://en.wikipedia.org/wiki/Singleton_pattern) that implements the [service locator registry](https://en.wikipedia.org/wiki/Service_locator_pattern). The **ServiceLocator** allows register and lookup implementations of a service.
* Define the **ServiceLookup** class, which is a [facade](https://en.wikipedia.org/wiki/Facade_pattern) of the **ServiceLocator** *lookup* method.

## Getting Started
### Prerequisites
* Python version: >= 3.4
* [setuptools](https://pypi.python.org/pypi/setuptools)

### Installing
```
git clone https://github.com/alexescalonafernandez/service-locator.git
cd service-locator
python setup.py sdist
cd dist
pip install service-locator-1.0.tar.gz
```

### Example
```python
# example_repository.py
from service_locator import qualifiers
from service_locator.decorators import ServiceProvider

@ServiceProvider(qualifiers.Repository, 'ExampleRepository')
class ExampleRepository:
    def do_action(self):
        print('do repository action')
```

```python
# example_controller.py
from service_locator import qualifiers
from service_locator.decorators import ServiceProvider
from service_locator.lookup import ServiceLookup

@ServiceProvider(qualifiers.Controller, 'ExampleController')
class ExampleController:
    def __init__(self, repository=ServiceLookup.proxy(qualifiers.Repository, 'ExampleRepository')):
        self.repository = repository
    
    def do_action(self):
        self.repository.do_action()
```

```python
# main.py
from service_locator import _command
from service_locator.lookup import ServiceLookup
from service_locator import qualifiers

# set here the main module path for scanning service providers
module_path = 'main module path'

# generate _services.py files with providers configuration
_command.generate_providers_configuration(module_path)


# import _services.py dynamically
_command.populate_service_locator_registry(module_path)

controller = ServiceLookup.lookup(qualifiers.Controller, 'ExampleController')
controller.do_action()
```

### ServiceLookup proxy vs lookup
The [proxy](https://en.wikipedia.org/wiki/Proxy_pattern) method differs from the *lookup* in that *lookup* requests an instance from the provider immediately, instead proxy returns a [dynamic proxy](https://en.wikipedia.org/wiki/Proxy_pattern) from the instance so that the instance is only created when any property or method of the instance representing by the **proxy** is invoked.

It is recommended to use the [proxy](https://en.wikipedia.org/wiki/Proxy_pattern) method in all [dependency injections](https://en.wikipedia.org/wiki/Dependency_injection) at the parameter level in all the scripts, which uses the **@ServiceProvider** decorator.
 
To understand the above, let's analyze what would happen if the **controller** class is loaded before the **repository** one. The **controller** would get a **null** instance because the [service locator registry](https://en.wikipedia.org/wiki/Service_locator_pattern) does not have any **provider** for the **repository**.

This means that the **order** in which the **_services.py** scripts are loaded is important. 
The [proxy](https://en.wikipedia.org/wiki/Proxy_pattern) method allows the [service locator registry](https://en.wikipedia.org/wiki/Service_locator_pattern) to work correctly regardless of the order in which the scripts are loaded.
Otherwise, it would be necessary to implement a [topological sort](https://en.wikipedia.org/wiki/Topological_sorting) of the scripts to be loaded.
