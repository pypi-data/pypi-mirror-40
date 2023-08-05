[tox]
envlist =
    clean,
    # docs,
% for env in sorted(environments):
    ${env},
% endfor
    report

[testenv]
setenv =
    PYTHONUNBUFFERED=yes
passenv =
    *
deps =
    pytest

[testenv:docs]
deps =
    -r{toxinidir}/docs/requirements.txt
commands =
    sphinx-build {posargs:-E} -b doctest docs dist/docs
    sphinx-build {posargs:-E} -b html docs dist/docs
    sphinx-build -b linkcheck docs dist/docs

[testenv:coveralls]
deps =
    coveralls
skip_install = true
commands =
    coveralls

[testenv:codecov]
deps =
    codecov
skip_install = true
commands =
    coverage xml --ignore-errors
    codecov []

[testenv:ocular]
deps =
    scrutinizer-ocular
skip_install = true
commands =
    ocular

[testenv:codacy]
deps =
    codacy-coverage
skip_install = true
commands =
    python-codacy-coverage -r coverage.xml

[testenv:report]
deps =
    coverage
skip_install = true
commands =
    coverage report
    coverage html

[testenv:clean]
deps =
    coverage
skip_install = true
commands = coverage erase

% for env, config in sorted(environments.items()):
[testenv:${env}]
% if env.startswith("check"):
skip_install = true
commands =<% python_files = "setup.py ci psh_environ tests" %>
    bandit --verbose --configfile=bandit.yml --recursive --aggregate file ${python_files}
    flake8 --verbose ${python_files}
    black --verbose --check --diff ${python_files}
    isort --verbose --check-only --diff --recursive ${python_files}
% endif
% if config.get("env_vars"):
setenv =
    {[testenv]setenv}
% endif
% for var, value in sorted(config.get("env_vars", {}).items()):
    ${var}=${value}
% endfor
% if config.get("cover", True):
usedevelop = true
commands =
    {posargs:pytest --cov --cov-report=term-missing -vv}
% elif env.startswith("py"):
commands =
    {posargs:pytest -vv}
% endif
% if config.get("cover", True) or config.get("deps", []):
deps =
% if not env.startswith("check"):
    {[testenv]deps}
% endif
% endif
% if config.get("cover", True):
    pytest-cov
% endif
% for dep in config.get("deps", []):
    ${dep}
% endfor

% endfor
