from setuptools import setup, find_packages

setup(
    name="swarmd",
    version="0.1.0",
    description="CLI para despliegues progresivos (canary rollouts) en Docker Swarm usando Nginx",
    author="swarmd contributors",
    license="MIT",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "typer",
        "docker",
        "jinja2",
        "pyyaml"
    ],
    entry_points={
        "console_scripts": [
            "swarmd=swarmd.main:app"
        ]
    },
    python_requires=">=3.7",
) 