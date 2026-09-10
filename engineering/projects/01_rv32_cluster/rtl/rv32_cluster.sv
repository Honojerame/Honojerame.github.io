// A grant is locked until the shared memory completes the transaction.
module rv32_cluster #(parameter integer CORES=4)(
 input wire clk,reset,
 output wire [CORES*32-1:0] imem_addr,input wire [CORES*32-1:0] imem_rdata,
 output wire mem_valid,output wire [31:0] mem_addr,mem_wdata,
 output wire [3:0] mem_wstrb,input wire mem_ready,input wire [31:0] mem_rdata,
 output wire [CORES-1:0] halted,trace_valid,trace_trap,
 output wire [CORES*32-1:0] trace_pc,trace_insn,trace_value,
 output wire [CORES*5-1:0] trace_rd,output wire [CORES*4-1:0] trace_cause,
 output wire [CORES*32-1:0] cycles,retired,memory_stalls,load_stalls,redirects
);
 wire [CORES-1:0] valid; wire [CORES*32-1:0] addr,data; wire [CORES*4-1:0] strb;
 reg locked; integer owner,rr,grant,j,idx; reg found;
 always @* begin
   grant=owner;found=locked;idx=0;
   if(!locked)begin
     grant=rr;
     for(j=0;j<CORES;j=j+1)begin
       idx=rr+j; if(idx>=CORES)idx=idx-CORES;
       if(!found&&valid[idx])begin grant=idx;found=1;end
     end
   end
 end
 assign mem_valid=found&&valid[grant];
 assign mem_addr=addr[grant*32+:32]; assign mem_wdata=data[grant*32+:32];assign mem_wstrb=strb[grant*4+:4];
 always @(posedge clk)begin
   if(reset)begin locked<=0;owner<=0;rr<=0;end
   else if(mem_valid)begin
     if(mem_ready)begin locked<=0;rr<=(grant==CORES-1)?0:grant+1;end
     else begin locked<=1;owner<=grant;end
   end
 end
 genvar c;
 generate for(c=0;c<CORES;c=c+1)begin:core
   rv32_core #(.HART_ID(c)) cpu(
    .clk(clk),.reset(reset),.imem_addr(imem_addr[c*32+:32]),.imem_rdata(imem_rdata[c*32+:32]),
    .mem_valid(valid[c]),.mem_addr(addr[c*32+:32]),.mem_wdata(data[c*32+:32]),.mem_wstrb(strb[c*4+:4]),
    .mem_ready(mem_ready&&mem_valid&&grant==c),.mem_rdata(mem_rdata),.halted(halted[c]),
    .trace_valid(trace_valid[c]),.trace_pc(trace_pc[c*32+:32]),.trace_insn(trace_insn[c*32+:32]),
    .trace_value(trace_value[c*32+:32]),.trace_rd(trace_rd[c*5+:5]),.trace_trap(trace_trap[c]),.trace_cause(trace_cause[c*4+:4]),
    .cycles(cycles[c*32+:32]),.retired(retired[c*32+:32]),.memory_stalls(memory_stalls[c*32+:32]),
    .load_stalls(load_stalls[c*32+:32]),.redirects(redirects[c*32+:32]));
 end endgenerate
endmodule
