import setuptools

with open("README.md", "r") as fh:
	long_description = fh.read()

setuptools.setup(
	name="ratuil",
	version="0.3.0",
	author="troido",
	author_email="troido@protonmail.com",
	description="A terminal UI library for games",
	long_description=long_description,
	long_description_content_type="text/markdown",
	url="https://github.com/jmdejong/ratuil",
	packages=setuptools.find_packages(),
	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent"
	],
	python_requires='>=3.6'
)

