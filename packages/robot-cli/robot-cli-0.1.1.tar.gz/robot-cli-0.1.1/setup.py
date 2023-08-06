import os
from setuptools import setup, find_packages

PATH = os.path.dirname(os.path.abspath(__file__))

install_requires = []


def read(fname):
    return open(os.path.join(PATH, fname)).read()


version = __import__('robot_cli').get_version()

setup(
    name='robot-cli',
    version=version,
    description='',
    long_description=read('README.md'),
    url='https://github.com/hypc/robot-cli',
    author='hypc',
    author_email='h_yp00@163.com',
    license='MIT',
    keywords='robotframework robot-cli',
    packages=find_packages(exclude=['docs', 'tests*', 'example']),
    install_requires=install_requires,
    python_requires='>=3',
    classifiers=[
        'Development Status :: 5 - Production/Stable',

        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',

        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    entry_points={
        'console_scripts': [
            'robot-cli=robot_cli.core:execute_from_command_line',
        ],
    },
)
