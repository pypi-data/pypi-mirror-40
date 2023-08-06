# -*- coding:utf-8 -*-


import ast
import re
from typing import Any

import pydash as py_
from jinja2 import Environment, BaseLoader
from owlmixin import TOption


def exact_match(target: str, regexp: str):
    return bool(re.search(f'^{regexp}$', target))


def get_by_diff_key(d: dict, diff_key: str) -> Any:
    return py_.get(d, diff_key
                   .replace("root", "")
                   .replace("><", ".")
                   .replace(">", "")
                   .replace("<", "")
                   .replace("'", ""))


env = Environment(loader=BaseLoader())
env.filters['reg'] = exact_match


def when_filter(when: str, data: dict) -> bool:
    return ast.literal_eval(env.from_string('{{' + when + '}}').render(data))


def when_optional_filter(when: TOption[str], data: dict) -> bool:
    return when.map(lambda x: when_filter(x, data)).get_or(True)


def jinja2_format(fmt: str, data: dict) -> str:
    return env.from_string(fmt).render(data)
