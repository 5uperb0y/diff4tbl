#!/bin/bash
source ./tests/__utils__.sh
setup
cat << EOF > "${TMP_FILE1}"
id	N	TF	p
a1	3	T	0.1
a2	5	F	0.5
a3	4	T	0.2
EOF
cat << EOF > "${TMP_FILE2}"
id	N	TF	p
a1	3	T	0.1
a2	5	T	0.2
a4	2	F	0.6
EOF
cat << EOF > "${TMP_EXPECT}"
common
a1	3	T	0.1
addition
a4	2	F	0.6
deletion
a3	4	T	0.2
change
a2	5	F{T}	0.5{0.2}
EOF
python -m diff4tbl --lines --header --index id "${TMP_FILE1}" "${TMP_FILE2}" > "${TMP_ACTUAL}"
assert "${TMP_EXPECT}" "${TMP_ACTUAL}"