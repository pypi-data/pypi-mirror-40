from setuptools import setup, find_packages

setup(
    name='django-test-utils3',
    version='1.1.10',
    packages=find_packages(),
    author='Johan Michaelson Phroiland',
    author_email='jon@crowdkeep.com',
    description='A package to help testing in Django',
    long_description='Testing and Crawling a Django Project.\n'
                     ' Compatible with Django 1.11 and Python 3.6.\n'
                     ' Version references <version>.<month>.<change>.\n'
                     ' Version updated annually.\n',
    long_description_content_type='text/markdown',
    url='https://github.com/phroiland/django-test-utils',
    download_url='https://github.com/phroiland/django-test-utils',
    test_suite='test_project.run_tests.run_tests',
    include_package_data=True,
    install_requires=['BeautifulSoup4', 'twill3', 'django', 'six', ]
)
