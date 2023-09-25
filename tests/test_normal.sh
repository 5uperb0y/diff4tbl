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
a1	id	a1		a1
a1	N	3		3
a1	TF	T		T
a2	id	a2		a2
a2	N	5		5
a2	TF	F	|	T
EOF
python -m diff4tbl --normal --header --index id --exclude-fields p "${TMP_FILE1}" "${TMP_FILE2}" > "${TMP_ACTUAL}"
assert "${TMP_EXPECT}" "${TMP_ACTUAL}"