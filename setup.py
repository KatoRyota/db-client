from setuptools import setup, find_packages

with open('requirements.txt') as requirements_file:
    install_requirements = requirements_file.read().splitlines()

setup(
    name="db-client",
    version="0.0.1",
    description="db-client",
    author="Kato Ryota",
    packages=find_packages(),
    install_requires=install_requirements,
    entry_points={
        "console_scripts": [
            "db-client=db-client.__main__",
        ]
    },
    classifiers=[
        'Programming Language :: Python :: 2.7',
    ]
)
