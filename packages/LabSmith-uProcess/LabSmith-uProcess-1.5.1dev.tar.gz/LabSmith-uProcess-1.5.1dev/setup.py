
from distutils.core import setup, Extension
from distutils import sysconfig

setup(
    name = 'LabSmith-uProcess',
    version='1.5.1dev',
    #include_package_data=True,
    packages=['Python'],
    url='http://www.labsmith.com',
    long_description=open('README.txt').read(),
    author='LabSmith',
    author_email='ecummings@labsmith.com',
)