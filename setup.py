"""
Flask 原理与实战 - 安装脚本
Flask Principles and Practice - Setup Script
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="flask-principles-and-practice",
    version="1.0.0",
    author="Flask Tutorial",
    author_email="contact@example.com",
    description="Flask 原理与实战 - 完整教程和示例",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/flask-principles-and-practice",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Framework :: Flask",
    ],
    python_requires=">=3.8",
    install_requires=[
        "Flask>=3.0.0",
        "Flask-SQLAlchemy>=3.1.1",
        "Flask-WTF>=1.2.1",
        "Flask-Login>=0.6.3",
        "Flask-Bcrypt>=1.0.1",
        "Flask-RESTful>=0.3.10",
        "Flask-CORS>=4.0.0",
        "Flask-Migrate>=4.0.5",
        "Flask-Caching>=2.1.0",
        "python-dotenv>=1.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.3",
            "pytest-flask>=1.3.0",
            "pytest-cov>=4.1.0",
            "flake8>=6.1.0",
            "black>=23.12.0",
            "isort>=5.13.2",
        ],
        "prod": [
            "gunicorn>=21.2.0",
            "gevent>=23.9.1",
            "psycopg2-binary>=2.9.9",
        ],
    },
    entry_points={
        "console_scripts": [
            "flask-tutorial=scripts.cli:main",
        ],
    },
)
