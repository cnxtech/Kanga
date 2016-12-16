import zc.zk

zk = None
try:
    host = '10.251.22.99:2181'
    zk = zc.zk.ZooKeeper(host)
    print zk
    zk.delete_recursive('brokers/topics/test')
    zk.close()
except Exception as e:
    zk.close()


