import setuptools



setuptools.setup(name = 'daymark',
	packages = setuptools.find_packages(),
	version = '1.0.6',
	license =['__license__'],
	description = 'daymark is a helper package.',
	author = 'Samarthya Choudhary',
	author_email = 'samarthyachoudhary7@gmail.com',
	url = 'https://gitlab.com/aman.indshine/lighthouse-function-helper.git',
	install_requires =['requests', 'redis', 'boto'],
	classifiers=['Programming Language :: Python :: 3', 'Development Status :: 3 - Alpha', 'Intended Audience :: Developers', 'Topic :: Software Development :: Build Tools', 'License :: OSI Approved :: MIT License'])