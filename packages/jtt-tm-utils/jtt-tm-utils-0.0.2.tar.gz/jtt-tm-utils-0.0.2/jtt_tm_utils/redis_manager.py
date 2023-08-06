from .consul_handle import consul_reader
import aioredis
import asyncio
TAG_MAPPING={
    'cache':'cache',
    'cache_r':'cache'
}
class RedisManager:
    def __init__(self):
        self._cache ={}

    async def aload_configs(self,rds_names):
        rds_urls ={}
        for rds_name in rds_names:
            (name,as_slave )= rds_name if type(rds_name)==tuple else (rds_name,False)
            rds_urls[name]=self.load_redis_url(name,as_slave)

        tasks =(aioredis.create_redis_pool(url) for url in rds_urls.values())
        redises =await asyncio.gather(*tasks)
        for name,rds in zip(rds_urls.keys(),redises):
            self._cache[name]=rds
            self.make_property(name)
            
    def get_redis(self,name):
        assert name in self._cache.keys(),'redis manager %s not setting' % name
        return self._cache.get(name)

    def make_property(self,name):
        def make_func():
            def _method(self):
                return self.get_redis(name)
            return _method
        setattr(self.__class__,name,property(make_func()))

    async def clear_cahce(self):
        pass

    def load_redis_url(self,name,as_slave):
        tag = TAG_MAPPING.get(name,name)
        return consul_reader.redis_as_url(tag,as_slave = as_slave)

redis_manager = RedisManager()


