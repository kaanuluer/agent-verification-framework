"""
Agent Verification Framework - Setup Script
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="agent-verification-framework",
    version="0.1.0",
    author="Agent Verification Team",
    author_email="info@example.com",
    description="Agent'ların yaptığı işlemleri ve intent'lerini doğrulamak için framework",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/example/agent-verification-framework",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Security",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=[
        "python-dateutil>=2.8.2",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
            "black>=23.7.0",
            "flake8>=6.1.0",
            "mypy>=1.5.0",
        ],
        "ml": [
            "numpy>=1.24.0",
            "pandas>=2.0.0",
            "scikit-learn>=1.3.0",
        ],
        "distributed": [
            "redis>=4.6.0",
        ],
        "web": [
            "flask>=2.3.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "agent-verify=agent_verification.cli:main",
        ],
    },
)
