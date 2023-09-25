from setuptools import find_packages, setup

setup(
	name = "diff4tbl",
	version = "0.1.0",
	description = "diff4tbl is a command-line table comparison tool developed in Python, leveraging the Pandas library. Inspired by GNU diff, it also offers functionalities such as data filtering, selective omission of common elements, and discrepancy metrics.",
	author = "5uperb0y",
	url = "https://github.com/5uperb0y/diff4tbl",
	packages = find_packages(),
	include_package_data = True,
	entry_points = {
		"console_scripts": [
			"diff4tbl=diff4tbl.__main__:main"
		]
	},
	install_requires = [
		"pandas"
	]
)