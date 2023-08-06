from setuptools import find_packages, setup

setup(
    name='django-zipkin-trace-nonspecialist',
    version='1.1.0',
    url='https://github.com/nonspecialist/django-zipkin-trace',
    author='Colin Panisset',
    author_email='github@clabber.com',
    description='Automatically trace your Django application to Zipkin',
    license='MIT',
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    install_requires=[
        'Django',
        'py_zipkin==0.13.0',
        'requests-futures==0.9.7',
        'requests[security]',
        'pyOpenSSL'
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: System :: Networking :: Monitoring',
    ],
)
