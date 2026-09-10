module rv_fifo #(parameter integer WIDTH=64,DEPTH=4)(
 input wire clk,reset,input wire in_valid,output wire in_ready,input wire [WIDTH-1:0] in_data,
 output wire out_valid,input wire out_ready,output wire [WIDTH-1:0] out_data
);
 localparam PW=(DEPTH<2)?1:$clog2(DEPTH),CW=$clog2(DEPTH+1);
 reg [WIDTH-1:0] mem[0:DEPTH-1];reg [PW-1:0] rp,wp;reg [CW-1:0] count;
 wire push=in_valid&&in_ready,pop=out_valid&&out_ready;
 assign in_ready=(count<DEPTH);assign out_valid=(count!=0);assign out_data=mem[rp];
 always @(posedge clk)begin
   if(reset)begin rp<=0;wp<=0;count<=0;end
   else begin
     if(push)begin mem[wp]<=in_data;wp<=(wp==DEPTH-1)?0:wp+1'b1;end
     if(pop)rp<=(rp==DEPTH-1)?0:rp+1'b1;
     case({push,pop})2'b10:count<=count+1'b1;2'b01:count<=count-1'b1;default:count<=count;endcase
   end
 end
endmodule
