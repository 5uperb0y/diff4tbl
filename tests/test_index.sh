#!/bin/bash
source ./tests/__utils__.sh
setup
trap cleanup EXIT TERM INT
cat << EOF > "${TMP_FILE1}"
id	REF	ALT
a2	T	G
a1	C	G
EOF
cat << EOF > "${TMP_FILE2}"
id	REF	ALT
a3	T	G
a1	A	G
EOF
cat << EOF > "${TMP_EXPECT}"
id	REF	ALT
a1	C{A}	G
EOF
python -m diff4tbl -i "id" "${TMP_FILE1}" "${TMP_FILE2}" > "${TMP_ACTUAL}"
assert "${TMP_EXPECT}" "${TMP_ACTUAL}"