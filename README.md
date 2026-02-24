![](../../workflows/gds/badge.svg) ![](../../workflows/docs/badge.svg) ![](../../workflows/test/badge.svg) ![](../../workflows/fpga/badge.svg)

# Temporal Encoder/Decoder

This project implements a temporal encoder and decoder for permutation indices. The decoder receives 8-bit one-hot inputs sequentially (one per clock cycle) representing a permutation's arrival order, and computes the corresponding factorial number system index. The decoder output is then fed into the encoder, which converts the index back into a sequence of one-hot outputs. The decoder output (lower 8 bits of the 16-bit permutation index) is available on `uo_out`, and the encoder's one-hot temporal output is available on `uio_out`.

You can see the gold model implemented here: <https://github.com/sifferman/temporal_encoder/blob/main/dv/dv_pkg.sv>.

## Notable Design Characteristics

This design takes advantage of SystemVerilog parameterized classes: [`temporal_encoder_helper`](https://github.com/sifferman/temporal_encoder/blob/main/rtl/temporal_encoder_helper.sv). The design is fully supported by vcs, verilator, and sv2v.

The design is well optimized, and can operate at 29.14 MHz on the ICE40UP5K-SG48I FPGA with, and 50.25 MHz on sky130.
