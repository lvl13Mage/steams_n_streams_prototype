mysql: 
	docker run -it -p 3307:3306 --name bg-sql --env MYSQL_USER=bg --env MYSQL_PASSWORD=bg --env MYSQL_ROOT_PASSWORD=root --env MYSQL_DATABASE=bg --rm -v /var/lib/mysql -d mysql