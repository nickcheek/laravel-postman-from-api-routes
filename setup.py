from setuptools import setup, find_packages

setup(
    name="laravel-to-postman",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[],
    entry_points={
        "console_scripts": [
            "laravel2postman=laravel_to_postman.main:cli",
        ],
    },
    author="Nicholas Cheek",
    author_email="nick@nicholascheek.com",
    description="Convert Laravel routes to Postman collection",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/nickcheek/laravel-postman-from-api-routes",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)