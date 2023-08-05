language: python
sudo: false
cache: pip

env:
  global:
    - LD_PRELOAD=/lib/x86_64-linux-gnu/libSegFault.so
    - SEGFAULT_SIGNALS=all
    # CODECOV_TOKEN
    - secure: "DoVD6zudq6lSMtAd8pBd/4vPX6Us3FRO5NV74YhbPQImI4/pDtRNMKKgtyXAaMkJQKMfQ1TLwJ6ERIv0istE6pQClewh1TYm4gOJ7nCFOjAv+IvFB2hUMXarWsZwwkyYbxZ97agQaLdF3SbKrgEnBYJ9T5rlIOxPjZOpazjAndGkqxUDJ2LlV8Re5LF/WwPAfqp0bUs0qNZALD8n0hl3Z3mntm8BhfziNHxbFAbHr/Dz/So7ec5I/GR/Xh1nLbhBL8kSwaqSqRoEPiQe4hmvw9zV55ZgbeiZTIdmDLeEyktu9YEzB3SbjohHlyAb0yY5bX9U1tfxX+Wamg5eVu2PpGl51v/AjkripqtIiwiMbriQK0swOkML35quSS6YzE0sWYM1j85d5CW4oPH4ki1Gq0wGBrlQecE2BBw3cW52QF2+hNFQy3BT5OjnPpoQyhW5DTol4HOjFY+TFkKNPGV+dEfdCJemqjJqvJRE5hCoQYHy0kGasVtvC0IWCztkmFOOhwhIbE1XSD0qxBHiTBH6EYBNuXjwyP/k+XZ+Ughk02rtqUfi5dNxUoqo4nABQ8gcxaY1Ch71MHxzemnJTRvk8TzAOlJQVCszmFwvIlJ3jBrRWnz7Ic4SWUxZ5GrSiJAa85QHztCk3OJIIlZbh4P+v8jOW3E/ngVpDkzzHj6rv3w="
    # CC_TEST_REPORTER_ID
    - secure: "r6XE2dCXhftWpH/KZzEW4bBv2W1bYkeeDwhSawjB4+YA5SBoQn21icx/mKnbmSNrz8PpaLo39IMmsMAeFv4i2UO+ai41KscWT7v2xHj5t7fxosnqfFqWr00a67hUfIPm+M9irzfeI8HoOf9qKFIGmfzlIKQ7eMlMygo7UfshMNXzENW6PP9g3p56o08W7Y9/0LQUvo/xNs1v03dOEJcxCOSyt5cB1m3zP0U6btb2V7EzwVpge58K0ISDS5lsWJW0DTvCHM2pwgF0uTMR2ilSzXsyB9mU2K2srossfjN/iPGi+HcEdjuGAzGABsExz3Ii7mrOS3JBPXVT4We9Unm/c2gC4jvlF0lZGYZHGPM0Jstu2yJzIOSmED4Cft2g0CXcy5d6kMU8iv4E7v44A29ESuurpPO5jW6/41DvyGzU89UyEdfgIyR5Q3Ht3MOt9RCWM/7ivSVNU1ISSwaKYdWYZEcR0e4yIEr/EG6fkAo7vCy9AVlEb/+WZ1w7lCCR+mFbubza8RhO/7OljDHyOZN6gDuae9Xs4cTOmnNmXC2//Rw5OnV0Uiav7rczX1oA9RnPsDm84shDML6eYjpSCEIhNdIVP0FegeaA1tXiy0vdhylPVfdOzN+nj2nO2XxV9VrxLJ7S5zz4GgaUX9o0Nmk4oFSZEaziGZRSxpZSpTV0Ew4="
    # COVERALLS_REPO_TOKEN
    - secure: "CHUT8Gmkp1Hoj7Og7w3bUaxGoFSkArO6IdwBJMiWEV9/V+2USgM3qp7DnVjgpTwiAIycO5utaMUd+WbKw/mknO0wFYt7h/zUigkTamJluKbeusPBX8xVaoU8ju6clqJ3EM5i0CtUWKSfLzJMVd4LtIkgeuYOPPihA3kbuQl03woIGMiJUSKS0SjgB7k9YAZ+dPHQNoFB5aeQ97Ik6QH/OzYur0nVMTpF1bSrdeSOaNBUa+2gCpdunImInXclMKnCU73eHlKJeAwKwufZ194dJhrqdcKWJQLtG3OPQFkCjv/wfSU9JzQ/aue/z3bpSx0diqUcWfPm6radlT+RWmPs3w1hUiQ6ok+bIKrnx1iu6NfN1LxP3xatacL5vQ/IZMdgZ0mQHcufq2KjertxvU70/+3x5zBV/c9g0dseyUOmYvPzbxe1m3/T9jJ4LbpXFo5cdoaD8IMx4O6LiYpunTJMvEDlsfU7m3d/KJgGVS9/VLo81h73MmM+CXMzOTUDp4M3M2S/e39DUirz4PkR9CDLFPtm5aV38tsXmDLb7iRpWUv/MosmCNRiZiBnfIgvQV37aX/rEHe08iuqfZ6nCm/NNxMxrWgV6BNaxpvqms/wG19Y6m0eBWj9GU2nGcabKihSDz6NZkNnCoatp41aCqwZJBVXI5ksKBLnRUOiTD6qLEc="
    # CODACY_PROJECT_TOKEN
    - secure: "dmTPaPlYEcbVUUeYL3r3XG7wU5wvoEQjONV9DAfPLz3pOJG2EMDTaAEYD39ho4NFCFr02Xm9wsnRUX9lD7sPJJQc0RQ14qRoT+KBFOj4jSdo6OyZ3BwdDh1Q4CP4whi30/D3WdhG0WSICvKZ+CWuBqeT6ZFrUhtt1u555an++TA3wpNyG0eLdCiWxnrN2tO1K3K/LPRbS581+yQCbypL6Ihzvma40fOkPJi5PIXRJO4ggEkA/Zr6oXEV9OrAljk1MpGE2XCRKoBAbJ/tHAAbkImj66D62WQwHREjv/XQ4Ocvz028eiWOteQqJt97FRmCkAYGdX+29Z/4HypYCYZn8ssLZxTrP+HucMDbkU9whDtFR0rveL6PbrfdKcl8TfjAxbF9n/EbBL8IC9W/Hajq/+IZwrbfQVdGhm8d4d5eWKx4XWSV++yg5DgRYcTwzNmFc/crZNoPaf7sB/KbKnp0U0FufSSEcJLAierbq/+2B5eNBadoCiqgao2NiDWxEftQGXqg5XGekZJZSUq3YMRuQf8yhPSBKS1TyWQ9dDsj+oManbKc6pwdk6kUp44a9L8lsDSFGiHhkLvE1A2FeuBdIQHY7xUVhsM+FzwwTaBItnGE6jdi3QMCLt26lwza3pvQeaQlFrO5FuncW0Mw/i7tYH/5lQPaXxMoopeLaGjJFk4="

