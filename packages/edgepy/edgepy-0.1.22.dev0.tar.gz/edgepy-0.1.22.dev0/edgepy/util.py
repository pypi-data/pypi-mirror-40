def getdir():
    from edgepy import ref
    sdir = ref.__file__
    sdir = sdir.rstrip('.py').rstrip('/ref')

    getdir.package = sdir
    getdir.counts = sdir + '/docs/counts'
    getdir.genelib = sdir + '/docs/genelib'
    getdir.info = sdir + '/docs/info'
    getdir.plots = sdir + '/docs/plots'
    getdir.results = sdir + '/docs/results'
    getdir.rfiles = sdir + '/docs/rfiles'
    getdir.trimmed_results = sdir + '/docs/trimmed_results'
    getdir.workspace = sdir + '/docs/workspace'


