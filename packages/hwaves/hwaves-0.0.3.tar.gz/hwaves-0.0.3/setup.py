from setuptools import setup, find_packages

longdesc = 'Current capabilities: '\
    'Radial wavefunction densities; '\
    'Spherical harmonics; '\
    'Real-space densities of hydrogenic eigenfunctions; '\
    'Real-space density of real-valued wavefunctions; '\
    'Real-space density isosurfaces and polygon data'

setup(
    name='hwaves',
    version='0.0.3',
    url='https://github.com/lensonp/hwaves.git',
    description='Compute and plot hydrogenic wavefunctions',
    long_description=longdesc,
    author='Lenson A. Pellouchoud',
    license='BSD',
    author_email='',
    install_requires=['numpy','scipy','masstable','periodictable'],
    packages=find_packages(),
    package_data={}
    )


