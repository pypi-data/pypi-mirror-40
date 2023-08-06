import setuptools

with open("README.MD", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="leer_vm",
    version="1.1",
    author="Crez Khansick",
    author_email="TetsuwanAtomu@tuta.io", 
    description="Virtual Machine for leer cryptocurrency",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/WTRMQDev/VM", 
    packages=setuptools.find_packages(exclude=["example", ".git", ".mypy_cache"]),
    package_data = {},
    include_package_data = True,
    install_requires=['secp256k1_zkp>=0.14.3', 'sha3'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
