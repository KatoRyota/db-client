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
    author="",
    author_email="",
    packages=find_packages(),
    data_files=[
        ("config", ["config/*"]),
    ],
    include_package_data=True,
    zip_safe=False,
    install_requires=install_requirements,
    tests_require=[],
    entry_points={
        "console_scripts": [
            "dbclient=dbclient.__main__",
        ]
    },
)
