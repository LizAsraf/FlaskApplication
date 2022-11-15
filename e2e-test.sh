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

resp=$(curl -X POST http://app:5000/ -Is | grep -c "HTTP/1.1 200")
if [[ resp -eq 1 ]]; then
	echo "pass logginpage from / with POST"
else
	exit 1
fi
resp=$(curl -X POST http://app:5000/index -Is | grep -c "HTTP/1.1 200")
if [[ resp -eq 1 ]]; then	
	echo "pass logginpage from /index with POST"
else
	exit 1
fi

resp=$(curl http://app:5000/index -Is | grep -c "HTTP/1.1 200")
if [[ resp -eq 1 ]]; then	
	echo "pass logginpage from /index with GET"
else
	exit 1
fi

resp=$(curl -X POST http://app:5000/login -Is | grep -c "HTTP/1.1 200")
if [[ resp -eq 1 ]]; then
	echo "pass logginpage from /login with POST"
else
	exit 1
fi

resp=$(curl http://app:5000/login -Is | grep -c "HTTP/1.1 200")
if [[ resp -eq 1 ]]; then
	echo "pass logginpage from /login"
else
	exit 1
fi