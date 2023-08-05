import setuptools

with open("../README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='django-commander',
    version='0.1.0',
    description='Run Django manage.py command from the web',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Matt Cooper',
    author_email='vtbassmatt@gmail.com',
    url='https://github.com/vtbassmatt/django-commander',
    packages=setuptools.find_packages(),
    package_data={
        'commander': ['templates/*.html', 'management/commands/*.py'],
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ]
)