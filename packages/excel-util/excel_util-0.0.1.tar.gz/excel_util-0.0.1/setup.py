import setuptools
from pathlib import Path

readme_path = Path('./README')

setuptools.setup(
    name='excel_util',
    version='0.0.1',
    author='Filantus',
    author_email='filantus@mail.ru',
    url='https://pypi.org/project/plpy-ext/',
    description='Some utils for working with excel.',
    long_description=readme_path.read_text(),
    long_description_content_type="text/markdown",
    py_modules=['excel_util'],
    install_requires=['openpyxl'],
    packages=setuptools.find_packages(),
    license='GPL',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Programming Language :: Python :: 3.7',
        'Operating System :: OS Independent',
    ],
)
