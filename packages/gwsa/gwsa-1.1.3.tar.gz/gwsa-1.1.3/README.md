## gwsa - git work space automation

Runs common git commands on every git repo in a workspace

## Usage
### status
This command shows

 * status of repo: dirty or clean, 
 * if rebase, merge or cherry-pick is in progress
 * commit difference with remote: ahead + behind commits
 * status of remote: gone or ok
 * if forced push happend

![status](https://gitlab.com/aanatoly/gwsa/raw/master/doc/01-status.png)

### fetch
![fetch](https://gitlab.com/aanatoly/gwsa/raw/master/doc/02-fetch.png)

### rebase
Rebase local tracking branches. In case of a conflict, it aborts rebase.

![rebase](https://gitlab.com/aanatoly/gwsa/raw/master/doc/03-rebase.png)

## Installation
```bash
pip install gwsa
```

## Development
```bash
[[ -d venv ]] || virtualenv venv; . venv/bin/activate
make clean
make build
make test
make install
deactivate
```

## Credits
This project was inspired by [gws](https://github.com/StreakyCobra/gws) by Fabien Dubosson. <br>The reason for writing my own is a language. I prefer python over bash: better syntax, a lot of libraries, and easy install with `pip`
