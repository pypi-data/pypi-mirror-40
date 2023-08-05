import setuptools
with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='xmldiffs',
    version='0.0.4',
    entry_points = {
        'console_scripts': ['xmldiffs=xmldiffs.command_line:run_main'],
    },
    author="ZIJIAN JIANG",
    author_email="jiangzijian77@gmail.com",
    description="Compare two XML files",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/CallmeNezha/xmldiffs",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
    ],
    install_requires = [
    ]
)
