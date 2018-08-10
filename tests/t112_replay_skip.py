#!/usr/bin/env python

from runtest import TestBase
import subprocess as sp

TDIR='xxx'

class TestCase(TestBase):
    def __init__(self):
        TestBase.__init__(self, 'thread', ldflags='-pthread', result="""
# DURATION    TID     FUNCTION
            [20053] | main() {
            [20053] |   pthread_create() {
  81.953 us [20053] |   } /* pthread_create */
            [20053] |   pthread_create() {
  53.108 us [20053] |   } /* pthread_create */
            [20053] |   pthread_create() {
 188.065 us [20053] |   } /* pthread_create */
            [20053] |   pthread_create() {
 184.846 us [20053] |   } /* pthread_create */
            [20053] |   pthread_join() {
 747.693 us [20053] |     /* linux:schedule */
 779.561 us [20053] |   } /* pthread_join */
            [20053] |   pthread_join() {
   1.136 us [20053] |   } /* pthread_join */
            [20053] |   pthread_join() {
   0.702 us [20053] |   } /* pthread_join */
            [20053] |   pthread_join() {
   0.650 us [20053] |   } /* pthread_join */
   1.309 ms [20053] | } /* main */
""")

    def pre(self):
        record_cmd = "%s record -d %s %s" % (TestBase.uftrace_cmd, TDIR, 't-' + self.name)
        sp.call(record_cmd.split())
        return TestBase.TEST_SUCCESS

    def runcmd(self):
        return '%s replay -F main --no-merge -d %s' % (TestBase.uftrace_cmd, TDIR)

    def post(self, ret):
        sp.call(['rm', '-rf', TDIR])
        return ret

    def fixup(self, cflags, result):
        import re
        return re.sub('.*linux:sched.*\n', '', result)
