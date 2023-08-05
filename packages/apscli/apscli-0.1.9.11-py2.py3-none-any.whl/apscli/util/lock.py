# encoding=utf-8
import functools
import fcntl
import os
import json
import time
from glob import glob
from datetime import datetime
from dateutil import tz

from constant import cf

UTC_TZ = tz.tzutc()

def lock_method(lock_filename):
    ''' Use an OS lock such that a method can only be called once at a time. '''

    def decorator(func):

        @functools.wraps(func)
        def lock_and_run_method(*args, **kwargs):

            # Only run this program if it's not already running
            # Snippet based on
            # http://linux.byexamples.com/archives/494/how-can-i-avoid-running-a-python-script-multiple-times-implement-file-locking/

            fp = open(lock_filename, 'w')
            try:
                fcntl.flock(fp, fcntl.LOCK_EX | fcntl.LOCK_NB)
            except IOError:
                raise SystemExit(
                    "This program is already running.  Please stop the current process or " +
                    "remove " + lock_filename + " to run this script."
                )

            ret = None
            try:
                ret = func(*args, **kwargs)
            finally:
                fcntl.flock(fp, fcntl.LOCK_UN)
                fp.close()

            return ret

        return lock_and_run_method

    return decorator 


'''
def lock_method(lock_filename):
    # Use an OS lock such that a method can only be called once at a time.

    def decorator(func):
    
        @functools.wraps(func)
        def lock_and_run_method(*args, **kwargs):

            # Only run this program if it's not already running
            # Snippet based on http://linux.byexamples.com/archives/494/how-can-i-avoid-running-a-python-script-multiple-times-implement-file-locking/
            fd = None
            try:
                fd = os.open(lock_filename, os.O_CREAT | os.O_RDWR)
                fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
                return func(*args, **kwargs)
            except IOError:
                raise SystemExit(
                    "This program is already running.  Please stop the current process or " +
                    "remove " + lock_filename + " to run this script."
                )
            finally:
                if fd is not None:
                    fcntl.flock(fd, fcntl.LOCK_UN)

        return lock_and_run_method

    return decorator 
'''

# lockfile -sleeptime     | -r retries |
#          -l locktimeout | -s suspend | -!  | -ml | -mu | filename ...
# 尝试创建一系列的lock文件，如果存在创建失败，则sleep一段时间(默认8秒)，然后(从失败处)重试。
# 可以指定重试的次数(-r),直到最后失败，如果-r -1，则会一直retry下去
# 如果（重试过程中）timeout，导致创建所有文件失败，则return failure并删除已创建的所有锁文件
# lockfile创建的所有文件都是只读的，只能使用rm -f来删除
# -l locktimeout: 如果指定了该选项，那么创建的锁文件会被强制删除，在locktimeout秒以后。（防止创建锁文件的程序意外退出,而没有rm -f锁文件)
# -s suspend: default 16s, 在锁文件 rm -f之后会挂起16秒，以免别的程序新创建了锁文件而不小心立即进行了删除
# -ml / -mu: 如果拥有合适的权限,使用这两个选项来 lock / unlock your system mailbox
# Signal received, ...   Lockfile will remove anything it created till now and terminate.


def lock_method_nfs(lock_filename, retry=1, interval=1, suspend=16, locktimeout=60*60):
    ''' Use an local_or_NFS_lock such that a method can only be called once at a time. '''

    def decorator(func):
    
        @functools.wraps(func)
        def lock_and_run_method(*args, **kwargs):
            try:
                # 不重试,获取不到锁则立即失败
                # 如果程序意外退出而没有执行最后的rm -f锁文件，通过下一次执行同样命令(利用locktimeout指定的参数,进行遗留文件的删除)
                cmd = 'lockfile -%s -r %s -l %s -s %s  %s' % (interval, retry, locktimeout, suspend, lock_filename)
                if os.system(cmd)==0:
                    ret = func(*args, **kwargs)
                    os.system('rm -f %s' % lock_filename)
                    return ret
                else:
                    raise SystemExit('exec [%s] fail' % cmd)
            finally:
                if os.path.isfile(lock_filename):
                    os.system('rm -f %s' % lock_filename)

        return lock_and_run_method

    return decorator 


