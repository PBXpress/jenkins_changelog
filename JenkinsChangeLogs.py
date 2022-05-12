from collections import OrderedDict
from datetime import datetime

class JCLEContactWithTS:
    email = None
    name = None
    timestamp = None

    def __init__(self, val):
        espos = val.index('<')
        self.name = val[:espos].strip()
        val = val[espos + 1:]
        eepos = val.index('>')
        self.email = val[:eepos]
        timestamp_s = val[eepos + 2:]
        self.timestamp = datetime.strptime(timestamp_s, '%Y-%m-%d %H:%M:%S %z')
        #print(F'"{self.name}" "{self.email}" "{self.timestamp}"')

class JCLEntry:
    _commit = None
    _tree = None
    _parent = None
    _author = None
    _committer = None
    message = None
    metadata = None

    def __init__(self):
        self.message = []
        self.metadata = []

    @property
    def commit(self):
        return self._commit

    @commit.setter
    def commit(self, val):
        if self._commit is not None:
            raise ValueError(F'{type(self)}.commit is already set')
        self._commit = val

    @property
    def tree(self):
        return self._tree

    @tree.setter
    def tree(self, val):
        if self._tree is not None:
            raise ValueError(F'{type(self)}.tree is already set')
        self._tree = val

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, val):
        if self._parent is not None:
            raise ValueError(F'{type(self)}.parent is already set')
        self._parent = val

    @property
    def author(self):
        return self._author

    @author.setter
    def author(self, val):
        if self._author is not None:
            raise ValueError(F'{type(self)}.author is already set')
        self._author = JCLEContactWithTS(val)

    @property
    def committer(self):
        return self._committer

    @committer.setter
    def committer(self, val):
        if self._committer is not None:
            raise ValueError(F'{type(self)}.committer is already set')
        self._committer = JCLEContactWithTS(val)

class JenkinsChangeLogs:
    changes_by_commit = None

    def __init__(self, fname = None):
        self.changes_by_commit = OrderedDict()
        if fname is None:
            return
        self.append(fname)

    def append(self, fname):
        logs = open(fname).readlines()
        inbuf = []
        for logline in logs:
            if logline.startswith('commit ') and len(inbuf) > 0:
                self.injest_chunk(inbuf)
                inbuf = [logline,]
                continue
            inbuf.append(logline)
        if len(inbuf) > 0:
            self.injest_chunk(inbuf)

    def injest_chunk(self, chunk):
        #print('Chunk:', chunk)
        chunk = [x[:-1] for x in chunk]
        jcle = JCLEntry()
        for idx, line in enumerate(chunk):
            if len(line) == 0:
                break
            pname, pval = line.split(' ', 1)
            setattr(jcle, pname, pval)
            #print('  Param:', pname, pval)
        #print(jcle.commit)
        for idx1, line in enumerate(chunk[idx + 1:]):
            if not line.startswith('    '):
                break
            line = line[4:]
            jcle.message.append(line)
            #print('  Change Log:', line)
        for line in chunk[idx + idx1 + 3:]:
            #print('  MetaData:', line)
            jcle.metadata.append(line)
        self.changes_by_commit[jcle.commit] = jcle

if __name__ == '__main__':
    jcle = JCLEntry()
    jcle.commit = 'abcd'
    assert(jcle.commit == 'abcd')
    try:
        jcle.commit = 'abcd'
    except ValueError:
        pass
    else:
        assert(False)

    flist = (('130', '5446375514878251402'), ('131', '6911635698393948001'), ('171', '9945418633305796411'))

    jclo = JenkinsChangeLogs()
    for x, y in flist:
        jclo.append(F'/var/db/jenkins/workspace/build-fw-sippydo-32/changelogs.{x}/changelog{y}.xml')

    for cmt in jclo.changes_by_commit.values():
        print(cmt.message)
