import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pubsub_util",
    version="0.0.3",
    author="Ivana Mance",
    author_email="ivana.mance@photomath.com",
    description="Util for subscribing or publishing messages to Googles PubSub topics",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/photomath/pubsub-util.git",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(),
    py_modules=['pubsub_util'],
    python_requires=">=3.9",
)
