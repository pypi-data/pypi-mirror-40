import setuptools
from pathlib import Path

readme_path = Path('./README')

setuptools.setup(
    name='pandas_util',
    version='0.0.1',
    author='Filantus',
    author_email='filantus@mail.ru',
    url='https://pypi.org/project/pandas-util/',
    description='Some utils for working with pandas.',
    long_description=readme_path.read_text(),
    long_description_content_type="text/markdown",
    py_modules=['pandas_util'],
    install_requires=['pandas', 'openpyxl', 'excel-util'],
    packages=setuptools.find_packages(),
    license='GPL',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Programming Language :: Python :: 3.7',
        'Operating System :: OS Independent',
    ],
)
