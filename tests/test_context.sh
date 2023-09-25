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
id	N	TF
a1	3	T
a2	5	F{T}
EOF
python -m diff4tbl --context --header --index id --fields id,N,TF "${TMP_FILE1}" "${TMP_FILE2}" > "${TMP_ACTUAL}"
assert "${TMP_EXPECT}" "${TMP_ACTUAL}"