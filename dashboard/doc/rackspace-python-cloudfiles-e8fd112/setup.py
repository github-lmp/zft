
from setuptools import setup, find_packages
from cloudfiles.consts import __version__

setup(name='cloudfiles',
    version=__version__,
    description='CloudFiles client library for Python',
    classifiers=[], 
    keywords='',
    author='Rackspace',
    author_email='',
    url='https://www.rackspacecloud.com/',
    license='MIT',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    include_package_data=True,
    zip_safe=False,
    install_requires=[],
    setup_requires=[],
    test_suite='nose.collector',
    entry_points="""
    """,
    namespace_packages=[],
    )
