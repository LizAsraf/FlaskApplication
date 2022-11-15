#! /bin/bash
resp=$(curl -X POST http://app:5000/api/login/firstname-lastname-username-password -Is | grep -c "HTTP/1.1 302")
if [[ resp -eq 1 ]]; then
	echo "pass logginpage from /api/login with POST"
else
	exit 1
fi

resp=$(curl http://app:5000/index/liz -Is | grep -c "HTTP/1.1 200")
if [[ resp -eq 1 ]]; then
	echo "pass welcome page"
else
	exit 1
fi

resp=$(curl -X POST http://app:5000/posts -Is | grep -c "HTTP/1.1 200")
if [[ resp -eq 1 ]]; then
	echo "pass create new page with POST"
else
	exit 1
fi

resp=$(curl http://app:5000/posts -Is | grep -c "HTTP/1.1 200")
if [[ resp -eq 1 ]]; then
	echo "pass create new page"
else
	exit 1
fi

resp=$(curl -X POST http://app:5000/api/posts/liztest -Is | grep -c "HTTP/1.1 200")
if [[ resp -eq 1 ]]; then
	echo "pass api added new post with POST"
else
	exit 1
fi

resp=$(curl http://app:5000/api/posts/liztest -Is | grep -c "HTTP/1.1 200")
if [[ resp -eq 1 ]]; then
	echo "pass api added new post"
else
	exit 1
fi

resp=$(curl http://app:5000/delete_edit -Is | grep -c "HTTP/1.1 200")
if [[ resp -eq 1 ]]; then
	echo "pass delete_edit new page"
else
	exit 1
fi

resp=$(curl -X POST http://app:5000/delete_edit -Is | grep -c "HTTP/1.1 200")
if [[ resp -eq 1 ]]; then
	echo "pass delete_edit new page with POST"
else
	exit 1
fi

resp=$(curl -X DELETE http://app:5000/api/delete/name -Is | grep -c "HTTP/1.1 302")
if [[ resp -eq 1 ]]; then
	echo "pass api delete name with DELETE"
else
	exit 1
fi

resp=$(curl http://app:5000/delete/name -Is | grep -c "HTTP/1.1 302")
if [[ resp -eq 1 ]]; then
	echo "pass delete name with GET"
else
	exit 1
fi

resp=$(curl -X PUT http://app:5000/api/update/name/name2 -Is | grep -c "HTTP/1.1 302")
if [[ resp -eq 1 ]]; then
	echo "pass api update name to name2 with PUT"
else
	exit 1
fi


resp=$(curl http://app:5000/update/name/name2 -Is | grep -c "HTTP/1.1 302")
if [[ resp -eq 1 ]]; then
	echo "pass update name to name2 with GET"
else
	exit 1
fi