from setuptools import find_packages, setup

setup(
    name="hpl_solver",
    version="0.2",
    packages=find_packages(),
    url="https://github.com/MIPT-Virtual-Labs/HPL_solver.git",
    author="AbrashevaVeronika",
    author_email="8vero0810@gmail.com",
    install_requires=["numpy", "pandas", "scipy", "pydantic", "plotly-express"],
)
