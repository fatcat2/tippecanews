from __future__ import absolute_import
import nox

BLACK_PATHS = [
        "app.py",
        "info_getters.py"
]


@nox.session(python="3.7")
def lint(session):
    """Run linters.
    Returns a failure if the linters find linting errors or sufficiently
    serious code quality issues.
    """
    session.install("flake8", "black")
    session.install("-r", "requirements.txt")
    session.run("black", "--check", *BLACK_PATHS)
    session.run("flake8", *BLACK_PATHS)


@nox.session(python="3.7")
def blacken(session):
    """Run black.
    """
    session.install("black")
    session.run("black", *BLACK_PATHS)


def default(session):
    # Install all test dependencies, then install this package in-place.
    session.install("mock", "pytest", "pytest-cov", "pytest-asyncio")
    # session.install("-e", ".")
    session.install("-r", "requirements.txt")
    # Run py.test against the unit tests.
    session.run(
        "py.test",
        "--quiet",
        # "--cov=util",
        # "--cov=connector",
        "--cov-append",
        "--cov-config=.coveragerc",
        "--cov-report=",
        "--cov-fail-under=0",
        # os.path.join("tests"),
        *session.posargs
    )


@nox.session(python=["3.6", "3.7"])
def unit(session):
    default(session)


# @nox.session(python="3.7")
# def cover(session):
# """Run the final coverage report.
# This outputs the coverage report aggregating coverage from the unit
# test runs (not system test runs), and then erases coverage data.
# """
# session.install("coverage", "pytest-cov")
# session.run("coverage", "report", "--show-missing", "--fail-under=100")

# session.run("coverage", "erase")
