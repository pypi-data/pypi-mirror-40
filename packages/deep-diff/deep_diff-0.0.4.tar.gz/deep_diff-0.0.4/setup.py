
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='deep_diff',
    version='0.0.4',
    url='https://github.com/ider-zh/diff',
    license='BSD 3-Clause license',
    author='ider',
    author_email='326737833@qq.com',
    description='a tool to diff dict list set data',
    long_description = long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        'Topic :: Software Development :: Libraries',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only'],
)