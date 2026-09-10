// One resident warp; many independent, tagged 32-byte sector loads in flight.
module warp_coalescer #(parameter integer LANES=32)(
 input wire clk,reset,
 input wire warp_valid,output wire warp_ready,input wire [31:0] warp_tag,
 input wire [LANES-1:0] lane_mask,input wire [LANES*32-1:0] lane_addr,
 output wire req_valid,input wire req_ready,output wire [31:0] req_addr,req_tag,
 input wire rsp_valid,output wire rsp_ready,input wire [31:0] rsp_tag,input wire [255:0] rsp_data,
 output wire out_valid,input wire out_ready,output reg [31:0] out_tag,
 output reg [LANES*32-1:0] out_data,output reg out_error,
 output reg [31:0] sectors,active_lanes,latency_cycles
);
 localparam IDLE=0,ACTIVE=1,OUTPUT=2;
 reg [1:0] state;
 reg [LANES*32-1:0] addresses;
 reg [LANES-1:0] pending,outstanding,issued;
 reg [31:0] lane_sector_tag[0:LANES-1];
 integer leader,i;reg found,bad;reg [31:0] count;
 always @* begin
   leader=0;found=0;bad=0;count=0;
   for(integer j=0;j<LANES;j=j+1)begin
     if(pending[j]&&!found)begin leader=j;found=1;end
     if(lane_mask[j])begin count=count+1;if(lane_addr[j*32+:2]!=0)bad=1;end
   end
 end
 assign warp_ready=(state==IDLE);
 assign req_valid=(state==ACTIVE&&found);
 assign req_addr={addresses[leader*32+5+:27],5'b0};assign req_tag=leader;
 assign rsp_ready=(state==ACTIVE&&rsp_tag<LANES&&outstanding[rsp_tag]);
 assign out_valid=(state==OUTPUT);
 always @(posedge clk)begin
   if(reset)begin
     state<=IDLE;addresses<=0;pending<=0;outstanding<=0;issued<=0;
     out_tag<=0;out_data<=0;out_error<=0;sectors<=0;active_lanes<=0;latency_cycles<=0;
     for(i=0;i<LANES;i=i+1)lane_sector_tag[i]<=0;
   end else begin
     if(warp_valid&&warp_ready)begin
       addresses<=lane_addr;pending<=bad?{LANES{1'b0}}:lane_mask;outstanding<=0;issued<=0;
       out_tag<=warp_tag;out_data<=0;out_error<=bad;sectors<=0;active_lanes<=count;latency_cycles<=0;
       state<=(bad||lane_mask==0)?OUTPUT:ACTIVE;
     end
     if(state==ACTIVE)begin
       latency_cycles<=latency_cycles+1;
       if(req_valid&&req_ready)begin
         outstanding[leader]<=1;sectors<=sectors+1;
         for(i=0;i<LANES;i=i+1)if(pending[i]&&addresses[i*32+5+:27]==req_addr[31:5])begin
           pending[i]<=0;issued[i]<=1;lane_sector_tag[i]<=leader;
         end
       end
       if(rsp_valid&&rsp_ready)begin
         outstanding[rsp_tag]<=0;
         for(i=0;i<LANES;i=i+1)if(issued[i]&&lane_sector_tag[i]==rsp_tag)
           out_data[i*32+:32]<=rsp_data[addresses[i*32+2+:3]*32+:32];
       end
       if(pending==0&&outstanding==0)state<=OUTPUT;
     end
     if(out_valid&&out_ready)state<=IDLE;
   end
 end
endmodule
