#! /bin/bash
resp=$(curl http://app:5000/ -Is | grep -c "HTTP/1.1 200")
while [[ resp -ne 1 ]]
do
    if [[ resp -eq 1 ]]; then
		echo "pass logginpage from / with GET"
	fi
    sleep 2
	resp=$(curl http://app:5000/ -Is | grep -c "HTTP/1.1 200")
done
##test
resp=$(curl -X PUT http://localhost:5000/ -Is | grep -c "HTTP/1.1 200")
if [[ resp -eq 1 ]]; then
	echo "pass logginpage from / with POST"
fi
##test

resp=$(curl -X POST http://localhost:5000/ -Is | grep -c "HTTP/1.1 200")
if [[ resp -eq 1 ]]; then
	echo "pass logginpage from / with POST"
fi
#given the localhost url the loging is desplayd, the first page is the login page without entering to the system there is no way to get to the homepage
resp=$(curl -X POST http://localhost:5000/index -Is | grep -c "HTTP/1.1 200")
if [[ resp -eq 1 ]]; then	
	echo "pass logginpage from /index with POST"
fi

resp=$(curl http://localhost:5000/index -Is | grep -c "HTTP/1.1 200")
if [[ resp -eq 1 ]]; then	
	echo "pass logginpage from /index with GET"
fi

resp=$(curl -X POST http://localhost:5000/login -Is | grep -c "HTTP/1.1 200")
if [[ resp -eq 1 ]]; then
	echo "pass logginpage from /login with POST"
fi

resp=$(curl http://localhost:5000/login -Is | grep -c "HTTP/1.1 200")
if [[ resp -eq 1 ]]; then
	echo "pass logginpage from /login"
fi

resp=$(curl -X POST http://localhost:5000/api/login/firstname-lastname-username-password -Is | grep -c "HTTP/1.1 302")
if [[ resp -eq 1 ]]; then
	echo "pass logginpage from /api/login with POST"
fi

resp=$(curl http://localhost:5000/index/liz -Is | grep -c "HTTP/1.1 200")
if [[ resp -eq 1 ]]; then
	echo "pass welcome page"
fi

resp=$(curl -X POST http://localhost:5000/posts -Is | grep -c "HTTP/1.1 200")
if [[ resp -eq 1 ]]; then
	echo "pass create new page with POST"
fi

resp=$(curl http://localhost:5000/posts -Is | grep -c "HTTP/1.1 200")
if [[ resp -eq 1 ]]; then
	echo "pass create new page"
fi

resp=$(curl -X POST http://localhost:5000/api/posts/liztest -Is | grep -c "HTTP/1.1 200")
if [[ resp -eq 1 ]]; then
	echo "pass api added new post with POST"
fi

resp=$(curl http://localhost:5000/api/posts/liztest -Is | grep -c "HTTP/1.1 200")
if [[ resp -eq 1 ]]; then
	echo "pass api added new post"
fi

resp=$(curl http://localhost:5000/delete_edit -Is | grep -c "HTTP/1.1 200")
if [[ resp -eq 1 ]]; then
	echo "pass delete_edit new page"
fi

resp=$(curl -X POST http://localhost:5000/delete_edit -Is | grep -c "HTTP/1.1 200")
if [[ resp -eq 1 ]]; then
	echo "pass delete_edit new page with POST"
fi

resp=$(curl -X DELETE http://localhost:5000/api/delete/name -Is | grep -c "HTTP/1.1 302")
if [[ resp -eq 1 ]]; then
	echo "pass api delete name with DELETE"
fi

resp=$(curl http://localhost:5000/delete/name -Is | grep -c "HTTP/1.1 302")
if [[ resp -eq 1 ]]; then
	echo "pass delete name with GET"
fi

resp=$(curl -X PUT http://localhost:5000/api/update/name/name2 -Is | grep -c "HTTP/1.1 302")
if [[ resp -eq 1 ]]; then
	echo "pass api update name to name2 with PUT"
fi


resp=$(curl http://localhost:5000/update/name/name2 -Is | grep -c "HTTP/1.1 302")
if [[ resp -eq 1 ]]; then
	echo "pass update name to name2 with GET"
fi