from setuptools import setup, find_packages

setup(

    name='houtools',
    version='0.1.0',
    description='General tools for Houdini.',
    url='http://github.com/sitg/houtools',
    
    packages=find_packages(exclude=['build*', 'tests*']),
    
    author='Mike Boers',
    author_email='houtools@mikeboers.com',
    license='BSD-3',
    
    install_requires=[
        'metatools',
        'pyyaml',
    ],

    entry_points={
        'appinit.houdini.gui': '''
            houtools_shelf = houtools.shelf:load
        ''',
    }
    
)