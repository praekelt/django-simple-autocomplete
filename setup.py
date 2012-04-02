from setuptools import setup, find_packages

setup(
    name='django-simple-autocomplete',
    description='App enabling the use of jQuery UI autocomplete widget for ModelChoiceFields with minimal configuration required.',
    long_description = open('README.rst', 'r').read() + open('AUTHORS.rst', 'r').read() + open('CHANGELOG.rst', 'r').read(),
    version='0.2',
    author='Praekelt Foundation',
    author_email='dev@praekelt.com',
    license='BSD',
    url='http://github.com/praekelt/django-simple-autocomplete',
    packages = find_packages(),
    dependency_links = [
    ],
    install_requires = [
        'django',
    ],
    tests_require=[
        'django-setuptest>=0.0.6',
    ],
    test_suite="setuptest.SetupTestSuite",
    classifiers=[
        "Programming Language :: Python",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
    ],
    zip_safe=False,
)