class DummyLock(object):
    def __init__(self, path, retry, interval_in_seconds, job_id, mode, startpath='/nas'):
        raise NotImplementedError


class NFSLock(object):
    
    def __init__(self, path, mode, retry=0, interval_in_seconds=1, job_id='a', startpath=cf.get('Resource_Lock', 'absolute_prefix_path'), effective_in_seconds=cf.getint('Resource_Lock', 'max_effective_in_seconds')):
        if not os.path.exists(startpath):
            os.makedirs(startpath)

        path = path.strip().strip(os.sep)
        assert len(path)>0, 'lock_path should be like: pod1/db1/table1'   # ToDo: need regex_validate?

        mode = mode.upper()
        assert mode in ('S', 'X'), 'lock_mode should in (S, X)'

        chain = [[p,'S'] for p in path.split(os.sep)]
        chain[-1][1] = mode      # [['pod1', 'S'], ['db1', 'S'], ['table1', 'X']]
        
        self.raw_chain = chain

        self.chain = [
            [
                os.path.join(
                    startpath, os.sep.join([l[0] for l in chain][:i+1])
                ),
                chain[i][1]
            ] for i in range(len(chain))
        ]                           # [['/nas/pod1', 'S'], ['/nas/pod1/db1', 'S'], ['/nas/pod1/db1/table1', 'X']]
        assert type(effective_in_seconds) is int and 0<effective_in_seconds<=cf.get('Resource_Lock', 'max_effective_in_seconds'), 'resource_lock should be effective within at most 12 hours'
        self.path = path
        self.mode = mode
        self.retry = retry
        self.interval_in_seconds = interval_in_seconds
        self.startpath = startpath
        self.effective_in_seconds = effective_in_seconds
        
        self.job_id = job_id


    def to_dict(self):
        return {
            'path': self.path,
            'mode': self.mode,
            'retry': self.retry,
            'interval_in_seconds': self.interval_in_seconds,
            # 'startpath': self.startpath,
            'effective_in_seconds': self.effective_in_seconds,
            # 'resource_lock_flag_file': self.resource_lock_flag_file if hasattr(self, 'resource_lock_flag_file') else None
        }    
    def __str__(self):
        return json.dumps(self.to_dict(), indent=4)
    def __repr__(self):
        return self.__str__()


    @staticmethod
    def clean_ineffective_resource_lock_flag_files(startpath, top_level_resource_path):
        resource_lock_flag_files = [
            filename for filename in os.listdir(top_level_resource_path) if filename.startswith('APSCLI_LOCK_FLAG')
        ]
        ineffective_resource_lock_flag_files = [
            filename for filename in resource_lock_flag_files 
            if time.mktime(datetime.now(tz=UTC_TZ).timetuple()) > int(filename.split('#')[1]) + int(filename.split('#')[2]) 
        ]
        for filename in ineffective_resource_lock_flag_files:
            raw_chain = [s.split('=') for s in filename.split('#')[-1].split('.')]
            chain = [
                [
                    os.path.join(
                        startpath, os.sep.join([l[0] for l in raw_chain][:i+1])
                    ),
                    raw_chain[i][1]
                ] for i in range(len(raw_chain))
            ]
            for old_lock_file,new_lock_file in NFSLock.gen_lock_chain_transform(chain):
                os.rename(old_lock_file, new_lock_file)
            os.remove( os.path.join( chain[0][0], filename) )
        
    @staticmethod
    def gen_lock_chain_transform(chain):
        lock_chain_transform = []
        for full_path, lock_mode in reversed(chain):
            lock_file = glob(full_path + os.sep + 'S_*,X_*.lock')
            # lock_filenum = int(exec_shell_cmd('ls '+ full_path + os.sep + 'S_*,X_*.lock | wc -l')[1])
            assert len(lock_file)==1, 'should exist only one lock_file'
            lock_file = lock_file[0]    # exec_shell_cmd('ls '+ full_path + os.sep + 'S_*,X_*.lock')[1]
            
            exist_locks = dict([(x.split('_')[0],int(x.split('_')[1])) for x in lock_file[len(full_path)+1:][0:-5].split(',')])
            assert exist_locks[lock_mode]>0, 'current_lock: %s doesnt contain lock:%s at level: %s' % (lock_file,lock_mode, full_path)
            exist_locks[lock_mode] -= 1
            lock_chain_transform.append(
                (lock_file, full_path+os.sep+','.join([k+'_'+str(exist_locks[k]) for k in sorted(exist_locks)]) + '.lock')
            )
        return lock_chain_transform


    def put_lock_effective_flag(self):   # create my resource_lock_flag_file
        l = [p + '=' + lock_mode for p, lock_mode in self.raw_chain]
        utc_timestamp = time.mktime(datetime.now(tz=UTC_TZ).timetuple())
        self.resource_lock_flag_file = '#'.join([
            'APSCLI_LOCK_FLAG', 
            str(int(utc_timestamp)), 
            str(self.effective_in_seconds), 
            self.job_id, 
            '.'.join(l)
        ])
        open(os.path.join( self.chain[0][0], self.resource_lock_flag_file), 'a').close()


    def allocate(self):
        @lock_method_nfs(lock_filename=os.path.join(self.startpath, self.path.split(os.sep)[0]+'.lock'), retry=-1, interval=1, suspend=1, locktimeout=5)
        def try_allocate():
            print(time.ctime(), 'try_allocating_resource:%s' % self.path)
            abs_path = os.path.join(self.startpath, self.path)
            if not os.path.exists(abs_path):
                os.makedirs(abs_path)

            for full_path, lock_mode in self.chain:
                # lock_filenum = int(exec_shell_cmd('ls '+ full_path + os.sep + 'S_*,X_*.lock | wc -l')[1])
                # assert lock_filenum in (0,1), 'exist %d resource_lock_file under: %s' % (lock_filenum, full_path)
                lock_file = glob(full_path + os.sep + 'S_*,X_*.lock')
                assert len(lock_file) in (0,1), 'exist %d resource_lock_file under: %s' % (len(lock_file), full_path)
                if len(lock_file)==0:
                    open(os.path.join(full_path, 'S_0,X_0.lock'), 'a').close()

            NFSLock.clean_ineffective_resource_lock_flag_files(self.startpath, self.chain[0][0])
            
            can = True
            lock_chain_transform = []
            for full_path, lock_mode in self.chain:
                # lock_file = exec_shell_cmd('ls '+ full_path + os.sep + 'S_*,X_*.lock')[1]
                lock_file = glob(full_path + os.sep + 'S_*,X_*.lock')[0]

                exist_locks = dict([(x.split('_')[0],int(x.split('_')[1])) for x in lock_file[len(full_path)+1:][0:-5].split(',')])  # {'S': 0, 'X': 0}
                can, exist_locks = can_apply_lock(lock_mode, exist_locks)
                lock_chain_transform.append(
                    (lock_file, full_path+os.sep+','.join([k+'_'+str(exist_locks[k]) for k in sorted(exist_locks)]) + '.lock')
                )
                if not can:
                    return False
            
            self.put_lock_effective_flag()
            for old_lock_filename,new_lock_filename in lock_chain_transform:
                os.rename(old_lock_filename, new_lock_filename)
            print(time.ctime(), 'done_allocate_resource:%s' % self.path)
            return True

        return try_allocate()

    def free(self):    
        @lock_method_nfs(lock_filename=os.path.join(self.startpath, self.path.split(os.sep)[0]+'.lock'), retry=-1, interval=1, suspend=1, locktimeout=5)
        def _free():
            if hasattr(self, 'resource_lock_flag_file') and os.path.exists(
                os.path.join( self.chain[0][0], self.resource_lock_flag_file )
            ):    # my_resource_lock still effective/exists(not_freed_by_other_Apscli_because_of_exceed_lock_effective_time)

                print(time.ctime(), 'freeing_resource:%s' % self.path)
                abs_path = os.path.join(self.startpath, self.path)
                assert os.path.exists(abs_path), 'lock_path:%s doesnt exist when unlock' % abs_path
                
                for old_lock_file,new_lock_file in NFSLock.gen_lock_chain_transform(self.chain):
                    os.rename(old_lock_file, new_lock_file)
                os.remove( os.path.join( self.chain[0][0], self.resource_lock_flag_file) )
                print(time.ctime(), 'done_free_resource:%s' % self.path)

        _free()


    '''
    @lock_method_nfs(lock_filename=os.path.join(self.startpath, '/dc_cordinator.lock', retry=-1, interval=8, locktimeout=60*60)     # ToDo: /fsnadmin/<podname>.lock or /fsnadmin/<customer>.lock or /fsnadmin/<dc_short_name>.lock?
    def allocate(self):
        abs_path = os.path.join(self.startpath, self.path)
        if not os.path.exists(abs_path):
            os.makedirs(abs_path)

        for full_path, lock_mode in self.chain:
            lock_filenum = int(
                # os.popen('ls '+ full_path + os.sep + 'IS_*,IX_*,S_*,X_*.lock | wc -l').readline().strip()
                exec_shell_cmd('ls '+ full_path + os.sep + 'IS_*,IX_*,S_*,X_*.lock | wc -l')[1]
            )
            assert lock_filenum in (0,1), 'exist more than one resource_lock_file under: %s' % full_path
            if lock_filenum==0:
                open(os.path.join(full_path, 'IS_0,IX_0,S_0,X_0.lock'), 'a').close()

        can = True
        lock_chain_transform = []
        for full_path, lock_mode in self.chain:
            lock_file = exec_shell_cmd('ls '+ full_path + os.sep + 'IS_*,IX_*,S_*,X_*.lock')[1]   # os.popen('ls '+ full_path + os.sep + 'IS_*,IX_*,S_*,X_*.lock').readline().strip()

            exist_locks = dict([(x.split('_')[0],int(x.split('_')[1])) for x in lock_file[len(full_path)+1:][0:-5].split(',')])  # {'IX': 0, 'IS': 0, 'S': 0, 'X': 0}
            can, exist_locks = can_apply_lock(lock_mode, exist_locks)
            lock_chain_transform.append(
                (lock_file, full_path+os.sep+','.join([k+'_'+str(exist_locks[k]) for k in sorted(exist_locks)]) + '.lock')
            )
            if not can:
                return False

        for old_lock_filename,new_lock_filename in lock_chain_transform:
            os.rename(old_lock_filename, new_lock_filename)
        return True

    @lock_method_nfs(lock_filename='/fsnadmin/dc_cordinator.lock', retry=-1, interval=8, locktimeout=60*60)
    def free(self):
        abs_path = os.path.join(self.startpath, self.path)
        assert os.path.exists(abs_path), 'lock_path:%s doesnt exist when unlock' % abs_path
        
        lock_chain_transform = []
        for full_path, lock_mode in reversed(self.chain):
            lock_filenum = int(
                # os.popen('ls '+ full_path + os.sep + 'IS_*,IX_*,S_*,X_*.lock | wc -l').readline().strip()
                exec_shell_cmd('ls '+ full_path + os.sep + 'IS_*,IX_*,S_*,X_*.lock | wc -l')[1]
            )
            assert lock_filenum==1, 'should exist only one lock_file when unlock'
            
            lock_file = exec_shell_cmd('ls '+ full_path + os.sep + 'IS_*,IX_*,S_*,X_*.lock')[1] # os.popen('ls '+ full_path + os.sep + 'IS_*,IX_*,S_*,X_*.lock').readline().strip()
            exist_locks = dict([(x.split('_')[0],int(x.split('_')[1])) for x in lock_file[len(full_path)+1:][0:-5].split(',')])
            assert exist_locks[lock_mode]>0, 'current_lock: %s doesnt contain lock:%s at level: %s when unlock' % (lock_file,lock_mode, full_path)
            exist_locks[lock_mode] -= 1
            lock_chain_transform.append(
                (lock_file, full_path+os.sep+','.join([k+'_'+str(exist_locks[k]) for k in sorted(exist_locks)]) + '.lock')
            )

        for old_lock_file,new_lock_file in lock_chain_transform:
            os.rename(old_lock_file, new_lock_file)
    '''



