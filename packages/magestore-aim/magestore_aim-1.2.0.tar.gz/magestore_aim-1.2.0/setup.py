import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

package_name = 'magestore_aim'
packages = setuptools.find_packages(include=[package_name, "{}.*".format(package_name)])

setuptools.setup(
    name=package_name,
    version="1.2.0",
    author="Mars",
    author_email="mars@trueplus.vn",
    description="New connection type to HOST machine, using private key.\n"
                "Get magento source from github repo.",
    long_description=long_description,
    long_description_content_type="",
    url="https://github.com/Magestore/go-environment",
    packages=packages,
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    python_requires='>=3',
)
