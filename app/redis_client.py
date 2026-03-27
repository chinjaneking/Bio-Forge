"""Redis连接管理（简化版 - 内存模式）"""
import json
import time
from typing import Optional, Any
from collections import deque


class RedisClient:
    """Redis客户端封装 - 内存模拟版"""
    
    def __init__(self):
        self._data = {}
        self._queues = {}
        self._expires = {}
    
    def get(self, key: str) -> Optional[Any]:
        """获取值"""
        # 检查过期
        if key in self._expires and time.time() > self._expires[key]:
            self.delete(key)
            return None
        
        if key in self._data:
            return self._data[key]
        return None
    
    def set(self, key: str, value: Any, expire: Optional[int] = None) -> bool:
        """设置值"""
        self._data[key] = value
        if expire:
            self._expires[key] = time.time() + expire
        return True
    
    def delete(self, key: str) -> bool:
        """删除键"""
        if key in self._data:
            del self._data[key]
        if key in self._expires:
            del self._expires[key]
        return True
    
    def exists(self, key: str) -> bool:
        """检查键是否存在"""
        return key in self._data
    
    def push_queue(self, queue_name: str, value: Any) -> bool:
        """推入队列"""
        if queue_name not in self._queues:
            self._queues[queue_name] = deque()
        self._queues[queue_name].appendleft(value)
        return True
    
    def pop_queue(self, queue_name: str, timeout: int = 0) -> Optional[Any]:
        """弹出队列"""
        start_time = time.time()
        while True:
            if queue_name in self._queues and len(self._queues[queue_name]) > 0:
                return self._queues[queue_name].pop()
            
            if timeout == 0 or (time.time() - start_time) > timeout:
                break
            
            time.sleep(0.1)
        
        return None
    
    def queue_len(self, queue_name: str) -> int:
        """获取队列长度"""
        if queue_name in self._queues:
            return len(self._queues[queue_name])
        return 0
    
    @property
    def client(self):
        """获取原始客户端"""
        return self


# 全局Redis实例
redis_client = RedisClient()
