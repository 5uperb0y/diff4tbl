#!/bin/bash
function run_test(){
	test=$1
	TMP_TEST_LOG=$(mktemp)
	if "${test}" > "${TMP_TEST_LOG}" 2>&1 ; then
		echo "$(basename ${test}): passed"
		return 0
	else
		echo "$(basename ${test}): failed"	
		cat "${TMP_TEST_LOG}"
		return 1
	fi
	rm "${TMP_TEST_LOG}"
}
test_to_run=$(find . -name "test_*.sh")
total_test_number=$(echo "${test_to_run}" | wc -w)
passed=0
echo -e "collected ${total_test_number} items\n"
for test in ${test_to_run}; do
	run_test "${test}" && ((passed ++))
done
echo -e "\n${passed} passed"