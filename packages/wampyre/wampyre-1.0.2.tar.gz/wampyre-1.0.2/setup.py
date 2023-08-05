from setuptools import setup, find_packages


setup(
    name='wampyre',
    version='1.0.2',
    description='Python implementation of a WAMP router.',
    author='Anders Jensen',
    author_email='johndoee@tidalstream.org',
    url='https://github.com/JohnDoee/wampyre',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    extras_require={
        'django': [
            'channels',
            'autobahn',
        ],
        'tests': [
            'pytest',
        ],
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)