'''
Mode | NL | IS | IX | S  | X
-----------------------------
NL   | Y  | Y  | Y  | Y  | Y   
IS   | Y  | Y  | Y  | Y  | -
IX   | Y  | Y  | Y  | -  | -
S    | Y  | Y  | -  | Y  | -
X    | Y  | -  | -  | -  | -

_lock_groups = {
    # ('NL','NL'):True, 
    # ('NL','IS'):True,
    # ('NL','IX'):True,
    # ('NL','S'): True,
    # ('NL','X'): True,
    ('IS','IS'):True, 
    ('IS','IX'):True,
    ('IS','S'): True,
    ('IS','X'): False,
    ('IX','IX'):True,
    ('IX','S'): False,
    ('IX','X'): False,
    ('S' ,'S'): True,
    ('S' ,'X'): False,
    ('X' ,'X'): False
}

def lock_compatible(lock_a, lock_b):
    assert lock_a in ('IS', 'IX', 'S', 'X') and lock_b in ('IS', 'IX', 'S', 'X'), 'illegal input_lock'
    return _lock_groups[(lock_a, lock_b)] if (lock_a, lock_b) in _lock_groups else _lock_groups[(lock_b, lock_a)]
'''

_lock_groups = {
    ('S' ,'S'): True,
    ('S' ,'X'): False,
    ('X' ,'X'): False
}

