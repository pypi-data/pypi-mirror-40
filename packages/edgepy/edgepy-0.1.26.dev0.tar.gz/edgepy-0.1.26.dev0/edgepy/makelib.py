
def make(location='', xid=''):
    from BCBio import GFF
    import pandas as pd
    from edgepy import util
    import os

    if location == '':
        location = input('Please enter the location of the gff file: ')

    if xid == '':
        xid = input('Please enter an identifier for the organism: ')

    util.getdir()
    sdir = util.getdir.genelib
    sdir = sdir + '/%s.csv' % xid

    if os.path.exists(sdir):
        print('This genelib already exists.')
    else:
        if 'gff.gz' in location:
            import gzip, shutil
            with gzip.open(location, 'rb') as f_in:
                with open(location.rstrip('.gz'), 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)

            location = location.rstrip('.gz')

        in_handle = open(location)
        limit_info = dict(gff_type=['protein', 'gene', 'mRNA', 'CDS'],)

        dbxrefs= []
        gene_names = []
        gene_ids = []
        locus_tags = []

        for rec in GFF.parse(in_handle, limit_info=limit_info):
            for feature in rec.features:
                dbxref = feature.qualifiers['Dbxref'][0]
                gene_name = feature.qualifiers['Name'][0]
                gene_id = feature.qualifiers['ID'][0]
                locus_tag = feature.qualifiers['locus_tag'][0]

                dbxref = dbxref.lstrip('GeneID:')

                dbxrefs.append(dbxref)
                gene_names.append(gene_name)
                gene_ids.append(gene_id)
                locus_tags.append(locus_tag)

        d = {'geneNum': gene_ids, 'dbxref': dbxrefs, 'geneName': gene_names, 'locus_tag': locus_tags}
        df = pd.DataFrame(d)

        df.to_csv(sdir, index=False)
