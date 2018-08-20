from redis.connection import BlockingConnectionPool
from redis import Redis
import random


class SSDBHandler():
    """
    SSDB Handler

    make it easy to get key-value from ssdb or redis

    """

    def __init__(self, tb_name, host, port):

        self.name = tb_name
        self.__conn = Redis(
            connection_pool=BlockingConnectionPool(host=host, port=port))

    def get(self, key):
        """
        get an item
        """
        data = self.__conn.hget(name=self.name, key=key)
        if data:
            return data.decode() if isinstance(data, bytes) else data
        else:
            return None

    def put(self, task_pid, task_path):
        """
        put a k-v pair into db
        """
        data = self.__conn.hset(self.name, task_pid, task_path)
        return data

    def delete(self, key):
        """
        remove a k-v pair with key
        """
        self.__conn.hdel(self.name, key)

    def update(self, key, value):
        """
        update a k-v pair 
        """
        self.__conn.hincrby(self.name, key, value)

    def getAllKeys(self):
        """
        get all keys in table
        """
        task_pids = self.__conn.hkeys(self.name)
        return [task_pid.decode() if isinstance(task_pid, bytes) else task_pid for task_pid in task_pids] if task_pids else None

    def getAll(self):
        """
        get all k-v pairs in table
        """
        item_dict = self.__conn.hgetall(self.name)
        return {key.decode() if isinstance(key, bytes) else key: value.decode() if isinstance(value, bytes) else value for key, value in item_dict.items()}

    def pop(self):
        """
        random pick a k-v pair
        """
        task_pids = self.__conn.hkeys(self.name)
        if task_pids:
            task_pid = random.choice(task_pids)
            task_path = self.__conn.hget(self.name, task_pid)
            self.delete(task_pid)
            return {'key': task_pid.decode() if isinstance(task_pid, bytes) else task_pid,
                    'value': task_path.decode() if isinstance(task_path, bytes) else task_path}
        return None

    def exists(self, key):
        """
        check wheather the key is exists in table 
        """
        return self.__conn.hexists(self.name, key)

    def getNumber(self):
        """
        get the length of table
        """
        return self.__conn.hlen(self.name)

    def changeTable(self, name):
        """
        switch to another table
        """
        self.name = name


if __name__ == '__main__':

    import json
    c = SSDBHandler('base_machine', '192.168.50.172', 8888)
    if not c.exists("palm"):

        c.put("palm", json.dumps({"run": "palm_run", "running": "palm_running",
                                  "success": "palm_success", "fail": "palm_fail"}))
    else:
        print("exists")
    print(c.get("palm"))
    print(json.loads(c.get("palm"))["run"])
    c.changeTable("palm_run")
    print(c.getAll())
