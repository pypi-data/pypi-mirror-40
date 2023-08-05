from setuptools import setup, find_packages


with open("README.md", "r") as fh:
    long_description = fh.read()

if __name__ == "__main__":
    setup(
        name="kafkahelpers",
        version="0.0.3",
        description="Helpers for aiokafka clients",
        long_description=long_description,
        long_description_content_type="text/markdown",
        url="https://github.com/jhjaggars/kafkahelpers",
        author="Jesse Jaggars",
        author_email="jhjaggars@gmail.com",
        packages=find_packages(),
        install_requires=["kafka-python", "attr"],
        package_data={'': ['LICENSE']},
        license='Apache 2.0',
        classifiers=[
            'Development Status :: 5 - Production/Stable',
            'Intended Audience :: Developers',
            'Natural Language :: English',
            'License :: OSI Approved :: Apache Software License',
            'Programming Language :: Python',
            'Programming Language :: Python :: 3.6',
        ],
        include_package_data=True,
    )
