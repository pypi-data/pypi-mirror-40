from setuptools import setup


def readme():
    with open('README.md') as f:
        README = f.read()
    return README


setup(
    name="search-trains",
    version="1.0.2",
    description="A Python package to search trains between stations in India.",
    long_description=readme(),
    long_description_content_type="text/markdown",
    author="Naveen Tummidi",
    author_email="naveentummidi0807@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
    ],
    packages=["trains"],
    include_package_data=True,
    install_requires=["requests", "tabulate", "bs4"],
    entry_points={
        "console_scripts": [
            "search-trains=trains.train:main",
        ]
    },
)
