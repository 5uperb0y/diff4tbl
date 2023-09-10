#!/bin/bash
source ./tests/__utils__.sh
setup
cat << EOF > "${TMP_FILE1}"
id	REF	ALT	QUAL
a1	A	G	40
a2	C	G	50
EOF
cat << EOF > "${TMP_FILE2}"
id	REF	ALT	FILTER
a1	T	G	PASSED
a2	C	G	FAILED
EOF
cat << EOF > "${TMP_EXPECT}"
id	REF
a1	A{T}
a2	C
EOF
python main.py -c id,REF "${TMP_FILE1}" "${TMP_FILE2}" > "${TMP_ACTUAL}"
assert "${TMP_EXPECT}" "${TMP_ACTUAL}"