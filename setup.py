from setuptools import find_packages, setup

setup(
    name='service-locator',
    version='1.0',
    packages=find_packages(),
    include_package_data=True,
    url='https://github.com/alexescalonafernandez/service-locator',
    license='MIT',
    author='Alexander Escalona Fernández',
    author_email='alexescalonafernandez@gmail.com',
    setup_requires=['setuptools-markdown'],
    description='Python implementation of service locator pattern based on java CDI and ServiceLoader api.',
    long_description_markdown_filename='README.md',
    classifiers=[
            'Intended Audience :: Developers',
            'License :: OSI Approved :: MIT License',
            'Operating System :: OS Independent',
            'Programming Language :: Python',
            'Programming Language :: Python :: 3.5',
            'Programming Language :: Python :: 3.6',
            'Topic :: Utilities',
        ],
)
