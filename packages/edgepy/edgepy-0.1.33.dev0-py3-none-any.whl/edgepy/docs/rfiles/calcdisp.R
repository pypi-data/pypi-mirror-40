
suppressMessages(library(edgeR))
# library(stringr)
myArgs = commandArgs(trailingOnly = TRUE)
wkdir = myArgs[[1]]

# wkdir = str_replace(wkdir, '/rfiles', '')
run_csv = readLines(paste(wkdir, "/workspace/runcsv.txt", sep=""))
groups = read.table(paste(wkdir, "/workspace/groups.csv", sep=""), sep=",")

sampleInfo = read.table(run_csv, header=TRUE, sep=",", row.names=1)

dgeFull = DGEList(sampleInfo, group=unlist(groups))

keep = rowSums(cpm(dgeFull)>1) >= 2
dgeFull = dgeFull[keep, , keep.lib.sizes=FALSE]
dgeFull = DGEList(dgeFull$counts[apply(dgeFull$counts,1,sum) != 0,], group=dgeFull$samples$group)
dgeFull = calcNormFactors(dgeFull, method="TMM")

dgeFullC = estimateCommonDisp(dgeFull)
dgeFullT = estimateTagwiseDisp(dgeFullC)
dgeTest = exactTest(dgeFullT)

etp = topTags(dgeTest, n=100000)
etp$table$logFC = -etp$table$logFC

filename = paste(wkdir, "/workspace/results.csv", sep="")
write.csv(etp$table, filename)