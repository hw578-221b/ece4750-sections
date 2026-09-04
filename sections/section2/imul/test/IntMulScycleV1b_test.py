#=========================================================================
# IntMulScycleV1_test
#=========================================================================

from pymtl3 import *
from pymtl3.stdlib.test_utils import run_test_vector_sim

from imul.IntMulScycleV1 import IntMulScycleV1

#-------------------------------------------------------------------------
# test_basic
#-------------------------------------------------------------------------
# Output ports need to be indicated by adding a * suffix for run_test_vector_sim() function
def test_basic( cmdline_opts ):
  run_test_vector_sim( IntMulScycleV1(), [
    ('in0 in1 out*'),
    [ 2, 2, '?' ], # Initial output is ignored
    [ 3, 2,  4  ], # Result from previous 2 * 2 (after 1 cycle)
    [ 3, 3,  6  ], # Result from previous 3 * 2
    [ 0, 0,  9  ], # Result from previous 3 * 3
    [ 0, 0,  0  ], # Result from previous 0 * 0
  ], cmdline_opts )

#-------------------------------------------------------------------------
# test_overflow
#-------------------------------------------------------------------------

def test_overflow( cmdline_opts ):
  run_test_vector_sim( IntMulScycleV1(), [
    ('in0         in1 out*'),
    [ 0x80000001, 2, '?' ],
    [ 0xc0000002, 4,  2  ],
    [ 0x00000000, 0,  8  ],
    [ 0x00000000, 0,  0  ],
  ], cmdline_opts )

