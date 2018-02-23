import os
import re


def generate_providers_configuration(module_path):
    compiled_re = re.compile('^\s*@(\w+\.)*ServiceProvider\s*\(.*$')
    _hash = {}
    for root, dirs, files in os.walk(module_path):
        for f in files:
            name, ext = os.path.splitext(f)
            if ext == '.py':
                if name == '_services':
                    os.remove(os.path.join(root, f))
                else:
                    with open(os.path.join(root, f), encoding="utf8") as in_file:
                        for line in in_file:
                            if compiled_re.search(line):
                                if root not in _hash:
                                    _hash[root] = []
                                _hash[root].append(name)
                                break
    for key, values in _hash.items():
        path = os.path.join(key, '_services.py')
        print("Creating %s file" % path)
        with open(path, 'w+') as out_file:
            for e in values:
                out_file.write("from . import %s\n" % e)


def populate_service_locator_registry(module_path):
    for root, dirs, files in os.walk(module_path):
        for f in files:
            if f == '_services.py':
                import_path = root
                while os.path.isfile(os.path.join(import_path, '__init__.py')):
                    import_path = os.sep.join(import_path.split(os.sep)[:-1])
                __import__("%s.%s" % (os.path.relpath(root, import_path).replace(os.sep, '.'), '_services'))
