#!/bin/bash
source ./tests/__utils__.sh
setup
cat << EOF > "${TMP_FILE1}"
id	N	TF	p
a1	3	T	0.1
a2	5	F	0.5
EOF
cat << EOF > "${TMP_FILE2}"
id	N	TF	p
a1	3	T	0.1
a2	5	T	0.2
EOF
cat << EOF > "${TMP_EXPECT}"
id	identity	1.0
N	md	0.0
TF	kappa	0.0
p	corr	0.9999999999999998
EOF
python -m diff4tbl --stats --header --index id --fields id:identity,N:md,TF:kappa,p:corr "${TMP_FILE1}" "${TMP_FILE2}" > "${TMP_ACTUAL}"
assert "${TMP_EXPECT}" "${TMP_ACTUAL}"