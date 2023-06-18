from setuptools import setup

setup(
    name='clean_folder',
    version='0.0.5',
    description='Sorting files by category',
    url='https://github.com/VadimMarenko/hw_07.git',
    author='Vadim Marenko',
    author_email='vadim.marenko@gmail.com',
    license='MIT',
    packages=['clean_folder'],
    entry_points={'console_scripts': ['clean-folder = clean_folder.clean:main']}
)