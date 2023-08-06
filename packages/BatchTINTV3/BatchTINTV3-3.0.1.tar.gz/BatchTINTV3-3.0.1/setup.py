import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

pkgs = setuptools.find_packages()
print('found these packages:', pkgs)

pkg_name = "BatchTINTV3"

setuptools.setup(
    name=pkg_name,
    version="3.0.1",
    author="Geoffrey Barrett",
    author_email="",
    description="BatchTINTV3 - GUI created to more efficiently sort Axona/Tint data.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/HussainiLab/BatchTINTV3.git",
    packages=pkgs,
    install_requires=
    [
        'pyqt',
    ],
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Affero General Public License v3  ",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.7 "
    ),
)
