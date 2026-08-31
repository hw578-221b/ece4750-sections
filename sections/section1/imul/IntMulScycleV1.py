#=========================================================================
# IntMulScycleV1
#=========================================================================

# PyMTL3 wrapper for every component we want to test 

from pymtl3 import *
# This imports Verilog-related functionality, including:
# - VerilogPlaceholder
# - VerilogPlaceholderPass
# - VerilogTranslationImportPass
from pymtl3.passes.backends.verilog import *

# “Placeholder” means that this Python component temporarily represents the Verilog model. 
# During import, it is replaced by an executable, Verilator-backed component.
class IntMulScycleV1( VerilogPlaceholder, Component ):
  # This defines the component’s construction method. The method is called during elaboration.
  def construct( s ):
    s.in0 = InPort ( 32 )
    s.in1 = InPort ( 32 )
    s.out = OutPort( 32 )

# The clk and reset ports do not appear explicitly in this wrapper. 
# The placeholder pass scans the Verilog source and detects them automatically.
