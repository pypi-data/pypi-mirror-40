from setuptools import setup

setup(name="gameserver_response_parser",
        version="0.1.1",
        description="a library to parse the responses of gameservers",
        url="https://github.com/991jo/gameserver_response_parser",
        author="992jo",
        license="WTF",
        packages=["gameserver_response_parser"],
        test_suite="gameserver_response_parser.test.srcds_new_format",
        include_package_data=True)
