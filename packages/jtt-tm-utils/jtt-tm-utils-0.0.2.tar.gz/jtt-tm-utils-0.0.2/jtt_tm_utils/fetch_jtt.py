import ujson
import aiohttp
from aiohttp import web
from concurrent.futures._base import TimeoutError as Co_TimeoutError
import logging
from .sync_basedata import data_manager
from .consul_handle import consul_reader
from .redis_manager import redis_manager
from .timeutil import linux_timestamp
import asyncio
from asyncio.tasks import FIRST_COMPLETED
from .log import logger

SYNC_DATA_CONFIG =[('vehicle','carid,dvrid1,fleetid,vtid'),
               'accredituser']


class JttEmsg:
    # 4000 开始是jtt terminate 发回的错误
    E4001 = '失败'
    E4002 = '消息有误'
    E4003 = '不支持的命令'

    # 4200 开始是gateway 发回的错误
    # 1：车机不在线；
    # 2：等待超时；
    # 3：参数错误；
    # 4：不支持的命令
    E4201 = '车机不在线'
    E4202 = '等待超时'
    E4203 = '参数错误'
    E4204 = '不支持的命令'
    E4205 ='gateway回应格式错误'

    #4300开始是规则检查
    E4401 ='找不到车机'
    E4402 ='找不到gateway'
    E4403 = '没有终端注册到车'
    E4404 = '服务回应超时'
    E4405 ='gateway不明错误'
    E4406 ='gateway服务未注册'
    E4407 ='其它'
    E4408 ='不明错误，请联系管理员'


    @classmethod
    def msg(cls,code):
        return getattr(cls,'E%d' % code)



def gen_jtt_command(cmd_name,sim,cmd_body={}):
    def get_header(sim):
        return {
            "sim": sim
        }

    body = {'header':get_header(sim)}
    body.update(cmd_body)
    return {cmd_name:body}

def error_response(errcode,errmsg):
    return web.json_response({'errcode':errcode,'errmsg':errmsg},status = 400)

def up_ack_response(carid,up_ack):
    if up_ack['ack_result']==0:
        return normal_ack(carid)
    else:
        ecode = 4000+up_ack['ack_result']
        return error_response(ecode, JttEmsg.msg(ecode))

def gateway_error_response():
    ecode =4205
    return error_response(ecode,JttEmsg.msg(ecode))

def gateway_ack_response(carid,gateway_ack):
    if gateway_ack['ret_code']==0:
        return normal_ack(carid)
    else:
        ecode = 4200+gateway_ack['ret_code']
        return error_response(ecode, JttEmsg.msg(ecode))

def normal_ack(carid):
    return web.json_response(data={'terminate':carid})

def handle_sync_response(carid,data,cmd_name=''):
    try:
        key,body = data.popitem()
    except:
        return gateway_error_response()

    if key=='up_ack':
        return up_ack_response(carid,body)
    elif key =='gateway_ack':
        return gateway_ack_response(carid,body)
    elif key ==cmd_name:
        body.pop('header')
        return web.json_response(body)
    else:
        raise FetchJttError('not support response:%s' % cmd_name)


timeout = aiohttp.ClientTimeout(total=30)

class FetchJttError(Exception):
    def __init__(self,code,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.code = code

# class FetchJttTimeoutError(FetchJttError):
#     pass
def fail(ecode):
    raise FetchJttError(ecode)

def gateway_address(gateway):
    try:
        srv =consul_reader.read_service('jtt_gateway',gateway,True)
        return '%s:%s' % (srv.ip,srv.port)
    except Exception as e:
        return ''

async def get_connect_gateways(sim):
    rds = redis_manager.cache_r
    gateways =await rds.zrangebyscore('cache:sim:%s:connections' % sim ,linux_timestamp() - 3*60,linux_timestamp())
    return [gateway.decode() for gateway in gateways]


async def cansend_terminate(carid):
    v = await data_manager.get_vehicle(carid)
    if v is None:
        fail(4401)
    else:
        sim = v.get('dvrid1', '')
        # gateway = v.get('jtt_gateway','')
        if sim =='':
            fail(4403)
        gateways =await get_connect_gateways(sim)
        if len(gateways)<=0:
            fail(4402)

        server_address =[gateway_address(gateway) for gateway in gateways]
        server_address =[address for address in server_address if address!='']
        if len(server_address)<=0:
            fail(4406)

        return sim,server_address

async def post_jtt_each(url,data,loop):
    async with aiohttp.ClientSession(json_serialize=ujson.dumps,loop=loop,timeout=timeout) as session:
        try:
            async with session.post( url, timeout=timeout,data= ujson.dumps(data)) as r:
                if r.status == 200:
                    re = await r.json()
                    return re
                else:
                    # return await r.json()
                    logger.error('fetch error:%s,status:%s' % (url, r.status))
                    raise FetchJttError(4405)
        except Co_TimeoutError :
            logger.error('fetch timeout:%s' % url)
            raise FetchJttError( 4404)
        except Exception as e:
            logger.error('fetch error:%s,%s' % (url,str(e)))
            raise FetchJttError(4408,str(e))

async def post_jtt(carid,cmd_name,cmd_body,loop=None):
    sim,server_address =await cansend_terminate(carid)
    urls =['http://%s/wm/v1/request' % address for address in server_address]
    data = gen_jtt_command(cmd_name,sim,cmd_body)
    tasks =set([loop.create_task(post_jtt_each(url,data,loop)) for url in urls])
    done, pending = await asyncio.wait(tasks, return_when=FIRST_COMPLETED)
    if len(done)<=0:
        fail(4404)
    task = done.pop()
    if task._result is not None:
        return task._result
    else:
        if task.exception is not None:
            if task.exception is FetchJttError:
                fail(FetchJttError(task.exception).code)
            else:
                logger.error('post jtt error:%s,%s,%s' % (carid,cmd_name,str(task.exception)))
                fail(4408)







