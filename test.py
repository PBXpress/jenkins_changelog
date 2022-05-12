from datetime import datetime, timezone
import sys

from JenkinsChangeLogs import JenkinsChangeLogs

if __name__ == '__main__':
    jclo = JenkinsChangeLogs()
    for arg in sys.argv[1:]:
        jclo.append(arg)
    print(F'Changesets Loaded: {len(jclo)}')

    fdate = datetime(2022, 1, 1, tzinfo = timezone.utc)
    jclo_f = jclo.get_filtered(lambda x: x.timestamp >= fdate)

    for since, jclo_x in ('Beginning', jclo), (str(fdate), jclo_f):
        print(F'Stats since {since}:')

        for ename, x in jclo_x.get_summary(order = True).items():
            print('  ', ename, x)

        for ename, x in jclo_x.get_summary('author', order = True).items():
            print('  ', ename, x)
