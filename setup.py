from distutils.core import setup

setup(
    name='pjm-ensam-sph',
    version='1',
    packages=['app', 'app.gui', 'app.save', 'app.facade', 'app.solver', 'app.solver.model', 'app.solver.helper',
              'app.geometry'],
    url='sph.iresam.org',
    license='MIT',
    author='Tycho Tatitscheff',
    author_email='tycho.tatitscheff@ensam.eu',
    description=''
)
