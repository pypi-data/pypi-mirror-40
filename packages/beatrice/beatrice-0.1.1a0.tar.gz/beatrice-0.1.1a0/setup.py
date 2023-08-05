import re
import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()
   
with open('beatrice/__init__.py') as f:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', f.read(), re.MULTILINE).group(1)

setuptools.setup(
    name='beatrice',
    version=version,
    author='Andre Augusto',
    description='A discord.py extension for storing files on discord servers ',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/Naranbataar/Beatrice',
    packages=['beatrice'],
    include_package_data=True,
    python_requires='>=3.6.0',
    install_requires=['discord.py>=1.0.0a'],
    classifiers=[
        'Framework :: AsyncIO',
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
    ],
)
