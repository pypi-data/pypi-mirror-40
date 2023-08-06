from setuptools import setup, find_packages

setup(
    name="aognet",
    version="0.0.1",
    author="Xilai Li, Tianfu Wu",
    author_email="lixilai0819@gmail.com",
    description="AOGNet",
    url="https://github.com/xilaili/AOGNet",
    packages=find_packages(),
    long_description="aognet",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    #install_requires=["PyYAML"],
)
