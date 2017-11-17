from setuptools import setup, find_packages

setup(
	name='colorstrip',
	version='1.0.0rc1',

	url='https://github.com/0xLeon/py-colorstrip',
	author='Stefan Hahn',
	author_email='development@0xleon.com',

	license='MIT',

	py_modules=[
		'colorstrip',
	],

	entry_points={
		'console_scripts': [
			'colorstrip = colorstrip:main'
		],
	},

	install_requires=[
		'numpy>=1.13',
		'opencv-contrib-python>=3.3'
	],

	classifiers=[
		'Environment :: Console',
		'Development Status :: 5 - Production/Stable',
		'Intended Audience :: Developers',
		'Intended Audience :: Education',
		'Intended Audience :: End Users/Desktop',
		'Intended Audience :: Science/Research',
		'License :: OSI Approved :: MIT License',
		'Operating System :: MacOS',
		'Operating System :: Microsoft :: Windows',
		'Operating System :: POSIX',
		'Operating System :: Unix',
		'Programming Language :: Python',
		'Programming Language :: Python :: 2',
		'Programming Language :: Python :: 2.7',
		'Programming Language :: Python :: 3',
		'Programming Language :: Python :: 3.6',
		'Topic :: Multimedia',
		'Topic :: Multimedia :: Graphics',
		'Topic :: Multimedia :: Video',
		'Topic :: Scientific/Engineering',
		'Topic :: Scientific/Engineering :: Information Analysis',
		'Topic :: Scientific/Engineering :: Visualization',
	],

	keywords='video color image visualization'
)
