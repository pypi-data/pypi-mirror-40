from .timeutil import linux_timestamp,timestamp_ms
import random
import json
from enum import Enum
from collections import namedtuple


TTL = 24 * 60*60 *3
class TaskState:
    pending=0
    sending =1
    waiting =2
    finished=3


# class TaskStyle:
#     queue=0
#     only=1
#     immediately =2

# class TaskType(Enum):
#     upgrade =''
#     params =''

RDS_JTT_TASKS ='jtt:tasks:%s:tasks:%s'      #[terminate,taskno]
RDS_JTT_TASKQUEUE ='jtt:tasks:%s:taskqueue' #[terminate]
RDS_JTT_TASKSEQS ='jtt:tasks:%s:taskseqs' #[terminate] zset score:ackseq ,field:task_no
RDS_JTT_WAITINGTASKS ='jtt:tasks:waitingtasks' # zset terminate.taskno score:linuxtimestamp

RDS_JTT_MESSAGES='jtt:tasks:%s:messages' #[terminate] jttmessage score:linuxtimestamp
RDS_USER_MESSAGES='jtt:user:%s:messages' #[username] type : list

class JTTMessage:
    def __init__(self,carid,name,create_time):
        self.carid =carid
        self.name =name
        self.create_time =create_time
        self.msg =''
        self.error =0
        self.errmsg =''

    def to_dict(self):
        return self.__dict__

    @classmethod
    def create_by_task(cls,task):
        return JTTMessage(task.terminate,task.name,task.create_time)

TASK_CMD_NAMEMAP={
    'upgrade':''

}
class TaskErrMsg:
    E1 ='fail'
    E2 ='cancel'
    E3 ='terminate not support'
    E4 ='task timeout'
    @classmethod
    def msg(cls,code):
        return getattr(cls,'E%d' % code)

def gen_taskno():
    return '%d_%d' % (timestamp_ms(),random.randint(1,100))

class ETaskError(Exception):
    pass

class ETaskAcceptError(ETaskError):
    pass

JTask_No=namedtuple('JTask_No','task_no create_time')

class JttTask:
    def __init__(self, terminate,task_name, content,user,taskno=None):
        # self.task_type = task_type
        self.terminate = terminate
        self.state = TaskState.pending
        self.content = content
        self.create_time = linux_timestamp()
        self.user =user
        self.name = task_name

        self.taskno =taskno if taskno else '%s_%s' % (self.name, gen_taskno())



    @property
    def cmd_name(self):
        return TASK_CMD_NAMEMAP.get(self.name) or self.name

    def to_dict(self):
        re = self.__dict__
        re['content']=json.dumps(self.content)

        return re

    @classmethod
    def load_dict(cls,data):
        task = JttTask(data['terminate'], data['name'],
                       json.loads(data['content']),data['user'],data['taskno'])
        # task.taskno =data['taskno']
        task.create_time = int(data['create_time'])
        task.state = int(data['state'])
        return task

