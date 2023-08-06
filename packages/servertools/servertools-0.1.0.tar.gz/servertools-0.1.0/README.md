# servertools

[![PyPI](https://img.shields.io/pypi/pyversions/servertools.svg)](http://pypi.python.org)
[![PyPI](https://img.shields.io/pypi/format/Django.svg)](http://pypi.python.org)
[![](https://img.shields.io/travis/michagrandel/servertools/develop.svg)](https://travis-ci.org/michagrandel/servertools)
[![](https://img.shields.io/codecov/c/github/michagrandel/servertools/develop.svg)]()
[![GitHub release](https://img.shields.io/github/release/michagrandel/servertools.svg)](https://github.com/michagrandel/servertools/releases)
[![PyPI](https://img.shields.io/pypi/v/servertools.svg)](http://pypi.python.org)
[![license](https://img.shields.io/github/license/michagrandel/servertools.svg)](https://github.com/michagrandel/servertools/blob/master/LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](http://makeapullrequest.com)

**servertools** provide some tools to identify servers and fix some specific problems.

> **Early Development**
>
> Please note that this project is in planning/early development phase!
> Many things might not work or not even exist the way you would expect.

## Getting Started

These instructions will get you a copy of the project up and running on your 
local machine for development and testing purposes. See deployment for notes on 
how to deploy the project on a live system.

### Prerequisites

This project is based [Python 3.5.x][python]. Other than that there are no special requirements.


#### Install on your local machine


To prepare for installation, make sure, you have at least [Python 3.5+][python] and 
[pip][pip] up and running!

### Installing

#### Install on any server or local machine

*Bare in mind that servertools are - as the name indicate - written to be used on a *server*.
That's why any feature may or may not work on your local machine.*

That said, most features will nonetheless work on any computer. 

#### Install on a uberspace Server

Download the servertools and extract:

```bash
[jasmin@fornax ~]$ url="`curl -s https://api.github.com/repos/michagrandel/servertools/releases/latest | grep tarball_url | cut -d '"' -f 4`"
[jasmin@fornax ~]$ wget $url -O servertools.tar
[jasmin@fornax ~]$ tar -xvf servertools.tar > name.txt
[jasmin@fornax ~]$ mv $(head -n 1 "name.txt") servertools
[jasmin@fornax ~]$ rm servertools.tar name.txt
```

Install the python module:

```
[jasmin@fornax ~]$ cd ~/servertools 
[jasmin@fornax servertools]$ python3 setup.py install
```

You are ready!


## Running the tests

Keep going, unit test are not written yet. Maybe you want to give it a try?

## Built With

* Python 3.5

## Contributing

Thank you very kindly for your interest in contributing to our code!

Please take a moment and read [our Contributing Guide](Contributing.md) to get you started!

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, 
see the [releases on this repository][github-releases]. 

## Authors

* **Micha Grandel** - *Author and maintainer* - [Github][github]

We thank all of our [contributors][github-contributors], who participated in this project.

## License

This project is licensed under the Apache 2.0 License - see the [LICENSE](LICENSE) 
file for details

[github]: https://github.com/michagrandel
[github-releases]: https://github.com/michagrandel/servertools/releases
[github-contributors]: https://github.com/michagrandel/servertools/graphs/contributors
[python]: https://www.python.org/downloads/
[pip]: https://pypi.python.org/pypi/pip
[flask]: http://flask.pocoo.org
[gitflow]: https://danielkummer.github.io/git-flow-cheatsheet/
[gitflow-model]: http://nvie.com/posts/a-successful-git-branching-model/
