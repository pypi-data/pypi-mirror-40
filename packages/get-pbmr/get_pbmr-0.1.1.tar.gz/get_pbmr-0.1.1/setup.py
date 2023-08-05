from setuptools import setup

setup(name='get_pbmr',
    version='0.1.1',
    description='Getting per base mutation rate from sam file',
    author='Semar Petrus',
    packages=['get_pbmr'],
    entry_points = {
        'console_scripts': [
            'get_pbmr=get_pbmr.get_pbmr:get_mutation_rate_graph']},
    install_requires=['matplotlib', 'pandas'])
