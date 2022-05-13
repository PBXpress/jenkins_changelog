from collections import OrderedDict
from datetime import datetime
from textwrap import wrap
import html

from JCLHtmlGen import JCLHtmlGen

class JCLEContactWithTS:
    email = None
    name = None
    ename = None
    timestamp = None

    def __init__(self, val):
        espos = val.index('<')
        self.name = val[:espos].strip()
        val = val[espos + 1:]
        eepos = val.index('>')
        self.email = val[:eepos]
        timestamp_s = val[eepos + 2:]
        self.timestamp = datetime.strptime(timestamp_s, '%Y-%m-%d %H:%M:%S %z')
        self.ename = (self.name, self.email)
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

class JCLStats:
    stats_by = None
    count = 1

    def __init__(self, stats_by):
        self.stats_by = stats_by

    def __str__(self):
        return F'{self.stats_by}: {self.count}'

class JenkinsChangeLogs:
    changes_by_commit = None

    def __init__(self, fname = None):
        self.changes_by_commit = OrderedDict()
        if fname is None:
            return
        self.append(fname)

    def __len__(self):
        return len(self.changes_by_commit)

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

    def get_summary(self, stats_by = 'committer', order = False):
        stats_res = dict()
        for change in self.changes_by_commit.values():
            change_by = getattr(change, stats_by).ename
            if change_by not in stats_res:
                stats_res[change_by] = JCLStats(stats_by)
            else:
                stats_res[change_by].count += 1
        if order:
            stats_res = dict(sorted(stats_res.items(), key = lambda x: x[1].count, reverse = True))
        return stats_res

    def get_filtered(self, ffunc, filter_by = 'committer'):
        filter_res = JenkinsChangeLogs()
        for commit, change in self.changes_by_commit.items():
            change_by = getattr(change, filter_by)
            if ffunc(change_by):
                filter_res.changes_by_commit[commit] = change
        return filter_res

    def gen_html(self):
        jhgen = JCLHtmlGen()

        seen = dict()
        seen['date'] = None
        seen['author'] = None

        def gen_author(seen, cmt):
            if cmt.author.ename == seen['author']:
                return ''
            author = [html.escape(cmt.author.name)]
            jhgen.wraptag(author, 'a', href = F'mailto:{cmt.author.email}')
            seen['author'] = cmt.author.ename
            return author

        def wrap_nl(txt, wrap_at):
            otxt = wrap(txt, wrap_at)
            if len(otxt) > 1:
                otxt.append('')
            return otxt

        def gen_message(cmt):
            wrap_trs = 160
            if max([len(x) for x in cmt.message]) > wrap_trs:
                wrap_at = 120
                rmsg = [wrap_nl(x, wrap_at) for x in cmt.message]
                rmsg = [item for sublist in rmsg for item in sublist]
            else:
                rmsg = [x for x in cmt.message]
            return jhgen.wraptag([html.escape(x) for x in rmsg], 'pre')

        def gen_date(seen, cmt):
            sdate = str(cmt.committer.timestamp).split(None, 1)[0]
            if sdate == seen['date']:
                return ''
            seen['date'] = sdate
            seen['author'] = None
            return sdate

        clnames = ('Date', 'Author', 'Message')
        cgens = (
          lambda x: gen_date(seen, x),
          lambda y: gen_author(seen, y),
          lambda z: gen_message(z),
        )

        changes = self.changes_by_commit.values()
        changes = sorted(changes, key = lambda x: x.committer.timestamp, reverse = True)
        htmldoc = jhgen.genTable(clnames, changes, *cgens)
        return '\n'.join(htmldoc)

if __name__ == '__main__':
    from datetime import timezone
    jcle = JCLEntry()
    jcle.commit = 'abcd'
    assert(jcle.commit == 'abcd')
    try:
        jcle.commit = 'abcd'
    except ValueError:
        pass
    else:
        assert(False)

    flist = (
      ('130', '5446375514878251402'),
      ('131', '6911635698393948001'),
      ('171', '9945418633305796411'),
      ('172', '190640242552814648')
    )

    jclo = JenkinsChangeLogs()
    for x, y in flist:
        jclo.append(F'/var/db/jenkins/workspace/build-fw-sippydo-32/changelogs.{x}/changelog{y}.xml')

    htmldoc = jclo.gen_html()
    open('test.html', 'w').write(htmldoc)

    fdate = datetime(2022, 1, 1, tzinfo = timezone.utc)
    jclo_f = jclo.get_filtered(lambda x: x.timestamp >= fdate)

    for since, jclo_x in ('Beginning', jclo), (str(fdate), jclo_f):
        print(F'Stats since {since}:')
        for ename, x in jclo_x.get_summary().items():
            print('  ', ename, x)
        for ename, x in jclo_x.get_summary('author', order = True).items():
            print('  ', ename, x)
