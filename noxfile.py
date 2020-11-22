import nox


@nox.session
def tests(session):
    session.install('.')
    session.install('pytest', 'pytest-coverage')
    session.run('pytest')
