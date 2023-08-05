#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function

from itertools import product

import attr
import inflection
import mako.template
import path
import yaml


@attr.s(slots=True, frozen=True)
class Entry(object):
    alias = attr.ib(type=str)
    value = attr.ib()

    @classmethod
    def from_value(cls, value):
        try:
            actual = value["value"]
        except TypeError:
            actual = value
            alias = inflection.parameterize(str(actual), "-")
        except KeyError:
            raise TypeError("Expected a value or a mapping with a `value` key.")
        else:
            try:
                alias = value["alias"]
            except KeyError:
                alias = inflection.parameterize(str(actual), "-")

        return cls(alias=alias, value=actual)

    def __str__(self):
        return self.alias


def resolve(data, root=None):
    if not isinstance(data, dict):
        if isinstance(data, list):
            for i, item in enumerate(data):
                data[i] = resolve(item, root)
        return data

    if root is None:
        root = data

    if "$ref" not in data:
        for key in data:
            data[key] = resolve(data[key], root)

        return data

    ref = data["$ref"]
    if ref.startswith("#"):
        return resolve_internal(ref, root)

    raise NotImplementedError(ref)


def resolve_internal(reference, data):
    if reference in ("", "#", "#/"):
        return data

    ref_path = reference[2:].split("/")
    ref_data = data
    for path_item in ref_path:
        ref_data = ref_data[path_item]

    return ref_data


def load_matrix(file_path=None):
    if file_path is None:
        file_path = path.Path("./.matrix.yml")

    with open(file_path) as fp:
        data = yaml.safe_load(fp)

    data["matrix"] = {
        name: [Entry.from_value(value) for value in options]
        for name, options in data["matrix"].items()
    }

    # resolve $ref
    data = resolve(data)
    rv = {}

    for env in data["environments"]:
        label = env.pop("label", None)
        matrix = env.pop("matrix", {})

        items = [(name, options) for name, options in matrix.items() if options]
        names = [name for name, options in items]
        if not label:
            label = "-".join("{{{}}}".format(name) for name in names)

        for combination in product(*(options for name, options in items)):
            combination = dict(zip(names, combination))

            name = label.format_map(combination)
            environment = env.copy()
            environment.update({k: v.value for k, v in combination.items()})
            rv[name] = environment

    return rv


def main():
    base_path = path.Path(__file__).dirname().dirname()
    print(("Project path: {}".format(base_path)))

    environments = load_matrix(base_path / ".matrix.yml")
    template_path = base_path / "ci" / "templates"
    templates = template_path.listdir()

    for tpl_path in templates:
        root, _ = tpl_path.basename().splitext()

        tpl = mako.template.Template(filename=str(tpl_path))
        contents = tpl.render(environments=environments).rstrip()
        with open(base_path / root, "w") as fp:
            fp.write(contents + "\n")

        print("Wrote {}".format(root))

    print("DONE.")


if __name__ == "__main__":
    main()
