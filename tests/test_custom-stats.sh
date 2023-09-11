#!/bin/bash
source ./tests/__utils__.sh
setup
trap cleanup EXIT TERM INT
cat << EOF > "${TMP_FILE1}"
id	REF	ALT	QUAL	p
a2	T	G	50	0.01
a1	C	G	30	0.05
EOF
cat << EOF > "${TMP_FILE2}"
id	REF	ALT	QUAL	p
a2	T	G	50	0.05
a1	A	G	30	0.01
EOF
cat << EOF > "${TMP_EXPECT}"
REF	kappa	0.3333333333333333
QUAL	corr	0.9999999999999999
p	md	0.04
EOF
python -m diff4tbl --stats -c REF:kappa,QUAL:corr,p:md "${TMP_FILE1}" "${TMP_FILE2}" > "${TMP_ACTUAL}"
assert "${TMP_EXPECT}" "${TMP_ACTUAL}"