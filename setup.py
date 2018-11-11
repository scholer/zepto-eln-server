
"""

Zepto ELN server: Flat-file Markdown-based wiki-style electronic laboratory notebook and journal.

Pico-inspired web app for serving Markdown documents as HTML-compiled web pages, written in Python.

For local and online journal presentation.

"""

# from distutils.core import setup
from setuptools import find_packages, setup


# To update entry points, just bump verison number and do `$ pip install -e .`

# update 'version' and 'download_url', as well as qpaint_analysis.__init__.__version__
setup(
    name='zepto-eln-server',  # old names: eln-md-pico-server
    description='Zepto ELN server: Flat-file Markdown-based wiki-style electronic laboratory notebook and journal.',
    long_description=__doc__,
    # long_description=open('README.txt').read(),
    version='0.1.0dev1',  # Update for each new version
    packages=find_packages(),  # List all packages (directories) to include in the source dist.
    # packages=[  # Manual listing is required for namespace distribution packages:
    #     'zepto_eln.eln_server', 'zepto_eln.md_utils', 'zepto_eln.eln_cli'
    # ],
    url='https://github.com/scholer/zepto-eln-server',
    # download_url='https://github.com/scholer/rsenv/tarball/0.1.0',
    download_url='https://github.com/scholer/zepto-eln-server/archive/master.zip',  # Update for each new version
    author='Rasmus Scholer Sorensen',
    author_email='rasmusscholer@gmail.com',
    license='GNU Affero General Public License v3',
    keywords=[
        "ELN", "Journal", "Research", "wiki", "web app",
        "Molecular biology", "Biotechnology", "Bioinformatics",
        "DNA", "DNA sequences", "sequence manipulation",
        "Data analysis", "Data processing", "plotting", "Data visualization",
        "Image analysis", "AFM", "Microscopy", "TEM", "HPLC", "Chromatograms",
    ],

    # Automatic script creation using entry points has largely super-seeded the "scripts" keyword.
    # you specify: name-of-executable-script: [package.]module:function
    # When the package is installed with pip, a script is automatically created (.exe for Windows).
    # The entry points are stored in ./gelutils.egg-info/entry_points.txt, which is used by pkg_resources.
    entry_points={
        'console_scripts': [
            # console_scripts should all be lower-case, else you may get an error when uninstalling:
            # 'rsenv=rsenv.rsenv_cli:rsenv_cli',
            # 'zepto-eln-server:zepto_eln.eln_server.eln_server_app:cli',
            # Edit: Use the flask runner to run the server app:
            #   $ activate <environment>
            #   $ set FLASK_APP=zepto_eln.eln_server.eln_server_app
            #   $ flask run
            # TODO: Create CLI for getting help, or just repurpose zepto-eln-server (and maybe a `man zepto` entry?).
            # TODO: Use
            # TODO:     app.config.from_object('zepto_eln.eln_server.default_settings')
            # TODO:     app.config.from_envvar('ZEPTO_ELN_SERVER_SETTINGS')
        ],
    },

    install_requires=[
        'flask',
        'jinja2',
        'pyyaml',
        'markdown',
        # 'requests',
        'click',     # Easy creation of command line interfaces (CLI).
        'python-dotenv',
    ],
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 4 - Beta',

        # Indicate who your project is intended for
        # 'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Education',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Healthcare Industry',

        # 'Topic :: Software Development :: Build Tools',
        'Topic :: Education',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
        'Topic :: Scientific/Engineering :: Medical Science Apps.',

        # Pick your license as you wish (should match "license" above)
        # 'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'License :: OSI Approved :: GNU Affero General Public License v3',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',

        'Operating System :: MacOS',
        'Operating System :: Microsoft',
        'Operating System :: POSIX :: Linux',
    ],

)
