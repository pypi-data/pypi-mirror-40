import setuptools

with open("README.md", "r") as fh:
	long_description = fh.read()

setuptools.setup(
	name="ikabot",
	version="0.8.2",
	author="santipcn",
	description="A bot for ikariam",
	long_description=long_description,
	long_description_content_type="text/markdown",
	url="https://github.com/santipcn/ikabot",
	packages=setuptools.find_packages(),
	install_requires=[
		  'requests',
		  'pycryptodome'
	],
	entry_points = {
		'console_scripts': ['ikabot=ikabot.command_line:main'],
	},
	classifiers=(
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"Operating System :: POSIX :: Linux",
	),
)