class JttTaskManager:
    def __init__(self,rds):
        self.cache={}
        self.rds =rds


    def remove_task(self,terminate,task_no):
        try:
            self.cache.pop('%s.%s' %(terminate,task_no))
        except:
            pass

    def _task_key(self,terminate,task_no):
        return '%s.%s' %(terminate,task_no)

    def add_task(self,task):
        key = self._task_key(task.terminate,task.taskno)
        self.cache[key] = task

    async def _change_task_state(self,terminate,task_no,state):
        task = await self.load_task(terminate, task_no, False)
        if task is not None:
            task.state = state

    async def load_task(self,terminate,task_no,from_redis=True):
        key = self._task_key(terminate,task_no)
        task =self.cache.get(key)
        if task is None and from_redis:
            data =await self.rds.hgetall(RDS_JTT_TASKS % (terminate,task_no))
            if data or {} !={}:
                data ={k.decode():v.decode()for k,v in data.items()}
                task =JttTask.load_dict(data)
                self.add_task(task)
        return task

    async def same_task(self,terminate,task_name):
        #是否存在相同的task
        score =await self.rds.zscore(RDS_JTT_TASKQUEUE % terminate,task_name)
        return score is not None

    async def write_task(self,task):
        tr = self.rds.multi_exec()

        tr.hmset_dict(RDS_JTT_TASKS % (task.terminate, task.taskno),task.to_dict())
        tr.expire(RDS_JTT_TASKS % (task.terminate, task.taskno),TTL)
        if task.state  ==TaskState.pending:
            tr.zadd(RDS_JTT_TASKQUEUE % task.terminate,linux_timestamp(),task.taskno)
            tr.expire(RDS_JTT_TASKQUEUE % task.terminate,TTL)
            # tr.sadd(RDS_JTT_TASK_TERMINTES,task.terminate)

        await tr.execute()


    async def create_task(self,terminate,task_name,content,user='',task_no=None):
        task = JttTask(terminate , task_name, content,user,task_no)
        task.state =TaskState.pending
        self.add_task(task)
        await self.write_task(task)

        return task

    async def close_task(self,terminate,task_no,errcode=0,errmsg='',extra=''):
        task =await self.load_task(terminate,task_no)
        if task:
            jtt_message = JTTMessage.create_by_task(task)
            jtt_message.error =errcode
            jtt_message.errmsg = errmsg
            jtt_message.msg = extra
            tr = self.rds.multi_exec()
            tr.zadd(RDS_JTT_MESSAGES % task.terminate ,linux_timestamp(),json.dumps( jtt_message.to_dict()))
            tr.expire(RDS_JTT_MESSAGES % task.terminate ,TTL)
            tr.rpush(RDS_USER_MESSAGES % task.user ,json.dumps( jtt_message.to_dict()))
            tr.expire(RDS_USER_MESSAGES % task.user, TTL)
            await tr.execute()

        tr = self.rds.multi_exec()
        tr.delete(RDS_JTT_TASKS % (terminate, task_no))
        tr.zrem(RDS_JTT_TASKQUEUE % terminate,task_no)
        tr.zrem(RDS_JTT_TASKSEQS % terminate,task_no)
        await tr.execute()

        self.remove_task(terminate,task_no)
        # todo: write to database


    async def waitting_task(self,terminate,task_no,ack_seq,add_waiting_list=False):
        tr = self.rds.multi_exec()
        tr.hmset_dict(RDS_JTT_TASKS % (terminate, task_no), {'state': TaskState.waiting})
        # 有后续操作,记录ack_seq
        tr.zadd(RDS_JTT_TASKSEQS % terminate, ack_seq, task_no)
        tr.expire(RDS_JTT_TASKSEQS % terminate,TTL)
        # timeout自动关闭任务
        if add_waiting_list:
            tr.zadd(RDS_JTT_WAITINGTASKS, linux_timestamp(),'%s.%s' %(terminate,task_no))

        await tr.execute()
        await self._change_task_state(terminate,task_no,TaskState.waiting)

    async def ack_task_fail(self,terminate,task_no):
        await self.rds.hmset_dict(RDS_JTT_TASKS % (terminate, task_no), {'state': TaskState.pending})
        await self._change_task_state(terminate, task_no, TaskState.pending)

    async def sending_task(self,terminate,task_no):
        tr = self.rds.multi_exec()
        tr.hmset_dict(RDS_JTT_TASKS % (terminate, task_no), {'state': TaskState.sending})
        tr.hincrby(RDS_JTT_TASKS % (terminate, task_no),'send_times')
        await tr.execute()

        await self._change_task_state(terminate, task_no, TaskState.sending)


    async def taskno_by_ackseq(self,terminate,ack_seq):
        data =await self.rds.zrangebyscore(RDS_JTT_TASKSEQS % terminate,ack_seq,ack_seq)
        if data:
            return data[0].decode()

    async def pop_taskno(self,terminate):
        data =await self.rds.zrange(RDS_JTT_TASKQUEUE % terminate, 0, 0, withscores=True)
        if data is not None and len(data)>0:
            [name,score]= data[0]
            return JTask_No(name.decode(),score)

    async def task_terminates(self):
        data =await self.rds.keys(RDS_JTT_TASKQUEUE % '*')
        if data is not None:
            return [item.decode().split(':')[-2] for item in data]
        else:
            return []

    async def get_waitting_tasks(self,starttime,endtime):
        data =await self.rds.zrangebyscore( RDS_JTT_WAITINGTASKS,starttime,endtime)
        if data:
            return [item.decode() for item in data]
        else:
            return []
