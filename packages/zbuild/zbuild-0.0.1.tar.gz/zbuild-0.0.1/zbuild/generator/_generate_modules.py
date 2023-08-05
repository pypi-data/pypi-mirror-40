#!/usr/bin/python
# -*- coding: UTF-8 -*-

try:
    import queue
except ImportError:
    import Queue as queue
from functools import reduce
from operator import itemgetter, attrgetter

def get_generate_modules(modules):
    module_dirt = {}
    for module in modules:
        module_dirt[module.name] = module

    generate_modules = list()
    module_queue = queue.Queue()
    for module in modules:
        this_dependency_modules = list()
        module_queue.put(module)
        while not module_queue.empty():
            this_dependency_module = module_queue.get()
            if generate_modules.count(this_dependency_module) == 0 and this_dependency_module.configuration_type != '':
                generate_modules.append(this_dependency_module)
            if (this_dependency_modules.count(this_dependency_module) > 0):
                continue
            this_dependency_modules.append(this_dependency_module)
            for dependency_module_name in this_dependency_module.dependency_module_names:
                if module_dirt.get(dependency_module_name, None) == None:
                    continue
                dependency_module = module_dirt[dependency_module_name]
                module_queue.put(dependency_module)
                module.public_include_paths.extend(dependency_module.public_include_paths)
                module.public_preprocessed_files.extend(dependency_module.public_preprocessed_files)
                module.public_definitions.extend(dependency_module.public_definitions)
            for third_party_name in this_dependency_module.public_third_party_dependencies:
                if module_dirt.get(third_party_name, None) == None:
                    continue
                dependency_module = module_dirt[third_party_name]
                module_queue.put(dependency_module)
                module.public_include_paths.extend(dependency_module.public_include_paths)
                module.runtime_dependencies.extend(dependency_module.runtime_dependencies)
                module.static_dependencies.extend(dependency_module.static_dependencies)
            for third_party_name in this_dependency_module.private_third_party_dependencies:
                if module_dirt.get(third_party_name, None) == None:
                    continue
                dependency_module = module_dirt[third_party_name]
                module_queue.put(dependency_module)
                module.private_include_paths.extend(dependency_module.public_include_paths)
                module.runtime_dependencies.extend(dependency_module.runtime_dependencies)
                module.static_dependencies.extend(dependency_module.static_dependencies)
            for include_path_module_name in this_dependency_module.include_path_module_names:
                if module_dirt.get(include_path_module_name, None) == None:
                    continue
                dependency_module = module_dirt[include_path_module_name]
                module_queue.put(dependency_module)
                module.public_include_paths.extend(dependency_module.public_include_paths)
        this_dependency_modules.clear()

    # Dependency ref count
    module_queue.queue.clear()
    for module in generate_modules:
        module_queue.put(module)
        while not module_queue.empty():
            dependency_module = module_queue.get()
            dependency_module.dependency_ref_count += 1
            for dependency_module_name in dependency_module.dependency_module_names:
                if module_dirt.get(dependency_module_name, None) == None:
                    continue
                if dependency_module_name == module.name:
                    continue
                module_queue.put(module_dirt[dependency_module_name])
            for include_path_module_name in dependency_module.include_path_module_names:
                if module_dirt.get(include_path_module_name, None) == None:
                    continue
                if include_path_module_name == module.name:
                    continue
                module_queue.put(module_dirt[include_path_module_name])

    return sorted(generate_modules, key=attrgetter('dependency_ref_count'), reverse=True)
