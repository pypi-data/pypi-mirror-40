from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="dcfgrpc",
    version="0.1.0",
    author="cyy03576",
    author_email="cyy03576@keti.re.kr",
    description="DCF API for gRPC",
    packages=find_packages(),
    license="MIT",
    python_requires='>=2.7,!=3.0.*,!=3.1.*,!=3.2.*,!=3.3.*',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/DigitalCompanion-KETI",
    classifiers=[
        "License :: OSI Approved :: MIT License",
    ],    
)

