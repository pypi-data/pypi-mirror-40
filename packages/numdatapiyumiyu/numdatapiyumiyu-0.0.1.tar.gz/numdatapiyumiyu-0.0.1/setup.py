import setuptools

with open("README.md","r") as fh:
	long_description = fh.read()

setuptools.setup(
	name="numdatapiyumiyu",
	version="0.0.1",
	author="piyush patel",
	author_email="piyush.patel@colorado.edu",
	description="simple package calculating for numbers",
	long_description=long_description,
	long_description_content_type="text/markdown",
	keywords="ckage numbers calculations",
	url="",
	packages=setuptools.find_packages(),
	classifiers=[
		"Programming Language :: Python :: 2",
		"Operating System :: OS Independent"
	],
	)