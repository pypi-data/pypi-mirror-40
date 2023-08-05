# the imports
from setuptools import setup


setup(
    name='statepub',
    version='0.0.0.2',
    description='A program for publishing the current state of a computing machine to the MQTT network',
    url='https://github.com/the16thpythonist/statepub',
    author='Jonas Teufel',
    author_email='jonseb1998@gmail.com',
    license='MIT',
    packages=[
        'statepub'
        '/scripts'
    ],
    install_requires=[
        'psutil',
        'paho-mqtt',
        'click'
    ],
    entry_points={
        'console_scripts':
            ['publish-status=statepub.scripts.publishstatus:cli']
    },
    python_requires='~=3.5',
    zip_safe=False
)
