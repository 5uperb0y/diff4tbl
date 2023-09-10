#!/bin/bash
source ./tests/__utils__.sh
setup
trap cleanup EXIT TERM INT
cat << EOF > "${TMP_FILE1}"
id	REF	ALT	N	FILTER	p
a2	T	G	90	PASSED	0.01
a1	C	G	20	FAILED	0.4
b1	A	CC	80	PASSED	0.03
EOF
cat << EOF > "${TMP_FILE2}"
id	REF	ALT		FILTER
a2		G	10	FAILED
a1	C	A	20	FAILED
b1	A	CC	80	PASSED
b2	G	A	10	FAILED
EOF
cat << EOF > "${TMP_EXPECT}"
id	REF	ALT	N{}	FILTER	p{}
a2	T{}	G	90{10}	PASSED{FAILED}	0.01{}
a1	C	G{A}	20	FAILED	0.4{}
b1	A	CC	80	PASSED	0.03{}
{b2}	{G}	{A}	{10}	{FAILED}	
EOF
python -m diff4tbl "${TMP_FILE1}" "${TMP_FILE2}" > "${TMP_ACTUAL}"
assert "${TMP_EXPECT}" "${TMP_ACTUAL}"