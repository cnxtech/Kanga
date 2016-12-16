import psycopg2

def main():
	ip_address = raw_input("Please enter ip address: ")
	print "you entered: ", ip_address
	init_root = '/cepdev/bin/init/'
	files = dict()
	files['kafka'] = {'consumer.properties', 'producer.properties', 'server.properties'}
	files['zookeeper'] = {'zookeeper.properties'}
	files['elasticsearch'] = {'elasticsearch.yml'}
	files['storm'] = {'storm.yaml'}
	files['hostname'] = {'hostname'}
	files['hosts'] = {'hosts'}
	roots = dict()
	roots['kafka'] = '/cepdev/kafka_2.10-0.8.2.2/config/'
	roots['zookeeper'] = '/cepdev/kafka_2.10-0.8.2.2/config/'
	roots['elasticsearch'] = '/cepdev/elasticsearch-1.7.1/config/'
	roots['storm'] = '/cepdev/apache-storm-0.9.5/conf/'
	roots['hostname'] = '/etc/'
	roots['hosts'] = '/etc/'
	services = dict()
	services['elasticsearch'] = 'ElasticSearch service'
	services['zookeeper'] = 'Zookeeper service'
	services['kafka'] = 'Kafka service'
	services['storm'] = 'Storm service'
	init_properties(ip_address,init_root,files,roots)
	update_db(ip_address)
	insert_properties_to_db(ip_address,files,roots,services)


def init_properties(ip_address,init_root,files,roots):
	pattern = '#my_ip#'
	for service,file_names in files.iteritems():
		for file_name in file_names:
			template = init_root+file_name
			destination = roots[service]+file_name
			with open(template) as infile, open(destination, 'w') as outfile:
				for line in infile:
					line = line.replace(pattern, ip_address)
					outfile.write(line)

	
def update_db(ip_address):
	conn = None
	cur = None
	try:
		conn = psycopg2.connect("dbname='kanga' user='kanga' port='54322' host='localhost' password='kanga123!' ")
		cur = conn.cursor()
		cur.execute("delete from system_service")
		cur.execute("delete from system_node")
		sql = "insert into system_node values('"+ip_address+"','kanga-VirtualBox','Kanga Standalone Dev')"
		cur.execute(sql)
		sql = list()
		sql.append("insert into system_service values ('ElasticSearch monitoring','9200','ELASTICSEARCH','GOOD','MONITORING',now(),now(),'"+ip_address+"')     ")
		sql.append("insert into system_service values ('ElasticSearch search head','9200','ELASTICSEARCH','GOOD','SERVICE',now(),now(),'"+ip_address+"')       ")
		sql.append("insert into system_service values ('ElasticSearch search nodes','9200','ELASTICSEARCH','GOOD','SERVICE',now(),now(),'"+ip_address+"')      ")
		sql.append("insert into system_service values ('ElasticSearch service','9200','ELASTICSEARCH','GOOD','SERVICE',now(),now(),'"+ip_address+"')      ")
		sql.append("insert into system_service values ('Kafka monitoring','9999','KAFKA','GOOD','MONITORING',now(),now(),'"+ip_address+"')                     ")
		sql.append("insert into system_service values ('Kafka service','9192','KAFKA','GOOD','SERVICE',now(),now(),'"+ip_address+"')                           ")
		sql.append("insert into system_service values ('OS metrics','0','OS','GOOD','MONITORING',now(),now(),'"+ip_address+"')                                 ")
		sql.append("insert into system_service values ('Storm monitoring','8080','STORM','GOOD','MONITORING',now(),now(),'"+ip_address+"')                     ")
		sql.append("insert into system_service values ('Storm nimbus','6627','STORM','GOOD','SERVICE',now(),now(),'"+ip_address+"')                            ")
		sql.append("insert into system_service values ('Storm service','6627','STORM','GOOD','SERVICE',now(),now(),'"+ip_address+"')                           ")
		sql.append("insert into system_service values ('Storm ui','8080','STORM','GOOD','SERVICE',now(),now(),'"+ip_address+"')                                ")
		sql.append("insert into system_service values ('Zookeeper monitoring','2181','ZOOKEEPER','GOOD','MONITORING',now(),now(),'"+ip_address+"')            ")
		sql.append("insert into system_service values ('Zookeeper service','2181','ZOOKEEPER','GOOD','SERVICE',now(),now(),'"+ip_address+"')                  ")
		for s in sql:
			cur.execute(s)
		conn.commit()
	except:
		print "There is an error in sql execution during update_db"
	finally:
		cur.close()
		conn.close()
	return True
		

def insert_properties_to_db(ip_address,files,roots,services):
	conn = None
	cur = None
	try:
		conn = psycopg2.connect("dbname='kanga' user='kanga' port='54322' host='localhost' password='kanga123!' ")
		cur = conn.cursor()
		cur.execute("delete from system_config")
		conn.commit()
		for service,service_id in services.iteritems():
			for file_name in files[service]:
				content = ''
				full_path = roots[service]+file_name
				with file(full_path) as f:
					content = f.read()
					service_id = services[service]
					cur.execute("insert into system_config(filename,service_id,content) values(%s,%s,%s)", (file_name, service_id, content))
		conn.commit()
	except Exception as e:
		print "There is an error in sql execution during insert_properties_to_db"
		print str(e)
	finally:
		cur.close()
		conn.close()
	return True




if __name__ == "__main__":
	main()


