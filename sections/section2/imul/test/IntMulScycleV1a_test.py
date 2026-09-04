#=========================================================================
# IntMulScycleV1_test
#=========================================================================

from pymtl3 import *
from pymtl3.passes.backends.verilog import *
from pymtl3.stdlib.test_utils import config_model_with_cmdline_opts

from imul.IntMulScycleV1 import IntMulScycleV1

# It looks exactly like our imul-v1-assertion-test.py script with two changes, and we use pytest to run this test:
# we pass in cmdline_opts to each test case function
# we do not need to explicitly call the test case functions at the bottom of the script
# pytest will assume any function that starts with the test_ prefix is a test case

#-------------------------------------------------------------------------
# test_basic
#-------------------------------------------------------------------------

def test_basic( cmdline_opts ):

  # Create and elaborate the model

  model = IntMulScycleV1()
  model.elaborate()

  # Apply the Verilog import passes and the default pass group

  model.apply( VerilogPlaceholderPass() )
  model = VerilogTranslationImportPass()( model )
  model.apply( DefaultPassGroup(linetrace=True,vcdwave="imul-v1-test-basic") )

  # Reset simulator

  model.sim_reset()

  # Write inputs and check outputs

  model.in0 @= 2
  model.in1 @= 2
  model.sim_tick()
  assert model.out == 4

  # Tick simulator three more cycles

  model.sim_tick()
  model.sim_tick()
  model.sim_tick()

  model.finalize()

#-------------------------------------------------------------------------
# test_overflow
#-------------------------------------------------------------------------

def test_overflow( cmdline_opts ):

  # Create and elaborate the model

  model = IntMulScycleV1()
  model.elaborate()

  # Apply the Verilog import passes and the default pass group

  model.apply( VerilogPlaceholderPass() )
  model = VerilogTranslationImportPass()( model )
  model.apply( DefaultPassGroup(linetrace=True,vcdwave="imul-v1-test-overflow") )

  # Reset simulator

  model.sim_reset()

  # Write inputs and check outputs

  model.in0 @= 0x80000001
  model.in1 @= 2
  model.sim_tick()
  assert model.out == 2

  # Tick simulator three more cycles

  model.sim_tick()
  model.sim_tick()
  model.sim_tick()

