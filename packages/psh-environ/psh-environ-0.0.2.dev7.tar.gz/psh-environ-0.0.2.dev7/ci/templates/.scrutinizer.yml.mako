checks:
  python:
    code_rating: true
    duplicate_code: true
    classes_valid_slots: true

build:
  environment:
    python: 3.6
  nodes:
    analysis:
      tests:
        override:
          - py-scrutinizer-run
    tests:
      tests:
        override:
          - true
filter:
  excluded_paths:
    - "*/test/*"
  dependency_paths:
    - "lib/*"
tools:
  external_code_coverage:<%
    from builtins import sorted, len
    items = [env for env, config in environments.items() if config["cover"]]
    comment = ", ".join(sorted(items))
    runs = len(items)
    timeout = runs * 90
%>
    # ${comment}
    runs: ${runs}
    # timeout in seconds, default 5 minutes
    timeout: ${timeout}
