import nox


@nox.session
def tests(session):
    session.install('.')
    session.install('pytest', 'pytest-coverage')
    session.run('pytest', '--cov=bv2', '--cov-branch', 'tests/', *session.posargs)
