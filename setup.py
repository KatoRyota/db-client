from setuptools import setup, find_packages

with open('requirements.txt') as requirements_file:
    install_requirements = requirements_file.read().splitlines()

setup(
    name="db-client",
    version="0.0.1",
    description="db-client",
    url="https://github.com/KatoRyota/db-client",
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
    # package_data={
    #     "dbclient.config": ["application.conf", "logging.conf"],
    # },
    # data_files=[
    #     ("", ["requirements.txt", "README.md"]),
    # ],
    zip_safe=True,
    install_requires=install_requirements,
    entry_points={
        "console_scripts": [
            "dbclient=dbclient.dbclient:main",
        ]
    },
)
