
from distutils.core import setup, Extension
from distutils import sysconfig

setup(
    name = 'LabSmith_uProcess',
    version='0.1dev',
    include_package_data=True,
    packages=['Python'],
    long_description=open('README.txt').read(),
    author='LabSmith',
    author_email='ecummings@labsmith.com',
)