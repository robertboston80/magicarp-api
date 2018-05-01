from setuptools import setup, find_packages


def readme():
    with open('README.md') as fpl:
        return fpl.read()


setup(
    name='magicarp-api',
    version='1.0.4',
    description=(
        'Magicarp-Api if flask based, micro-framework that allows to '
        'build functional api from get-go'
    ),
    long_description=readme(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.5',
        'Topic :: Software Development :: Version Control :: Git',
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
    packages=find_packages(),
    zip_safe=False
)
