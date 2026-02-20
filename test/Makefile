# Makefile
# See https://docs.cocotb.org/en/stable/quickstart.html for more info

# defaults
SIM ?= icarus
FST ?= -fst # Use more efficient FST format
TOPLEVEL_LANG ?= verilog
SRC_DIR = $(PWD)/../src
PROJECT_SOURCES = sifferman_temporal_encoder_decoder/rtl.sv2v.v project.v

# sv2v conversion (rule defined after cocotb include to avoid becoming default target)
SV2V_DIR = $(SRC_DIR)/sifferman_temporal_encoder_decoder
SV2V_OUT = $(SV2V_DIR)/rtl.sv2v.v
SV2V_SRC = $(SV2V_DIR)/rtl/temporal_encoder_helper.sv \
           $(SV2V_DIR)/rtl/temporal_encoder.sv \
           $(SV2V_DIR)/rtl/temporal_decoder.sv

ifneq ($(GATES),yes)

# RTL simulation:
SIM_BUILD				= sim_build/rtl
VERILOG_SOURCES += $(addprefix $(SRC_DIR)/,$(PROJECT_SOURCES))

else

# Gate level simulation:
SIM_BUILD				= sim_build/gl
COMPILE_ARGS    += -DGL_TEST
COMPILE_ARGS    += -DFUNCTIONAL
COMPILE_ARGS    += -DUSE_POWER_PINS
COMPILE_ARGS    += -DSIM
COMPILE_ARGS    += -DUNIT_DELAY=\#1
VERILOG_SOURCES += $(PDK_ROOT)/sky130A/libs.ref/sky130_fd_sc_hd/verilog/primitives.v
VERILOG_SOURCES += $(PDK_ROOT)/sky130A/libs.ref/sky130_fd_sc_hd/verilog/sky130_fd_sc_hd.v

# this gets copied in by the GDS action workflow
VERILOG_SOURCES += $(PWD)/gate_level_netlist.v

endif

# Allow sharing configuration between design and testbench via `include`:
COMPILE_ARGS 		+= -I$(SRC_DIR)

# Include the testbench sources:
VERILOG_SOURCES += $(PWD)/tb.v
TOPLEVEL = tb

# List test modules to run, separated by commas and without the .py suffix:
COCOTB_TEST_MODULES = test

# include cocotb's make rules to take care of the simulator setup
include $(shell cocotb-config --makefiles)/Makefile.sim

# sv2v build rule
$(SV2V_OUT): $(SV2V_SRC)
	sv2v $^ -DSYNTHESIS -w $@

# Ensure sv2v runs before cocotb sim
sim: $(SV2V_OUT)

# Standalone SystemVerilog testbench using the original DV
.PHONY: sim_sv
sim_sv:
	$(MAKE) -C $(SRC_DIR)/sifferman_temporal_encoder_decoder sim
