import setuptools

with open("README.md","r") as fh:
	long_description = fh.read()

setuptools.setup(
	name = "ArgotToo",
	version = "1.0",
	scripts = ["argotToo.py"],
	author = "Maarten JMF Reijnders",
	description = "Gene ontology prediction based on Argot2",
	long_description = long_description,
	long_description_content_type = "text/markdown",
	url = "https://gitlab.com/mreijnders/ArgotToo/",
	packages = setuptools.find_packages(),
	classifiers = [
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
	],
)
