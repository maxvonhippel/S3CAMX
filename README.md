#S3CAMX: S3CAM + Symbolic Execution

S3CAM uses simulations and symboolic execution to find falsifications to safety properties of Hybrid Systems. Please refer to the below publications for details:

- Zutshi, Sankaranarayanan, Deshmukh, Jin.
        "Symbolic-Numeric Reachability Analysis of Closed-Loop Control Software"
        Proceedings of the 19th International Conference on Hybrid Systems: Computation and Control. ACM, 2016.


- Zutshi, Deshmukh, Sankaranarayanan, Kapinski.
        "Multiple shooting, cegar-based falsification for hybrid systems."
        Proceedings of the 14th International Conference on Embedded Software. ACM, 2014.

##Overview
The S3CAMX package implements both S3CAMX and S3CAM algorithms. 

##Dependencies

S3CAMX is written in Python 2.7, and depends on several python packages. Additionally, the S3CAMX algorithm requires Z3 and symbolic paths generated by Pathcrawler. Matlab and Simulink are required if the given system under test is implemented using them. S-Taliro is required only to compare and reproduce the results in the paper. These dependencies are listed below.

- [Python 2.7.x](https://www.python.org/downloads/) and its packages. **Not required if using Package A**.
- [MATLAB R2015b (and Simulink)](http://www.mathworks.com/downloads/):
required to simulate systems which use Matlab based simulators: AFC.
- [Pathcrawler](http://pathcrawler-online.com/doWelcome#about) output:
 Pre-computed symbolic paths required for symbolic execution.
- [Z3](https://z3.codeplex.com/):
Required for running symbolic execution of the controller (**included in Package A**).
- [S-Taliro 1.6](https://sites.google.com/a/asu.edu/s-taliro/s-taliro):
Needed to reproduce comparison results (**included in Package A**).

## Distributions

The distribution package was tested on Ubuntu 12.04 and 14.04 and should work on Python 2.7.x (**Python 2.7.3 and higher**).

We provide two packages of S3CAMX

- **Package A (recommended)**: pre-compiled frozen package built using cx_freeze.
- **Package B**: contains all required sources.

###Installing from Package A

Package A is a pre-compiled distribution and does not require the installation of Python or its packages including Z3. However, Matlab + Simulink and S-Taliro still need to be installed. It is recommended that the user tries to run this before moving on to Package B. The package has been tested with a fresh install of Ubuntu ?, but a library mismatch can cause unexpected behavior, in which case a fallback to Package B is advised.

###Installing from Package B
This package contains only sources and requires the user to compile and obtain the necessary dependencies.
##Installation

###Installing Python and Required Packages
1. Install [Python 2.7.x](https://www.python.org/downloads/)<br>
> **Note:** The Python build must be configured with the option --enable-shared.
This is not the case with the default Python installation found in both Ubuntu 12.04 and hence a different local installation is required. This is only needed to interface Matlab with Python [Matlab -> Python], which is used to generate test results by S-Taliro on systems with simulators in Python.
For more details, refer to: [--enable-shared](https://www.mathworks.com/help/matlab/matlab_external/undefined-variable-py-or-function-py-command.html#buialof-65)<br><br>
e.g. if using [pyenv](https://github.com/yyuu/pyenv), then CONFIGURE\_OPTS must be set as below
<br>
`export CONFIGURE_OPTS='--enable-shared --enable-unicode=ucs4'` <br>
before issuing <br>
`pyenv install 2.7.x`

- Update Repository<br>
`sudo apt-get update`

- Install basic dependencies<br>
`sudo apt-get install build-essential python-dev`

- [pip](https://pip.pypa.io/en/stable/installing/)<br>
Download [get-pip.py](https://bootstrap.pypa.io/get-pip.py) and install using <br>
`sudo python ./get-pip.py`

- [pyparsing](https://pypi.python.org/pypi/pyparsing)<br>
`sudo -H pip install pyparsing`

- [numpy 1.10.4](http://www.numpy.org/)<br>
    - Install or upgrade numpy. <br>
     `sudo -H pip install numpy --upgrade`
    - Install dependencies: If the above step gives an error due to missing dependencies, then either the user can manually resolve them or use `sudo apt-get build-dep python-numpy` to install an exhaustive list.

- [scipy 0.16.1](http://www.scipy.org/)<br>
    - Install or upgrade scipy. <br>
     `sudo -H pip install scipy --upgrade`
    - If the above step gives an error due to missing dependencies, (usually blas, and gfortran) they can be installed using `sudo apt-get install libatlas-base-dev gfortran`. If this does not work then an exhaustive list can be installed using `sudo apt-get build-dep python-scipy`

- [blessings](https://pypi.python.org/pypi/blessings/)<br>
`sudo -H pip install blessings

- [networkx](https://networkx.github.io/)<br>
`sudo -H pip install networkx

- [matplotlib 1.5.1](http://matplotlib.org/)<br>
    - Install or upgrade matplotlib <br>
`sudo -H pip install matplotlib --upgrade`
    - In the case of unresolved dependencies try to install the commonly missing packages: libfreetpy and libpng <br>
`sudo apt-get install libpng-dev libfreetype6-dev` <br>
Else, use the below for an exhaustive resolution <br>
`sudo apt-get build-dep python-matplotlib`

- [tqdm](https://pypi.python.org/pypi/tqdm)<br>
`sudo -H pip install tqdm`

- [sh](https://pypi.python.org/pypi/sh)<br>
`sudo -H pip install sh`

###Installing Git
`sudo apt-get install git`

### Installing MATLAB

- MATLAB R2015b or higher. <br>
The below toolboxes may be required:
    - Simulink: required for running example **AFC**
    - Optimization toolbox: required for running S-Taliro for comparison

> **Note:**
>  The version R2015b is required and earlier versions will not work due to missing features.

S3CAMX uses both MATLAB -> Python and Python -> MATLAB interface for running S-Taliro on systems based on Python simulators and for analyzing systems based on MATLAB simulator respectively. These two interfaces are provided by MATLAB and can be set up as follows.

#### Setting up MATLAB -> Python

References:

- [Getting Started with Python](http://www.mathworks.com/help/matlab/getting-started_buik_wp-3.html)
- [Common Issues](http://www.mathworks.com/help/matlab/matlab_external/undefined-variable-py-or-function-py-command.html)

#### Setting up Python -> MATLAB

Reference: [MATLAB Engine for Python](https://www.mathworks.com/help/matlab/matlab_external/install-the-matlab-engine-for-python.html)

### Installing the Rest

Install Z3, S-Taliro and Pathcrawler using their respective instructions.

## Obtaining the Sources

- py2z3<br>
`git clone https://github.com/zutshi/py2z3.git`
- S3CAMX<br>
`git clone https://github.com/zutshi/S3CAMX.git`

## RUNNING S3CAMX

- To configure paths, please modify `set_path.sh` and update the paths for Z3's Python bindingd and py2z3.

- Start and share minimal Matlab session (optional):
	- Open a terminal and type
	`matlab& -nojvm -nodisplay -nosplash`
	- In Matlab, type the below to share the matlab engine
	`matlab.engine.shareEngine('<engine_name>')`
- Compile each system's controller by running <br>
`compile_examples.sh`

- To simulate a system run, use
`./secam.py -f <system path> -s <number of simulations>`

- To run S3CAM, use
`./secam.py -f <system path> -c`

- To run S3CAMX, use
`./secam.py -f <system path> -x pathcrawler -r trace -t tree`

- A shared Matlab engine can be provided as below.
`./secam.py -f <system path> [options] --meng <engine_name>`
This engine will be used to simulate systems which use Matlab simulators. If it is not provided, a Matlab engine will be started. A shared engine is preferred as launching a new Matlab engine is time consuming.
