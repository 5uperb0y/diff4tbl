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
a2	T	G	50	0.05
a1	A	G	30	0.01
EOF
cat << EOF > "${TMP_EXPECT}"
QUAL	corr	0.9999999999999999
EOF
python -m diff4tbl --stats -c QUAL:corr "${TMP_FILE1}" "${TMP_FILE2}" > "${TMP_ACTUAL}"
assert "${TMP_EXPECT}" "${TMP_ACTUAL}"