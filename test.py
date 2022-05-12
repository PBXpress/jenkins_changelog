import sys

from JenkinsChangeLogs import JenkinsChangeLogs

if __name__ == '__main__':
    jclo = JenkinsChangeLogs()
    for arg in sys.argv[1:]:
        jclo.append(arg)
