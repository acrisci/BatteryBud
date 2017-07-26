from setuptools import setup, find_packages

setup(
    name='batterybud',
    version='0.0.1',
    author='Tony Crisci',
    author_email='tony@dubstepdish.com',
    url='https://github.com/acrisci/batterybud'
    license='BSD',
    description='Battery tray status indicator',
    long_description=open('README.rst').read(),

    #install_requires=['PyYAML', 'netifaces', 'i3ipc', 'ijson', 'requests'],

    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3',
    ],

    package_data={'batterybud': ['icons/*']},

    scripts=['batterybud'],

    packages=find_packages(),
)
