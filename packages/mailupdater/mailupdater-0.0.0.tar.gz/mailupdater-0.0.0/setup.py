import setuptools

setuptools.setup(
    name="mailupdater",
    version="0.0.0",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    description="Easily send mail updates to yourself.",
    url="https://github.com/ychnlgy/MailUpdater",
    author="Yuchen Li",
    author_email="ychnlgy@gmail.com",
    license="MIT",
    packages=setuptools.find_packages(),
    include_package_data=True
)
