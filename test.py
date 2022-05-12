import sys

from JenkinsChangeLogs import JenkinsChangeLogs

if __name__ == '__main__':
    jclo = JenkinsChangeLogs()
    for arg in sys.argv[1:]:
        jclo.append(arg)
    print(F'Changesets Loaded: {len(jclo.changes_by_commit)}')

    for ename, x in jclo.get_summary().items():
        print(ename, x)

    for ename, x in jclo.get_summary('author').items():
        print(ename, x)