matrix:
  include:<%
    from builtins import sorted
    cover_env = ",report,coveralls,codecov,ocular,codacy"
    def sort_key(pair):
        env, config = pair
        return (
            env.startswith("py"),
            not config.get("cover", True),
            env,
        )
%>
% for env, config in sorted(environments.items(), key=sort_key):
    - python: "${config["python"]}"
% if config["python"] == "3.7":
      dist: xenial
      sudo: required
% endif
      env:
        - TOXENV=${(env + (cover_env if config.get("cover", True) else ""))}
% endfor

before_install:
  - python --version
  - uname -a
  - lsb_release -a

install:
  - |
    set -ex
    if [[ $TRAVIS_PYTHON_VERSION == 'pypy' ]]; then
      (cd $HOME
       wget https://bitbucket.org/pypy/pypy/downloads/pypy2-v6.0.0-linux64.tar.bz2
       tar xf pypy2-*.tar.bz2
       pypy2-*/bin/pypy -m ensurepip
       pypy2-*/bin/pypy -m pip install -U virtualenv)
      export PATH=$(echo $HOME/pypy2-*/bin):$PATH
      export TOXPYTHON=$(echo $HOME/pypy2-*/bin/pypy)
    fi
    if [[ $TRAVIS_PYTHON_VERSION == 'pypy3' ]]; then
      (cd $HOME
       wget https://bitbucket.org/pypy/pypy/downloads/pypy3-v6.0.0-linux64.tar.bz2
       tar xf pypy3-*.tar.bz2
       pypy3-*/bin/pypy3 -m ensurepip
       pypy3-*/bin/pypy3 -m pip install -U virtualenv)
      export PATH=$(echo $HOME/pypy3-*/bin):$PATH
      export TOXPYTHON=$(echo $HOME/pypy3-*/bin/pypy3)
    fi
    set +x
  - pip install -U tox pbr
  - virtualenv --version
  - easy_install --version
  - pip --version
  - tox --version

before_script:
  - curl -L https://codeclimate.com/downloads/test-reporter/test-reporter-latest-linux-amd64 > ./cc-test-reporter
  - chmod +x ./cc-test-reporter
  - ./cc-test-reporter before-build

script:
  - tox -v

after_failure:
  - more .tox/log/* | cat
  - more .tox/*/log/* | cat

after_script:
  - ./cc-test-reporter after-build --exit-code $TRAVIS_TEST_RESULT || true

deploy:
  provider: pypi
  user: demosdemon
  distributions: sdist bdist_wheel
  skip_existing: true
  password:
    secure: "Y4Rc43O3VIxi0D8UQajQSzBMHT6b7ZNrivPWQNv9r3E3B9Br52IqIq1u8sZhstAWpTRTDJmxP93OtTOIUbPcBSb+lsoylF4QOt9DRrc+ieBFW1KiAHFzNxzPalp8fuZOq7la9tDeo2f4YtcxUiHWC3xzQAginMj1kVPRmnET5W/jH7+vaMpWdoq9VBStjgxOUQzzL0MSEWLJrt/THTwsqQbExOiTCWzeYgKVavzqgykbfo5uDivAGVlvA23na+MydnJ5QRfIpMqyERHsyOwJgJdwipwZ07z1DupWQBil7aklVH8mmcUvH1y1YOnBhaHCsrFbTdGrFBrTCG/tAwCTjy0ybWrBemgLMMxeTwBZjX+dJt10M1h/pTR+WRJEkw2me61HkPSwlU6s5zKpzqtVf5FycBrkjnmXhj30J9xWSabDWD9YqoiZI1l7yH35zz5siS1dlDXF3b5vCfo/AodaFITvn0+cujsrcPa5AzrI1OyX8aL81c74yiIH+VNww2Opit6EteUBojXtG0BNXy5PR8Q6Px+chfDc+dgXSINhoh7bsrufvd3LmdqP97iRbaO+EATHefKJa7GuEda35VWoP2bW0R2H8Zbynt7nyQzwekwu6u8PjW5I1wY0TRPWZblUWo1EZV8Lub/Rz7kWRfhaBKy/yov8olCOZYzQM2MJaYo="
  on:
    # tags: true
    condition: '$TOXENV = *"-nocov"'

notifications:
  email:
    on_success: never
    on_failure: change
