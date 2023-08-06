import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="journeyplanner",
    version="1.0.0",
    license="MIT",
    author="Bytes & Brains",
    author_email="developers@bytesandbrains.com",
    description="Journey Planner API client library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/bytesandbrains/journeyplanner-python",
    packages=["journeyplanner"],
    test_suite="test",
)
