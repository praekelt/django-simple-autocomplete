from setuptools import setup, find_packages


setup(
    name='django-simple-autocomplete',
    description='App enabling the use of jQuery UI autocomplete widget for ModelChoiceFields with minimal configuration required.',
    long_description = open('README.rst', 'r').read() + open('AUTHORS.rst', 'r').read() + open('CHANGELOG.rst', 'r').read(),
    version='1.11',
    author='Praekelt Consulting',
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
        'tox',
    ],
    classifiers=[
        "Programming Language :: Python",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
    ],
    zip_safe=False,
    include_package_data=True
)
