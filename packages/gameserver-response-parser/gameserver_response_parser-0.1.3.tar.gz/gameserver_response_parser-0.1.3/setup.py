from setuptools import setup

def readme():
    with open('README.rst') as f:
        return f.read()

setup(name="gameserver_response_parser",
        version="0.1.3",
        description="a library to parse the responses of gameservers",
        long_description=readme(),
        url="https://github.com/991jo/gameserver_response_parser",
        author="992jo",
        license="WTF",
        packages=["gameserver_response_parser"],
        test_suite="gameserver_response_parser.test.srcds_new_format",
        include_package_data=True)
