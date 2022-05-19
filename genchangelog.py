from datetime import datetime, timezone
import sys

from JenkinsChangeLogs import JenkinsChangeLogs

if __name__ == '__main__':
    jclo = JenkinsChangeLogs()
    for arg in sys.argv[1:-1]:
        jclo.append(arg)
    print(F'Changesets Loaded: {len(jclo)}')

    print(F'Stats:')

    for ename, x in jclo.get_summary(order = True).items():
        print('  ', ename, x)

    for ename, x in jclo.get_summary('author', order = True).items():
        print('  ', ename, x)

    htmldoc = jclo.gen_html()
    open(sys.argv[-1], 'w').write(htmldoc)
