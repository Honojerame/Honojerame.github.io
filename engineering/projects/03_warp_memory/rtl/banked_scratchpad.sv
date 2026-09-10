// A bank serves one distinct word per cycle. Duplicate loads broadcast for free.
// Conflicting same-address stores are deterministic: highest active lane wins.
module banked_scratchpad #(parameter integer LANES=32,BANKS=8,WORDS=256)(
 input wire clk,reset,
 input wire in_valid,output wire in_ready,input wire is_store,
 input wire [LANES-1:0] lane_mask,input wire [LANES*32-1:0] word_addr,store_data,
 output wire out_valid,input wire out_ready,output reg [LANES*32-1:0] load_data,
 output reg out_error,output reg [31:0] service_cycles
);
 localparam IDLE=0,SERVICE=1,OUTPUT=2;
 reg [1:0] state;reg write_op;
 wire [31:0] bank_read[0:BANKS-1];
 reg [31:0] bank_value[0:BANKS-1],bank_word[0:BANKS-1];
 reg [LANES-1:0] pending,served;
 reg [LANES*32-1:0] addresses,values;
 integer chosen[0:BANKS-1];integer i,j,b;reg bad;
 always @* begin
   served=0;bad=0;
   for(integer k=0;k<LANES;k=k+1)if(lane_mask[k]&&word_addr[k*32+:32]>=WORDS)bad=1;
   for(integer bank=0;bank<BANKS;bank=bank+1)begin
     chosen[bank]=-1;bank_value[bank]=0;bank_word[bank]=0;
     for(integer lane=0;lane<LANES;lane=lane+1)
       if(pending[lane]&&(addresses[lane*32+:32]%BANKS)==bank&&chosen[bank]==-1)chosen[bank]=lane;
     if(chosen[bank]!=-1)begin
       bank_word[bank]=addresses[chosen[bank]*32+:32]/BANKS;
       for(integer lane=0;lane<LANES;lane=lane+1)
         if(pending[lane]&&addresses[lane*32+:32]==addresses[chosen[bank]*32+:32])begin
           served[lane]=1;bank_value[bank]=values[lane*32+:32];
         end
     end
   end
 end
 assign in_ready=(state==IDLE);assign out_valid=(state==OUTPUT);
 genvar bank;
 generate for(bank=0;bank<BANKS;bank=bank+1)begin:storage_bank
   // One physical write port per bank, regardless of the number of lanes.
   reg [31:0] words[0:WORDS/BANKS-1];
   assign bank_read[bank]=words[bank_word[bank]];
   always @(posedge clk)if(!reset&&state==SERVICE&&write_op&&chosen[bank]!=-1)
     words[bank_word[bank]]<=bank_value[bank];
 end endgenerate
 always @(posedge clk)begin
   if(reset)begin state<=IDLE;pending<=0;addresses<=0;values<=0;write_op<=0;load_data<=0;out_error<=0;service_cycles<=0;end
   else begin
     if(in_valid&&in_ready)begin
       addresses<=word_addr;values<=store_data;write_op<=is_store;load_data<=0;
       pending<=bad?{LANES{1'b0}}:lane_mask;out_error<=bad;service_cycles<=0;
       state<=(bad||lane_mask==0)?OUTPUT:SERVICE;
     end
     if(state==SERVICE)begin
       service_cycles<=service_cycles+1;pending<=pending&~served;
       for(i=0;i<LANES;i=i+1)if(served[i])begin
         if(!write_op)load_data[i*32+:32]<=bank_read[addresses[i*32+:32]%BANKS];
       end
       if((pending&~served)==0)state<=OUTPUT;
     end
     if(out_valid&&out_ready)state<=IDLE;
   end
 end
endmodule
