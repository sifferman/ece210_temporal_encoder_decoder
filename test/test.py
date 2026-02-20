# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles, RisingEdge


def factorial(n):
    f = 1
    for i in range(2, n + 1):
        f *= i
    return f


def gold_temporal_decode(arrival_order, n):
    """Gold model: arrival order -> permutation index."""
    index = 0
    received = 0
    for t in range(n):
        k = arrival_order[t]
        count = 0
        for j in range(k):
            if not (received & (1 << j)):
                count += 1
        fact = factorial(n - 1 - t)
        index += count * fact
        received |= 1 << k
    return index


async def reset(dut):
    dut.ena.value = 1
    dut.ui_in.value = 0
    dut.uio_in.value = 0
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 10)
    dut.rst_n.value = 1
    await ClockCycles(dut.clk, 1)


async def send_permutation(dut, arrival_order):
    """Send a permutation as one-hot temporal inputs and wait for decoder output."""
    n = len(arrival_order)

    # Send each element one at a time as one-hot on ui_in
    for elem in arrival_order:
        dut.ui_in.value = 1 << elem
        await RisingEdge(dut.clk)
    dut.ui_in.value = 0

    # Wait for decoder output valid (uo_out updates when decoder finishes)
    # The decoder pipeline takes a few cycles after the last input
    for _ in range(20):
        await RisingEdge(dut.clk)

    # Read decoder output (lower 8 bits of permutation index)
    dec_out = dut.uo_out.value.integer
    return dec_out


@cocotb.test()
async def test_identity_permutation(dut):
    """Test identity permutation [0,1,2,...,7] -> index 0."""
    dut._log.info("Start")
    clock = Clock(dut.clk, 10, unit="us")
    cocotb.start_soon(clock.start())
    await reset(dut)

    dut._log.info("Test identity permutation")
    arrival_order = list(range(8))
    expected = gold_temporal_decode(arrival_order, 8)
    assert expected == 0, f"Gold model says identity should be 0, got {expected}"

    dec_out = await send_permutation(dut, arrival_order)
    expected_low8 = expected & 0xFF
    assert dec_out == expected_low8, f"Identity permutation: expected {expected_low8}, got {dec_out}"
    dut._log.info("Identity permutation test passed")


@cocotb.test()
async def test_reverse_permutation(dut):
    """Test reverse permutation [7,6,5,...,0] -> index 8!-1 = 40319."""
    clock = Clock(dut.clk, 10, unit="us")
    cocotb.start_soon(clock.start())
    await reset(dut)

    dut._log.info("Test reverse permutation")
    arrival_order = list(range(7, -1, -1))
    expected = gold_temporal_decode(arrival_order, 8)
    assert expected == factorial(8) - 1

    dec_out = await send_permutation(dut, arrival_order)
    expected_low8 = expected & 0xFF
    assert dec_out == expected_low8, f"Reverse permutation: expected {expected_low8}, got {dec_out}"
    dut._log.info("Reverse permutation test passed")


@cocotb.test()
async def test_swap_permutation(dut):
    """Test a simple swap permutation [1,0,2,3,4,5,6,7] -> index should be 5040."""
    clock = Clock(dut.clk, 10, unit="us")
    cocotb.start_soon(clock.start())
    await reset(dut)

    dut._log.info("Test swap permutation")
    arrival_order = [1, 0, 2, 3, 4, 5, 6, 7]
    expected = gold_temporal_decode(arrival_order, 8)

    dec_out = await send_permutation(dut, arrival_order)
    expected_low8 = expected & 0xFF
    assert dec_out == expected_low8, f"Swap permutation: expected {expected_low8}, got {dec_out}"
    dut._log.info("Swap permutation test passed")
