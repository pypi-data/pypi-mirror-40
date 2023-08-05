from setuptools import setup
 


def readme():
    with open('README.md', encoding='utf-8') as f:
        README = f.read()
    return README


setup(
    name="ghent-theft-module",
    version="0.0.2.2",
    description="A Python package demonstration.",
    long_description=readme(),
    long_description_content_type="text/plain",
    url="https://github.com/lucassel/ghent-theft-module",
    author="Lucas Selfslagh",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["ghent_theft_module"],
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "ghent-theft-module=ghent_theft_module.cli:main",
        ]
    },
)