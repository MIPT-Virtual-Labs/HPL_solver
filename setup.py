from setuptools import find_packages, setup

setup(
    name="hpl_solver",
    version="0.1",
    packages=find_packages(),
    url="https://github.com/MIPT-Virtual-Labs/HPL_solver.git",
    author="",
    author_email="",
    include_package_data=True,
    package_data={"": ["./bin/*"]},
    # install_requires=["numpy", "pandas", "plotly-express", "pydantic"],
)