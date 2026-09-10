// Output-stationary PE: operands advance one hop per enabled clock.
module mac_pe(input wire clk,reset,clear,enable,
 input wire signed [7:0] a_in,b_in,
 output reg signed [7:0] a_out,b_out,
 output reg signed [31:0] accumulator);
 wire signed [15:0] product=a_in*b_in;
 always @(posedge clk)begin
   if(reset||clear)begin a_out<=0;b_out<=0;accumulator<=0;end
   else if(enable)begin
     a_out<=a_in;b_out<=b_in;
     accumulator<=accumulator+{{16{product[15]}},product};
   end
 end
endmodule
