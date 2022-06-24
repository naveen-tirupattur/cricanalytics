from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name="cricanalytics",
      description="Cricket Analytics",
      license="MIT",
      install_requires=["requests", "bs4", "dateparser", "lxml", "pandas"],
      author="Naveen Tirupattur",
      author_email="naveen.tirupattur@gmail.com",
      packages = find_packages(),
      keywords= "cricket, analytics, data science",
      zip_safe = True)
