from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="kuriyama",
    version='0.1.10',
    description='A framework for OICQ(QQ, made by Tencent) headless client "Mirai".',
    author='Chenwe-i-lin',
    author_email="Chenwe_i_lin@outlook.com",
    url="https://github.com/Chenwe-i-lin/python-mirai",
    packages=find_packages(include=("mirai", "mirai.*")),
    python_requires='>=3.7',
    keywords=["oicq qq qqbot", ],
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers = [
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: User Interfaces',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7',
        "Operating System :: OS Independent"
    ]
)
