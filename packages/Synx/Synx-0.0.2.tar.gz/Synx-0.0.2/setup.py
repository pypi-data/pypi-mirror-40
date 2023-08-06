import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Synx",
    version="0.0.2",
    author="Eliezer Odjao",
    author_email="eliezerodjaoofficial@gmail.com",
    description="A framework for easy and simple creation of user interfaces for Python applications",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://eliezerodjao.com/desktop/portfolio.php?sent=synx",
    license="Proprietary",
    packages=setuptools.find_packages(),
    include_package_data=True,
    keywords='GUI graphical user interface UI UX',
    install_requires=['Pillow'],
    python_requires='~=3.3',
    classifiers=[
        "Environment :: Win32 (MS Windows)",
        "Environment :: Console",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.4",
        "License :: Other/Proprietary License",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX :: Linux",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    project_urls={
    'Documentation': 'https://eliezerodjao.com/docs/Synx_User_Documentation.docx',
    'Source': 'https://eliezerodjao.com/desktop/portfolio.php?sent=synx'
    },
)
