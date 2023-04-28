/*
    file: seg.v
    author: Jingbo Su
    created: August 2022
*/

`timescale 1ns / 1ps

module SEG (
  input clk,
  input wire[11:0] val,
  output reg[2:0] sel,
  output reg[7:0] seg
);

initial begin
  sel = 3'b100;
end

reg[3:0] data = 0;

always @(posedge clk) begin
  case (sel)
    3'b100 : begin data = val[3:0]; end
    3'b101 : begin data = val[11:8]; end
    3'b110 : begin data = val[7:4]; end
  endcase

  sel = sel + 1'd1;
  if (sel > 3'd6) begin
    sel = 3'd4;
  end

end

always @(posedge clk) begin
  case(data)
    4'h0: seg = 8'b00111111;
    4'h1: seg = 8'b00000110;
    4'h2: seg = 8'b01011011;
    4'h3: seg = 8'b01001111;
    4'h4: seg = 8'b01100110;
    4'h5: seg = 8'b01101101;
    4'h6: seg = 8'b01111101;
    4'h7: seg = 8'b00000111;
    4'h8: seg = 8'b01111111;
    4'h9: seg = 8'b01101111;
    4'ha: seg = 8'b01110111;
    4'hb: seg = 8'b01111100;
    4'hc: seg = 8'b00111001;
    4'hd: seg = 8'b01011110;
    4'he: seg = 8'b01111001;
    4'hf: seg = 8'b01000000;
  endcase
end

endmodule