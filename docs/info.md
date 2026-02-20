<!---

This file is used to generate your project datasheet. Please fill in the information below and delete any unused
sections.

You can also include images in this folder and reference them in the markdown. Each image must be less than
512 kb in size, and the combined size of all images must be less than 1 MB.
-->

## How it works

This project implements a temporal encoder and decoder for permutation indices. The decoder receives 8-bit one-hot inputs sequentially (one per clock cycle) representing a permutation's arrival order, and computes the corresponding factorial number system index. The decoder output is then fed into the encoder, which converts the index back into a sequence of one-hot outputs. The decoder output (lower 8 bits of the 17-bit permutation index) is available on `uo_out`, and the encoder's one-hot temporal output is available on `uio_out`.

## How to test

Apply a reset (pull `rst_n` low for several cycles, then release). Then send a permutation as a sequence of one-hot values on `ui_in` (one bit set per cycle, each bit used exactly once across 8 cycles). After the pipeline latency, the decoder output appears on `uo_out` and the encoder begins emitting one-hot outputs on `uio_out`.

## External hardware

None
