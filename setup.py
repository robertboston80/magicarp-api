from setuptools import setup


def readme():
    with open('README.md') as fpl:
        return fpl.read()


setup(
    name='magicarp-api',
    version='1.0',
    description=(
        'Flask based api - not complete api but solid building blocks '
        'to create one of your own'
    ),
    long_description=readme(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Software Development :: Version Control :: Git',
        'Topic :: Utilities',
    ],
    test_suite='nose.collector',
    tests_require=['nose'],
    url='https://github.com/Drachenfels/magicarp-api',
    author="Drachenfels",
    author_email="drachu@gmail.com",
    license="MIT",
    install_requires=[
        'Flask==0.12.2',
        'simple-settings==0.12.1',
        'python-dateutil==2.6.1',
        'pytz==2018.3',
        'url2vapi==1.2',
        'validators==0.12.1',
    ],
    include_package_data=False,
    packages=['magicarp'],
    zip_safe=False
)
