from setuptools import setup, find_packages


with open('README.rst') as f:
    long_description = ''.join(f.readlines())


setup(
    name='radicale-sirius-plugin',
    version='0.3.0',
    description='Access CVUT Fit Sirius Service using caldav',
    long_description=long_description,
    author='Pavel Bezstarosti',
    author_email='bezstpav@fit.cvut.cz',
    keywords='radicale, caldav, Sirus',
    license='MIT',
    url='https://github.com/bezstpav/radicale-sirius-plugin',
    packages=find_packages(),
    package_data={
    },
    entry_points={
    },
    install_requires=[
        'requests',
        'radicale'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Intended Audience :: Customer Service',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.7',
        'Topic :: Utilities',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    zip_safe=False,
)
