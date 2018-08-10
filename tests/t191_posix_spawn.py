#!/usr/bin/env python

from runtest import TestBase

class TestCase(TestBase):
    def __init__(self):
        TestBase.__init__(self, 'posix_spawn', """
# DURATION    TID     FUNCTION
            [ 9874] | main() {
            [ 9874] |   posix_spawn() {
 142.145 us [ 9874] |   } /* posix_spawn */
            [ 9874] |   waitpid() {
            [ 9874] |     /* linux:sched-out */
            [ 9875] | main() {
            [ 9875] |   a() {
            [ 9875] |     b() {
            [ 9875] |       c() {
            [ 9875] |         getpid() {
   0.976 us [ 9875] |         } /* getpid */
   1.992 us [ 9875] |       } /* c */
   2.828 us [ 9875] |     } /* b */
   3.658 us [ 9875] |   } /* a */
   7.713 us [ 9875] | } /* main */
   1.311 ms [ 9874] |     /* linux:sched-in */
   1.315 ms [ 9874] |   } /* waitpid */
            [ 9874] |   posix_spawn() {
 132.836 us [ 9874] |   } /* posix_spawn */
            [ 9874] |   waitpid() {
            [ 9874] |     /* linux:sched-out */
            [ 9876] | main() {
            [ 9876] |   fopen() {
   2.828 us [ 9876] |   } /* fopen */
            [ 9876] |   fclose() {
   3.658 us [ 9876] |   } /* fclose */
   7.713 us [ 9876] | } /* main */
   1.380 ms [ 9874] |     /* linux:sched-in */
   1.382 ms [ 9874] |   } /* waitpid */
   2.708 ms [ 9874] | } /* main */

""")

    def build(self, name, cflags='', ldflags=''):
        ret  = TestBase.build(self, 'abc', cflags, ldflags)
        ret += TestBase.build(self, 'openclose', cflags, ldflags)
        ret += TestBase.build(self, self.name, cflags, ldflags)
        return ret

    def runcmd(self):
        return '%s -F main --no-merge %s' % (TestBase.uftrace_cmd, 't-' + self.name)

    def fixup(self, cflags, result):
        import re
        return re.sub('.*linux:sched.*\n', '', result)
