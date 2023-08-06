from setuptools import setup

setup(
    name='kagenda',
    version='1.1.0',
    packages=['kagenda'],
    url='https://github.com/kisom/kagenda',
    license='MIT',
    author='kyle',
    author_email='coder@kyleisom.net',
    description='Every morning, I like to get my daily agenda.',
    scripts=['bin/agenda'],
    install_requires=[
        "darkskylib",
        "google-api-python-client",
        "natural",
        "oauth2client",
        "pyserial",
        "pyttsx3",
        "pytz"
    ]
)
