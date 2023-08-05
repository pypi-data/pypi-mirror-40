
def calcdisp(location, xid, groups, results_name=''):
    import csv, os, re
    import pandas as pd
    from edgepy import util
    util.getdir()

    if results_name == '':
        results_name = util.namefromcsv(location)

    if not (os.path.exists(util.getdir.genelib + '/%s.csv' % xid)):
        print('Need genelib for the organism.')
    else:

        f = open(util.getdir.workspace + '/runcsv.txt', 'w')
        f.write(location + '\n')
        f.close()

        with open(util.getdir.workspace + '/groups.csv', 'w') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            writer.writerow(groups)

        loc = util.getdir.docs
        util.runR('calcdisp', loc)

        df = pd.read_csv(util.getdir.workspace + '/results.csv')
        df2 = pd.read_csv(util.getdir.genelib + '/%s.csv' % xid)
        df.rename(columns = {'Unnamed: 0':'geneNum'}, inplace = True)
        results = pd.merge(df, df2, how='left', left_on='geneNum', right_on='geneNum')
        results.to_csv(util.getdir.results + '/%s.csv' % results_name)

