#!/usr/bin/env python

import re
from runtest import TestBase

class TestCase(TestBase):
    def __init__(self):
        TestBase.__init__(self, 'racycount', ldflags='-pthread', result="""
# DURATION    TID     FUNCTION
            [22829] | __monstartup() {
  17.753 us [22829] | } /* __monstartup */
            [22829] | __cxa_atexit() {
   8.038 us [22829] | } /* __cxa_atexit */
            [22829] | main() {
            [22829] |   pthread_barrier_init() {
   6.095 us [22829] |   } /* pthread_barrier_init */
            [22829] |   pthread_create() {
  81.734 us [22829] |   } /* pthread_create */
            [22829] |   pthread_create() {
  85.171 us [22829] |   } /* pthread_create */
            [22829] |   racy_count() {
            [22829] |     pthread_barrier_wait() {
            [22829] |       /* linux:sched-out */
            [22832] |                 thread_fn() {
            [22832] |                   racy_count() {
            [22831] |                                 thread_fn() {
            [22832] |                     pthread_barrier_wait() {
            [22832] |                       /* linux:sched-out */
            [22831] |                                   racy_count() {
            [22831] |                                     pthread_barrier_wait() {
  21.614 us [22831] |                                     } /* pthread_barrier_wait */
 219.348 us [22829] |       /* linux:sched-in */
 246.706 us [22829] |     } /* pthread_barrier_wait */
  68.314 us [22832] |                       /* linux:sched-in */
  78.105 us [22832] |                     } /* pthread_barrier_wait */
 300.416 us [22831] |                                   } /* racy_count */
 314.149 us [22831] |                                 } /* thread_fn */
 567.337 us [22829] |   } /* racy_count */
            [22829] |   pthread_join() {
            [22829] |     /* linux:sched-out */
 370.700 us [22832] |                   } /* racy_count */
 383.658 us [22832] |                 } /* thread_fn */
 319.033 us [22829] |     /* linux:sched-in */
 334.627 us [22829] |   } /* pthread_join */
            [22829] |   pthread_join() {
   5.735 us [22829] |   } /* pthread_join */
   1.122 ms [22829] | } /* main */
""")

    def runcmd(self):
        return '%s --no-pltbind --column-view --no-merge %s' % (TestBase.uftrace_cmd, 't-' + self.name)

    def fixup(self, cflags, result):
        return re.sub('.*linux:sched.*\n', '', result)
