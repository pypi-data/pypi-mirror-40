import os
import sys

from setuptools import find_packages, setup

PROJECT_NAME = 'zmail'
MODULE_NAME = 'zmail'

# 'setup.py publish' shortcut.
if sys.argv[-1] == 'publish':
    os.system('pip3 install twine')
    os.system('pip3 install wheel')
    os.system('python3 setup.py sdist bdist_wheel')
    os.system('twine upload dist/*')
    os.system('rm -rf build dist .egg zmail.egg-info')
    sys.exit()

# 'setup.py test' shortcut.
if sys.argv[-1] == 'test':
    os.system('pip3 install pytest')
    os.system('pytest tests/')
    sys.exit()

# 'setup.py isort' shortcut.
if sys.argv[-1] == 'isort':
    os.system('isort -rc *.py')
    os.system('isort -rc zmail/*.py')
    os.system('isort -rc tests/*.py')
    sys.exit()

# 'setup.py flake8' shortcut.
if sys.argv[-1] in ('flake8', 'flake'):
    os.system('flake8 --ignore=E501 zmail/*.py tests/*.py')
    sys.exit()

setup(
    name='zmail',
    version='0.2.2',

    author='ZYunH',
    author_email='zyunhjob@163.com',

    description='Zmail allows you to send and get emails as possible as it can be in python',
    long_description='Zmail allows you to send and get emails as possible as it can be in python.'
                     'There is no need to check server address or make your own MIME string.With zmail, '
                     'you only need to care about your mail content.',
    keywords='email python3 package',

    url='https://github.com/ZYunH/zmail',
    license="MIT Licence",

    platforms='all',
    classifiers=(
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ),

    packages=find_packages(),
    include_package_data=True,

)