def lock_compatible(lock_a, lock_b):
    assert lock_a in ('S', 'X') and lock_b in ('S', 'X'), 'illegal input_lock'
    return _lock_groups[(lock_a, lock_b)] if (lock_a, lock_b) in _lock_groups else _lock_groups[(lock_b, lock_a)]

def can_apply_lock(lock, exist_locks):
    for l in exist_locks:
        if exist_locks[l]>0 and not lock_compatible(lock, l):
            return False, exist_locks

    exist_locks[lock]+=1
    return True, exist_locks

'''
class LockManager(object):
    def __init__(self):
        # 锁管理器
        # 1. 必须获取多个粒度/级别的锁，以便完全保护资源。这组具有多个粒度级别的锁称为锁层次结构。
        # 例如，为了完全保护索引的读取，锁管理器可能必须获取行上的共享锁(S)以及页和表上的意图共享锁(IS)
        # 2. 对一个Transaction授予锁(复数)，如果没有冲突的锁(复数)已被授予给/ 持有被别的Transaction.
        pass

class QueryProcessor(object):
    def __init__(self):
        # 查询处理器
        # 1.决定了在一个Transaction里，有哪些资源要被访问
        # 2.基于资源access类型/ transaction隔离级别，决定要申请何种类型的锁(复数)来保护transaction中要访问的每个资源
        # 3.从锁管理器请求适当的锁
        pass
        

意向锁的两个作用:
1. To prevent other transactions from modifying the higher-level resource in a way that would invalidate the lock at the lower level.
防止其他的事务，以一种让低级别锁失效的方式来修改较高级别的资源

2. To improve the efficiency of the SQL Server Database Engine in detecting lock conflicts at the higher level of granularity.
提高 数据库引擎在更高粒度级别上检测 锁冲突的效率

For example, a IS is requested at the table level before shared (S) locks are requested on pages or rows within that table. Setting an intent lock at the table level prevents another transaction from subsequently acquiring an exclusive (X) lock on the table containing that page. Intent locks improve performance because the SQL Server Database Engine examines intent locks only at the table level to determine if a transaction can safely acquire a lock on that table. This removes the requirement to examine every row or page lock on the table to determine if a transaction can lock the entire table.

IX is a superset of IS, and it also protects requesting shared locks on lower level resources.

Shared with intent exclusive (SIX)	Protects requested or acquired shared locks on all resources lower in the hierarchy and intent exclusive locks on some (but not all) of the lower level resources. Concurrent IS locks at the top-level resource are allowed. For example, acquiring a SIX lock on a table also acquires intent exclusive locks on the pages being modified and exclusive locks on the modified rows. There can be only one SIX lock per resource at one time, preventing updates to the resource made by other transactions, although other transactions can read resources lower in the hierarchy by obtaining IS locks at the table level.
SIX is acquired when all rows need to be read and at least some of them need to be modified.	
IS is compatible with everything but the exclusive locks. 
IX is compatible with other IX and IS locks. 
SIX is only compatible with IS locks.


Concurrent IS locks at the top-level resource are allowed.
For example, acquiring a SIX lock on a table also acquires intent exclusive locks on the pages being modified and exclusive locks on the modified rows.
There can be only one SIX lock per resource at one time, preventing updates to the resource made by other transactions, although other transactions can read resources lower in the hierarchy by obtaining IS locks at the table level.

Lock Compatibility
Lock compatibility controls whether multiple transactions can acquire locks on the same resource at the same time. If a resource is already locked by another transaction, a new lock request can be granted only if the mode of the requested lock is compatible with the mode of the existing lock. If the mode of the requested lock is not compatible with the existing lock, the transaction requesting the new lock waits for the existing lock to be released or for the lock timeout interval to expire. For example, no lock modes are compatible with exclusive locks. While an exclusive (X) lock is held, no other transaction can acquire a lock of any kind (shared, update, or exclusive) on that resource until the exclusive (X) lock is released. Alternatively, if a shared (S) lock has been applied to a resource, other transactions can also acquire a shared lock or an update (U) lock on that item even if the first transaction has not completed. However, other transactions cannot acquire an exclusive lock until the shared lock has been released.

Note
IX lock is compatible with an IX lock mode because IX means the intention is to update only some of the rows rather than all of them. 
Other transactions that attempt to read or update some of the rows are also permitted as long as they are not the same rows being updated by other transactions. 
Further, if two transactions attempt to update the same row, both transactions will be granted an IX lock at table and page level. However, one transaction will be granted an X lock at row level. The other transaction must wait until the row-level lock is removed.

Deadlocking is often confused with normal blocking. When a transaction requests a lock on a resource locked by another transaction, the requesting transaction waits until the lock is released. By default, SQL Server transactions do not time out, unless LOCK_TIMEOUT is set. The requesting transaction is blocked, not deadlocked, because the requesting transaction has not done anything to block the transaction owning the lock. Eventually, the owning transaction will complete and release the lock, and then the requesting transaction will be granted the lock and proceed.

When the lock monitor initiates deadlock search for a particular thread, it identifies the resource on which the thread is waiting. The lock monitor then finds the owner(s) for that particular resource and recursively continues the deadlock search for those threads until it finds a cycle. A cycle identified in this manner forms a deadlock.

After a deadlock is detected, the SQL Server Database Engine ends a deadlock by choosing one of the threads as a deadlock victim. The SQL Server Database Engine terminates the current batch being executed for the thread, rolls back the transaction of the deadlock victim, and returns a 1205 error to the application. Rolling back the transaction for the deadlock victim releases all locks held by the transaction. This allows the transactions of the other threads to become unblocked and continue. The 1205 deadlock victim error records information about the threads and resources involved in a deadlock in the error log.

By default, the SQL Server Database Engine chooses as the deadlock victim the session running the transaction that is least expensive to roll back. Alternatively, a user can specify the priority of sessions in a deadlock situation using the SET DEADLOCK_PRIORITY statement. DEADLOCK_PRIORITY can be set to LOW, NORMAL, or HIGH, or alternatively can be set to any integer value in the range (-10 to 10). The deadlock priority defaults to NORMAL. If two sessions have different deadlock priorities, the session with the lower priority is chosen as the deadlock victim. If both sessions have the same deadlock priority, the session with the transaction that is least expensive to roll back is chosen. If sessions involved in the deadlock cycle have the same deadlock priority and the same cost, a victim is chosen randomly.

When working with CLR, the deadlock monitor automatically detects deadlock for synchronization resources (monitors, reader/writer lock and thread join) accessed inside managed procedures. However, the deadlock is resolved by throwing an exception in the procedure that was selected to be the deadlock victim. It is important to understand that the exception does not automatically release resources currently owned by the victim; the resources must be explicitly released. Consistent with exception behavior, the exception used to identify a deadlock victim can be caught and dismissed.

'''

