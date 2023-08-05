from setuptools import setup
 

def readme():
    with open('README.md', encoding='utf-8') as f:
        README = f.read()
    return README


setup(
    name="dailify",
    version="0.0.0.5.1",
    description="A Python package helping me whore myself out even further on social media.",
    long_description=readme(),
    long_description_content_type="text/plain",
    url="https://github.com/lucassel/dailify",
    author="Lucas Selfslagh",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["dailify"],
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "dailify=dailify.cli:main",
        ]
    },
)