"""Water allocation models for RTC-Tools 2."""
import sys

from setuptools import find_packages, setup

import versioneer

DOCLINES = __doc__.split("\n")

CLASSIFIERS = """\
Development Status :: 4 - Beta
Intended Audience :: Science/Research
Intended Audience :: Information Technology
License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)
Programming Language :: Other
Topic :: Scientific/Engineering :: GIS
Topic :: Scientific/Engineering :: Mathematics
Topic :: Scientific/Engineering :: Physics
Operating System :: Microsoft :: Windows
Operating System :: POSIX
Operating System :: Unix
Operating System :: MacOS
"""

# TODO: Remove when support for python_requires is standard.
if sys.version_info < (3, 5):
    sys.exit("Sorry, Python 3.5 or newer is required.")

setup(
    name='rtc-tools-water-allocation',
    version=versioneer.get_version(),
    description=DOCLINES[0],
    classifiers=[_f for _f in CLASSIFIERS.split('\n') if _f],
    url='http://www.deltares.nl/en/software/rtc-tools/',
    author='Deltares',
    maintainer='Jack Vreeken',
    license='LGPLv3',
    keywords='rtctools optimization water allocation',
    platforms=['Windows', 'Linux', 'Mac OS-X', 'Unix'],
    packages=find_packages("src"),
    package_dir={"": "src"},
    install_requires=[
        'rtc-tools >= 2.3.0a2',
        'rtc-tools-channel-flow == 1.*',
        'numpy',
        'casadi'
    ],
    python_requires='>=3.5',
    cmdclass=versioneer.get_cmdclass(),
)
