def getdir():
    import os
    from edgepy import ref

    sdir = ref.__file__
    sdir = sdir.rstrip('.py').rstrip('/ref')

    getdir.package = sdir
    getdir.docs = sdir + '/docs'
    getdir.counts = sdir + '/docs/counts'
    getdir.genelib = sdir + '/docs/genelib'
    getdir.info = sdir + '/docs/info'
    getdir.plots = sdir + '/docs/plots'
    getdir.results = sdir + '/docs/results'
    getdir.rfiles = sdir + '/docs/rfiles'
    getdir.trimmed_results = sdir + '/docs/trimmed_results'
    getdir.workspace = sdir + '/docs/workspace'

    if os.path.exists(sdir + '/docs/counts/empty.txt'):
        flist = ['counts', 'genelib', 'info', 'plots', 'results', 'trimmed_results', 'workspace']
        for f in flist:
            if os.path.exists(sdir + '/docs/%s/empty.txt' % f):
                os.remove(sdir + '/docs/%s/empty.txt' % f)


def runR(rname, argument=''):
    from edgepy import ref
    import subprocess

    sdir = ref.__file__
    sdir = sdir.rstrip('.py').rstrip('/ref')
    rfiles = sdir + '/docs/rfiles'
    rfile = rfiles + '/%s.R' % rname

    command = ['Rscript', rfile, '--args', argument]
    subprocess.call(command, universal_newlines=True)


def namefromcsv(string):
    l = string.split('/')
    last = l.pop()
    s = last.rstrip('.csv')
    return s


