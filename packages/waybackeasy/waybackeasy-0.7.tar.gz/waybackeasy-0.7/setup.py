import setuptools

# reading in long description from README file
with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
	name = "waybackeasy",
	version = "0.7",
	author = "Johannes Seikowsky",
	author_email = "jseikowsky@gmail.com",
	description = "Easiest way to access a Waybackmachine snapshot of a sepecific website on a specific date.",
	long_description = long_description,
	long_description_content_type = "text/markdown",
	url = "https://github.com/JohannesSeikowsky/waybackeasy",
	packages = setuptools.find_packages(),
	install_requires = [
		"requests>=1.5.0"
	],
	classifiers = [
		"Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
	],
)