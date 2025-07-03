# swarmd

**swarmd** is a CLI tool for progressive (canary) deployments in Docker Swarm using YAML stack files and Nginx as a reverse proxy.

## Main Features
- Progressive deployment of services in Docker Swarm
- Management of stacks and canary/stable services
- Dynamic adaptation of Nginx as a reverse proxy
- Commands: `deploy`, `promote`, `rollback`, `status`, `cleanup`

## Installation

```bash
pip install .
```

## Usage

```bash
swarmd --help
```

## License
MIT
