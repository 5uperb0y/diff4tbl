#!/bin/bash
function setup(){
	TMP_ACTUAL=$(mktemp)
	TMP_EXPECT=$(mktemp)
	TMP_FILE1=$(mktemp)
	TMP_FILE2=$(mktemp)
	trap cleanup EXIT TERM INT
}
function cleanup() {
	rm "${TMP_FILE1}" "${TMP_FILE2}" "${TMP_EXPECT}" "${TMP_ACTUAL}"
}
function assert() {
	expect=$1
	actual=$2
	if diff "${expect}" "${actual}" > /dev/null 2>&1; then
		exit 0
	else
		diff -y "${expect}" "${actual}"
		exit 1
	fi
}