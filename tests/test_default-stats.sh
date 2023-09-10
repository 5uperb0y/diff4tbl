#!/bin/bash
source ./tests/__utils__.sh
setup
trap cleanup EXIT TERM INT
cat << EOF > "${TMP_FILE1}"
id	REF	ALT	QUAL	FILTER
a2	T	G	50	PASSED
a1	C	G	30	FAILED
EOF
cat << EOF > "${TMP_FILE2}"
id	REF	ALT	QUAL	p
a2	T	G	70	0.05
a1	A	G	50	0.01
EOF
cat << EOF > "${TMP_EXPECT}"
id	identity	1.0
REF	identity	0.5
ALT	identity	1.0
QUAL	mean	20.0
EOF
python ./diff4tbl/main.py --stats "${TMP_FILE1}" "${TMP_FILE2}" > "${TMP_ACTUAL}"
assert "${TMP_EXPECT}" "${TMP_ACTUAL}"