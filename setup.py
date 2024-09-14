from setuptools import setup, find_packages

setup(
    name="task_cli",
    version="0.1.0",
    description="A CLI Task tracker App.",
    author="Ankit Kumar",
    packages=find_packages(include=["task_cli", "task_cli.*"]),
    install_requires=[
        "typer",
        "rich",
    ],
    entry_points={
        "console_scripts": [
            "task_cli = task_cli.__main__:cli",
        ],
    },
    python_requires=">=3.7",
)
