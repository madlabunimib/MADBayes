import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='MADBayes',
    version='0.5.0',
    author='Alessio Zanga, Emanuele Cavenaghi, Fabio Stella, Marco Scutari',
    author_email='alessio.zanga@outlook.it, cavenaghi.emanuele@gmail.com',
    license='GNU GENERAL PUBLIC LICENSE - Version 3, 29 June 2007',
    description='MADBayes is a Python library about Bayesian Networks.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    platforms=[
        'Environment :: Console',
        'Operating System :: POSIX :: Linux',
        'Operating System :: Microsoft :: Windows :: Windows 10',
        'Operating System :: MacOS',
    ],
    url='https://github.com/madlabunimib/MADBayes',
    packages=setuptools.find_packages(),
    install_requires=[
        'pydot',
        'matplotlib',
        'networkx>=2.4',
        'numba>=0.48',
        'numpy',
        'scipy',
        'pandas',
        'xarray',
        'rpy2',
        'lark-parser',
    ],
)
