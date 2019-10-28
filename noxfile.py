import glob

import nox


@nox.session(python="3")
def blacken(session):
    """Run black code formater."""
    session.install("black==19.3b0", "isort==4.3.21")
    files = ["noxfile.py"] + glob.glob("winterbloom_sol/*.py")
    session.run("black", *files)
    session.run("isort", "--recursive", *files)


@nox.session(python="3")
def lint(session):
    session.install("flake8==3.7.8", "black==19.3b0")
    files = ["noxfile.py"] + glob.glob("winterbloom_sol/*.py")
    session.run("black", "--check", *files)
    session.run("flake8", *files)


@nox.session(python="3")
def test(session):
    session.install("pytest", "pytest-cov")
    session.run("python", "-m", "pytest", 
        "--cov=winterbloom_sol",
        "--cov-report=term-missing",
        "tests")
