[![Build Status](https://travis-ci.org/wmacevoy/brainwallet.svg?branch=master)](https://travis-ci.org/wmacevoy/brainwallet)

# Brain Wallet Tools

Python tools for making brainwallet keys using the Shamir Secret Sharing algorithm.

# OS X | Linux | WSL

```bash
./your/path/to/bw <options>
```

# Docker

For those wishing to use Docker to run the Brainwallet software, follow these steps:

## Build:
Navigate to the brainwallet directory containing Dockerfile and in the command-line interface:
**Run Once**
```
docker build -t brainwallet
```

## Run:

```
docker run --rm -t brainwallet:latest bw <options>
```

# Table of Contents
+ [Documentation Home](docs/README.md "Home Page")
+ [Usage](docs/usage.md "Usage")
+ [Creating Keys](docs/createOverview.md "Overview")
  + [Overview](docs/createOverview.md "Overview")
  + [Languages](docs/languages.md "Languages")
  + [Options](docs/options.md "Options")
+ [Recovering Keys](docs/recoverOverview.md)
+ [Testing](docs/testing.md "Testing")
+ [Troubleshooting](docs/troubleshooting.md)
