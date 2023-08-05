from setuptools import setup, find_packages
setup(
    name = "qvtool",
    version = "0.0.1",
    author = "muxingMax",
    author_email = "log_e@qq.com",
    description = "open port of ipc",
    py_modules = "qvtool",
    packages = find_packages(),
    entry_points = '''
        [console_scripts]
        qvtool=qvtool:main
    ''',
)

