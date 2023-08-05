import setuptools
import beewars

with open("README.md") as f:
    long_desc = f.read()


setuptools.setup(
        name="beewars",
        version=beewars.version,
        description="BeeWars (Game)",
        long_description=long_desc,
        long_description_content_type="text/markdown",
        url="https://github.com/poyynt/beewars/",
        author="Parsa Torbati",
        author_email="parsa@programmer.net",
        packages=setuptools.find_packages(),
        python_requires=">=3.2",
        install_requires=[
            "pygame",
            "numpy",
            ],
        entry_points={
            "console_scripts": [
                "beewars=beewars.main",
                ],
            },
        classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: GNU General Public License (GPL)",
            "Operating System :: OS Independent",
            "Development Status :: 5 - Production/Stable",
            "Natural Language :: English",
            "Topic :: Games/Entertainment",
            ],
        )
