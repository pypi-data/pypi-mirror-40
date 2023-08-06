import setuptools

with open("README.md","r") as fh:
	long_description = fh.read()

setuptools.setup(
	name = "CrowdGO",
	version = "1.0",
	scripts = ["CrowdGO.py"],
	author = "Maarten JMF Reijnders",
	description = "Gene ontology prediction merging and improvement, using semantic ontology and a random forest algorithm",
	long_description = long_description,
	long_description_content_type = "text/markdown",
	url = "https://gitlab.com/mreijnders/CrowdGO/",
	packages = setuptools.find_packages(),
	classifiers = [
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
	],
)
