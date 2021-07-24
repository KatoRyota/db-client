from setuptools import setup, find_packages

with open('requirements.txt') as requirements_file:
    install_requirements = requirements_file.read().splitlines()

setup(
    name="db-client",
    version="0.0.1",
    description="db-client",
    url="",
    license="",
    long_description="",
    keywords="",
    classifiers=[
        'Programming Language :: Python :: 2.7',
    ],
    author="Kato Ryota",
    author_email="example@com",
    packages=find_packages(),
    include_package_data=True,
    data_files=[
        ("config", ["config/application.conf", "config/logging.conf"]),
    ],
    zip_safe=False,
    install_requires=install_requirements,
    tests_require=[],
    entry_points={
        "console_scripts": [
            "dbclient=dbclient",
        ]
    },
)
