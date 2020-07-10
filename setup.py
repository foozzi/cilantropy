from setuptools import setup
import cilantropy
import sys

# Cilantropy requirements
install_requirements = [
        'Flask>=1.1.2',
        'setuptools>=0.6c11',
        'jinja2>=2.11.2',
        'docopt>=0.6.2',
        'colorama>=0.4.3',
        'docutils>=0.16'
]

def long_description():
    f = open("setup.rst", mode="r", encoding="utf-8")
    return f.read()

setup(
    name='Cilantropy',
    version=cilantropy.__version__,
    url='https://github.com/foozzi/cilantropy/',
    license='BSD License',
    author=cilantropy.__author__,
    author_email='foozzione@gmail.com',
    description='A Python Package Manager interface.',
    long_description=long_description(),
    packages=['cilantropy'],
    keywords='package manager, distribution tool, cilantropy',
    platforms='Any',
    zip_safe=False,
    include_package_data=True,
    package_data={
      'cilantropy': ['static/*.*', 'templates/*.*'],
    },
    install_requires=install_requirements,
    tests_require=['nose'],
    test_suite='nose.collector',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Web Environment',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    entry_points={
        'console_scripts': [
            'cilantropy = cilantropy.main:run_main',
            'plp = cilantropy.console:run_main'
        ],
    },
)
