"""sphinx helper for paver"""
from paver.easy import *  # pylint: disable=unused-wildcard-import,wildcard-import


# pylint: disable=invalid-name,unused-import
try:
    import sphinx  # type: ignore
    has_sphinx = True
except ImportError:
    has_sphinx = False

try:
    import sphinx.cmd.build as sphinx_cmd  # type:ignore
    import sphinx.ext.apidoc as sphinx_apidoc # type:ignore
    is_sphinx_1_7 = True
except ImportError:
    import sphinx as sphinx_cmd
    import sphinx.apidoc as sphinx_apidoc # type:ignore
    is_sphinx_1_7 = False
# pylint: enable=invalid-name,unused-import


def _get_paths():
    """look up the options that determine where all of the files are."""
    opts = options
    docroot = path(opts.get('docroot', 'docs'))
    if not docroot.exists():
        raise BuildFailure("Sphinx documentation root (%s) does not exist."
                           % docroot)
    builddir = docroot / opts.get("builddir", ".build")
    builddir.mkdir_p()
    srcdir = docroot / opts.get("sourcedir", "")
    if not srcdir.exists():
        raise BuildFailure("Sphinx source file dir (%s) does not exist"
                           % srcdir)
    apidir = None
    if opts.get("apidir", "api"):
        apidir = srcdir / opts.get("apidir", "api")
        apidir.mkdir_p()
    htmldir = builddir / "html"
    htmldir.mkdir_p()
    doctrees = builddir / "doctrees"
    doctrees.mkdir_p()
    return Bunch(locals())


@task
def apidoc():
    """Run sphinx-apidoc

    Parameters are same to paver.doctools.html
    """
    options.order('sphinx', add_rest=True)
    paths = _get_paths()

    # First, auto-gen additional sources
    if paths.apidir:
        sphinxopts = ['-f', '-o', paths.apidir] + options.get("apidoc_opts", [])
        sphinxopts += options.setup.packages
        if not is_sphinx_1_7:
            # OptionParser compatibility for sphinx <1.7.0
            sphinxopts.insert(0, '')

        dry("sphinx-apidoc %s" % (" ".join(sphinxopts),), sphinx_apidoc.main, sphinxopts)

@task
def html():
    """Run sphinx-apidoc

    Parameters are same to paver.doctools.html
    """
    options.order('sphinx', add_rest=True)
    paths = _get_paths()
    # Then generate HTML tree
    sphinxopts = ['-b', 'html', '-d', paths.doctrees,
                  paths.srcdir, paths.htmldir]
    if not is_sphinx_1_7:
        # OptionParser compatibility for sphinx <1.7.0
        sphinxopts.insert(0, '')

    dry("sphinx-build %s" % (" ".join(sphinxopts),), sphinx_cmd.main, sphinxopts)
