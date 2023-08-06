from setuptools import setup, find_packages
setup(
    name="redditmonitor",
    version="0.2.1",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'monitor_comments = redditmonitor.monitor:monitor_comments',
            'monitor_submissions = redditmonitor.monitor:monitor_submissions',
        ]
    },
    install_requires=[
    	'praw>=6',
    ],
)