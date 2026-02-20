/*
 * Copyright (c) 2026 Ethan Sifferman
 * SPDX-License-Identifier: Apache-2.0
 */

`default_nettype none

module tt_um_example (
    input  wire [7:0] ui_in,    // Dedicated inputs - decoder input (one-hot)
    output wire [7:0] uo_out,   // Dedicated outputs - decoder output (lower 8 of 17 bits)
    input  wire [7:0] uio_in,   // IOs: Input path (unused)
    output wire [7:0] uio_out,  // IOs: Output path - encoder output (8-bit one-hot)
    output wire [7:0] uio_oe,   // IOs: Enable path (active high: 0=input, 1=output)
    input  wire       ena,      // always 1 when the design is powered, so you can ignore it
    input  wire       clk,      // clock
    input  wire       rst_n     // reset_n - low to reset
);

  // All IOs are outputs
  assign uio_oe = 8'hFF;

  // Decoder: temporal one-hot input -> permutation index
  wire [16:0] dec_out;
  wire        dec_out_valid;

  temporal_decoder #(.NumInputs(8)) decoder (
      .clk_i       (clk),
      .rst_ni      (rst_n),
      .in_i        (ui_in),
      .out_o       (dec_out),
      .out_valid_o (dec_out_valid)
  );

  // Decoder output (lower 8 bits) to uo_out
  assign uo_out = dec_out[7:0];

  // Encoder: permutation index -> temporal one-hot output
  wire [7:0] enc_out;
  wire       enc_out_valid;
  wire       enc_out_last;
  wire       enc_in_ready;

  temporal_encoder #(.NumOutputs(8)) encoder (
      .clk_i       (clk),
      .rst_ni      (rst_n),
      .in_i        (dec_out),
      .in_valid_i  (dec_out_valid),
      .in_ready_o  (enc_in_ready),
      .out_o       (enc_out),
      .out_valid_o (enc_out_valid),
      .out_last_o  (enc_out_last)
  );

  // Encoder output to uio_out
  assign uio_out = enc_out;

  // List all unused inputs to prevent warnings
  wire _unused = &{ena, uio_in, enc_in_ready, enc_out_valid, enc_out_last, dec_out[16:8], 1'b0};

endmodule