'''
IS lock (intent share)
The lock owner can read data in the table, partition, or table space, but not change it. Concurrent processes can both read and change the data. The lock owner might acquire a page or row lock on any data it reads.
IX lock (intent exclusive)
The lock owner and concurrent processes can read and change data in the table, partition, or table space. The lock owner might acquire a page or row lock on any data it reads; it must acquire one on any data it changes.
S lock (share)
The lock owner and any concurrent processes can read, but not change, data in the table, partition, or table space. The lock owner does not need page or row locks on data it reads.
U lock (update)
The lock owner can read, but not change, the locked data; however, the owner can promote the lock to an X lock and then can change the data. Processes concurrent with the U lock can acquire S locks and read the data, but no concurrent process can acquire a U lock. The lock owner does not need page or row locks.
U locks reduce the chance of deadlocks when the lock owner is reading data to determine whether to change it. U locks are acquired on a table space when the lock size is TABLESPACE and the statement is a SELECT with a FOR UPDATE clause. Similarly, U locks are acquired on a table when lock size is TABLE and the statement is a SELECT with a FOR UPDATE clause.

SIX lock (share with intent exclusive)
The lock owner can read and change data in the table, partition, or table space. Concurrent processes can read data in the table, partition, or table space, but not change it. Only when the lock owner changes data does it acquire page or row locks.

In some circumstances a session holds an S lock on the table or a page. If the session now (within the same transaction) requests an X lock on a row in that same table, it first has to take an IX lock on the table/page. However, a session can hold only one lock on any given resource. So to take the IX lock, it would have to release the S lock wich is probably not desired, so SQL Server offers a combination: SIX.

The reason why you have a page lock is due to SQL Server sometimes deciding that it would be better to lock the page instead of locking each row. That happens often if there are very many locks taken between al sessions already, but can have many other reasons too.

This occurs when the transaction has read the row or page with the intention of writing to it later. An SIX lock on a row or page must be converted to an X lock before the actual update may occur. No other transaction can read or modify a row or page that has been locked with an SIX lock.
An SIX lock is stronger than an S lock or an IX lock. When a transaction obtains an SIX lock on a table, only that transaction will be able to modify data in the table. In this respect, an SIX lock slightly resembles an X lock. With an SIX lock, however, other transactions that want to read some of the data (read data at the row or page level and obtain an IS lock on the table) are allowed to proceed, so concurrency is better than with an X lock. Lock mode compatibility will be described in greater detail later in this module.
If other transactions obtain S row locks in a PUBLICROW table or S page locks in a PUBLIC table on rows that the SIX transaction wants to modify, the SIX transaction must wait until the S locks are released before it can modify the data.
Other transactions that want to read all of the data (obtain an S lock on the table) or that want to write to any portion of the data are not allowed to proceed until the SIX lock is released.
An SIX lock is also called a share subexclusive lock.

X lock (exclusive)
The lock owner can read or change data in the table, partition, or table space. A concurrent process can access the data if the process runs with UR isolation or if data in a partitioned table space is running with CS isolation and CURRENTDATA((NO). The lock owner does not need page or row locks.

Example
An SQL statement locates John Smith in a table of customer data and changes his address. The statement locks the entire table space in mode IX and the specific row that it changes in mode X.
'''

