from setuptools import find_packages, setup

setup(
    name='hthworldwide',
    version='0.0.2',
    description='HTH World Wide Medical Facilities Database controller.',
    url='https://gitlab.com/wefindx/hthworldwide',
    author='Mindey',
    author_email='mindey@qq.com',
    license='ASK FOR PERMISSIONS',
    packages = find_packages(exclude=['docs', 'tests*']),
    install_requires=['metadrive'],
    extras_require = {
        'test': ['coverage', 'pytest', 'pytest-cov'],
    },
    zip_safe=False
)
