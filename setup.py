from setuptools import setup, find_packages

setup(
    name="gcp_utils_sds",
    version="0.1.3",
    packages=find_packages(),
    install_requires=[
        "google-cloud-storage",
        "google-cloud-secret-manager",
        "google-auth",
        "google-auth-oauthlib",
        "pandas"
    ],
    author="Sam Taylor",
    author_email="2015samtaylor@gmail.com",
    description="Utilities functions for interacting with GCP tools",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
