import setuptools
from cx_Freeze import setup, Executable

with open("README.md", "r") as fh:
    long_description = fh.read()

with open('gnucash_importer/version.py') as f:
    exec(f.read())

# FIXME build with setup.py but do not execute (not find module cli)
buildOptions = dict(packages = ['gnucash_importer'], excludes = [])
base = 'Console'
executables = [
    Executable(
        'gnucash_importer/run_app.py',
        base = base,
        targetName = 'gmi'
    )
]

setup(
# setuptools.setup(
    name = "gnucash_magical_importer",
    version = __version__,
    author = "Jefferson Campos",
    author_email = "jefferson@jeffersoncampos.eti.br",
    description = "Parse data source (ofx, qif, csv, etc.) and import to Gnucash file.",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = "https://github.com/foguinhoperuca/gnucash_magical_importer",
    packages = setuptools.find_packages(),
    python_requires='>=3.6',
    classifiers = [
        'Development Status :: 3 - Alpha',
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    # package_data = {'test/fixtures': ['test/fixtures/*']},
    # data_files=[('my_data', ['data/data_file'])],  # Optional
    # entry_points={  # Optional
    #     'console_scripts': [
    #         'parser=parser:main',
    #     ],
    # },
    # options = {"build_exe": buildOptions},
    options = dict(build_exe = buildOptions),
    executables = executables
)
