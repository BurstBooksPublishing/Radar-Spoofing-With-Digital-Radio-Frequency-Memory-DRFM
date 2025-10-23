module stream_pipe (
  input  wire clk,
  input  wire rst_n,
  input  wire in_valid,               // source asserts valid
  input  wire [31:0] in_data,
  output wire in_ready,               // downstream ready
  output wire out_valid,              // sink ready/valid
  output wire [31:0] out_data
);
  // Small FIFO buffer (BRAM or distributed)
  // Pipeline stage 0: input register
  reg [31:0] reg0;
  reg        reg0_v;
  always @(posedge clk) begin
    if (!rst_n) begin reg0_v <= 1'b0; end
    else if (in_valid && in_ready) begin reg0 <= in_data; reg0_v <= 1'b1; end
    else if (out_valid && out_ready) begin reg0_v <= 1'b0; end
  end

  // Stage 1: DSP multiply (example)
  wire [47:0] mult_out; // fast multiply via DSP slice
  assign mult_out = reg0 * 16'h0100; // scale by constant

  // Stage 2: output register
  reg [31:0] reg1;
  reg        reg1_v;
  always @(posedge clk) begin
    if (!rst_n) begin reg1_v <= 1'b0; end
    else if (reg0_v) begin reg1 <= mult_out[31:0]; reg1_v <= 1'b1; end
    else if (out_valid && out_ready) begin reg1_v <= 1'b0; end
  end

  assign in_ready  = !reg0_v;        // simple backpressure
  assign out_valid = reg1_v;
  assign out_data  = reg1;
endmodule