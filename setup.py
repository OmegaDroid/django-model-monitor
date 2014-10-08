from distutils.core import setup

setup(
    name='django-model-monitor',
    version='0.0.1',
    packages=['modelmonitor'],
    package_dir={'': 'src'},
    url='https://github.com/OmegaDroid/django-model-monitor',
    license='MIT',
    author='Daniel Bate',
    author_email='',
    description='App to monitor changes in models',
    requires=["django"],
)
