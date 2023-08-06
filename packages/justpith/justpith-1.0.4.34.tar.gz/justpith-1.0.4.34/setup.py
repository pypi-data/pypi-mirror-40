from setuptools import setup

setup(
    name = "justpith",
    version = "1.0.4.34",
    author = "Antonio Caristia",
    author_email = "a.caristia@gmail.com",
    description = ("Core code for justpith infrastructure"),
    license = "GPL",
    keywords = "justpith's core",
    url = "http://packages.python.org/justpith",
    packages=['justpith','justpith.rabbit', 'justpith.mongo','justpith.mongo.teacher', 'justpith.mongo.factorizer', 'justpith.mongo.common', 'justpith.mongo.controller', 'justpith.mongo.reccomender', 'justpith.mongo.web_app', 'justpith.mongo.news_consumer', 'justpith.mongo.chat', 'justpith.mongo.social_worker','justpith.logger', 'justpith.util','justpith.social', 'justpith.mongo.affinity'],
    install_requires=[
          'pika','pymongo','fluent-logger','nltk','stop-words','PyYAML'
    ],
    include_package_data=True,
    zip_safe=False
)
