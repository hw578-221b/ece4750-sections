#=========================================================================
# imul-v1-adhoc-test <input-values>
#=========================================================================

from sys import argv

from pymtl3  import *
from pymtl3.passes.backends.verilog import *

from IntMulScycleV1 import IntMulScycleV1

# Get list of input values from command line
# Python uses the [start:stop:step] slicing syntax to extract specific elements:
# argv[1::2]: Starts at index 1 (the first actual argument), goes to the end of the list, and skips every other item (step=2). 
# This extracts items at odd indexes: 1, 3, 5, 7, etc.
# argv[2::2]: Starts at index 2 (the second argument), goes to the end, and skips every other item (step=2). 
# This extracts items at even indexes: 2, 4, 6, 8, etc.

# int(x, base) function converts a string x into an integer.
# Passing 0 as the base tells Python to automatically detect the number format based on its prefix.
# It parses hexadecimal strings like '0x1A' as base 16.It parses binary strings like '0b1010' as base 2.

# [int(x, 0) for x in ...] shorthand way to loop through a list and create a new one in a single line.
in0_values = [ int(x,0) for x in argv[1::2] ]
in1_values = [ int(x,0) for x in argv[2::2] ]

# Create and elaborate the model
# This creates an instance of the Python wrapper class
model = IntMulScycleV1()
# Build and inspect the entire hardware hierarchy
model.elaborate()

# Apply the Verilog import passes and the default pass group
# A PyMTL pass is an operation that analyzes, annotates, transforms, or prepares a hardware model

# checks whether the model has been elaborated and automatically elaborates it when necessary
# VerilogPlaceholderPass, is a Python class representing the pass. The parentheses create an instance of the pass.
model.apply( VerilogPlaceholderPass() )
# First parentheses VerilogTranslationImportPass() Create a pass object.
# Second parentheses import_pass( model ) Call that pass object with model as its argument.
# The original model is a placeholder. The new object is connected to the compiled Verilator simulation.
# Translation meaning: VerilogTranslationImportPass supports both Translating PyMTL RTL into Verilog and Importing Verilog into PyMTL
# Import means turning the Verilog module into an executable object that looks like a PyMTL component.
model = VerilogTranslationImportPass()( model )
# DefaultPassGroup(...) creates a configured collection of simulation passes.
# A “pass group” bundles several related passes so you do not need to apply each one separately.
# Internally, the default group performs work such as:
# Analyzing update-block dependencies; Scheduling combinational and sequential activity; Preparing the simulator
# Adding clock-tick support; Adding reset support; Adding line tracing; Adding text-wave recording; Adding VCD generation
# linetrace means print the model’s compact line trace during simulation
# The line-trace format itself comes from the Verilog tracing code
# textwave enables recording of signal values in a terminal-friendly waveform
# vcdwave: This enables VCD waveform generation and provides the base filename.
model.apply( DefaultPassGroup(linetrace=True,textwave=True,vcdwave="imul-v1-adhoc-test") )
# group = DefaultPassGroup(....) creates a configured pass-group object. It does not apply the group to the model yet
# model.apply(group) applies it. Internally, apply essentially does: group(model)
# So this line is equivalent to DefaultPassGroup(linetrace=True,textwave=True,vcdwave="imul-v1-adhoc-test")(model)
# DefaultPassGroup.__call__() modifies model in place and returns None, so don't do model = DefaultPassGroup(..)(..)
# Syntax: PassClass(configuration_arguments)(model_argument)

# Replacement pass style
# model = VerilogTranslationImportPass()( model )
# This pass returns an imported replacement model. The return value must be saved.

# In-place pass style
# model.apply( DefaultPassGroup(...) )
# Pass modifies model in place, doesn't return value

# Reset simulator

model.sim_reset()

# Apply input values and display output values

for in0_value,in1_value in zip(in0_values,in1_values):

  # Write input value to input port

  model.in0 @= in0_value # @= writes a value to a PyMTL input port
  model.in1 @= in1_value
  model.sim_eval_combinational() # lets the combinational parts of the model settle, but it does not update the registers.

  # Tick simulator one cycle (one cycle needed to compute mult before change input parameters)

  model.sim_tick()

# Tick simulator three more cycles and print text wave

model.sim_tick()
model.sim_tick()
model.sim_tick()
# prints the recorded waveform.
model.print_textwave()

