import setuptools

with open("README.md","r") as fh:
	long_description=fh.read()

setuptools.setup(
	name="lgblkb_tools",
	version="0.0.8",
	author="Dias Bakhtiyarov",
	author_email="dbakhtiyarov@nu.edu.kz",
	description="Some useful tools for everyday routine coding improvisation)",
	long_description=long_description,
	long_description_content_type="text/markdown",
	url="https://bitbucket.org/lgblkb/lgblkb_tools",
	packages=setuptools.find_packages(),
	classifiers=(
		"Programming Language :: Python :: 3.6",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
	),
)
