#!/bin/bash
trap cleanup EXIT TERM INT
source ./tests/__utils__.sh
setup
cat << EOF > "${TMP_FILE1}"
id	REF	QUAL
a1	C	40
a2	T	30
EOF
cat << EOF > "${TMP_FILE2}"
id	REF	ALT
a1	A	G
a2	T	G
EOF
cat << EOF > "${TMP_EXPECT}"
0	id	a1		a1
1	id	a2		a2
0	REF	C	|	A
1	REF	T		T
0	QUAL	40	>	
1	QUAL	30	>	
0	ALT		<	G
1	ALT		<	G
EOF
python -m diff4tbl -y "${TMP_FILE1}" "${TMP_FILE2}" > "${TMP_ACTUAL}"
assert "${TMP_EXPECT}" "${TMP_ACTUAL}"