'''
The following shows whether page locks of any two modes, or row locks of any two modes are compatible. No question of compatibility arises between page and row locks, because a table space cannot use both page and row locks. No question of compatibility arises between page and row locks, because a table space cannot use both page and row locks.

Table 1. Compatibility matrix of page lock and row lock modes

Lock_mode	        Share (S-lock)	Update (U-lock)	Exclusive (X-lock)
----------------------------------------------------------------------
Share (S-lock)	    Yes	            Yes	            No
Update (U-lock)	    Yes	            No	            No
Exclusive (X-lock)	No	            No	            No

Compatibility for table space locks is slightly more complex that for page and row locks. The following table shows whether table space locks of any two modes are compatible.
Table 2. Compatibility of table and table space (or partition) lock modes
Lock_Mode	IS	IX	S	U	SIX	X
------------------------------------
IS	        Yes	Yes	Yes	Yes	Yes	No
IX	        Yes	Yes	No	No	No	No
S	        Yes	No	Yes	Yes	No	No
U	        Yes	No	Yes	No	No	No
SIX	        Yes	No	No	No	No	No
X	        No	No	No	No	No	No
'''

'''
Suspension
Incoming lock requests are queued. Requests for lock promotion, and requests for a lock by an application process that already holds a lock on the same object, precede requests for locks by new applications. Within those groups, the request order is "first in, first out."
'''
 

