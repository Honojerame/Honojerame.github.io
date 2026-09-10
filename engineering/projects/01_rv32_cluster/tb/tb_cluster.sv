`timescale 1ns/1ps
module tb_cluster;
 parameter CORES=4;
 reg clk=0,reset=1; always #5 clk=~clk;
 wire [CORES*32-1:0] ia; reg [CORES*32-1:0] ir;
 wire valid;wire [31:0] addr,data;wire [3:0] strb;
 reg ready=0;wire [31:0] rdata;wire [CORES-1:0] halted,tv,tt;
 wire [CORES*32-1:0] tp,ti,td,cycles,retired,ms,ls,redirects;
 wire [CORES*5-1:0] tr;wire [CORES*4-1:0] tc;
 reg [31:0] rom[0:2047],ram[0:1023];
 string program_file,trace_file,memory_file;integer fd,i,c,n=0,seed=1,random_value,wait_mask=3;
 reg was_waiting=0;reg [67:0] held;
 rv32_cluster #(.CORES(CORES)) dut(clk,reset,ia,ir,valid,addr,data,strb,ready,rdata,halted,tv,tt,tp,ti,td,tr,tc,cycles,retired,ms,ls,redirects);
 always @* begin
   for(integer k=0;k<CORES;k=k+1)ir[k*32+:32]=(ia[k*32+:32]<8192)?rom[ia[k*32+:32]>>2]:32'h00000073;
 end
 assign rdata=ram[addr[11:2]];
 initial begin
   if(!$value$plusargs("PROGRAM=%s",program_file))$fatal(1,"missing PROGRAM");
   if(!$value$plusargs("TRACE=%s",trace_file))$fatal(1,"missing TRACE");
   if(!$value$plusargs("MEMORY=%s",memory_file))$fatal(1,"missing MEMORY");
   if($value$plusargs("SEED=%d",seed))begin end
   if($value$plusargs("WAIT_MASK=%d",wait_mask))begin end
   random_value=$urandom(seed);
   for(i=0;i<2048;i=i+1)rom[i]=32'h00000073;
   for(i=0;i<1024;i=i+1)ram[i]=32'h10203040+i;
   $readmemh(program_file,rom);fd=$fopen(trace_file,"w");
   if($test$plusargs("VCD"))begin $dumpfile("cluster.vcd");$dumpvars(0,tb_cluster);end
   repeat(4)@(negedge clk);reset=0;
 end
 always @(negedge clk)if(!reset)ready=(($urandom&wait_mask)==0);
 always @(posedge clk)if(!reset)begin
   n=n+1;if(n>200000)$fatal(1,"cluster timeout");
   if(was_waiting&&(!valid||{addr,data,strb}!==held))$fatal(1,"unstable shared request");
   was_waiting=valid&&!ready;held={addr,data,strb};
   if(valid&&addr>=4096)$fatal(1,"out of range data address %h",addr);
   if(valid&&ready)for(i=0;i<4;i=i+1)if(strb[i])ram[addr[11:2]][i*8+:8]<=data[i*8+:8];
   for(c=0;c<CORES;c=c+1)if(tv[c])$fdisplay(fd,"%0d %08x %08x %0d %08x %0d %0d",c,tp[c*32+:32],ti[c*32+:32],tr[c*5+:5],td[c*32+:32],tt[c],tc[c*4+:4]);
   if(&halted)begin
     for(c=0;c<CORES;c=c+1)$display("METRIC core=%0d cycles=%0d retired=%0d memory_stalls=%0d load_stalls=%0d redirects=%0d",c,cycles[c*32+:32],retired[c*32+:32],ms[c*32+:32],ls[c*32+:32],redirects[c*32+:32]);
     $writememh(memory_file,ram);$fclose(fd);$display("PASS cluster cores=%0d cycles=%0d",CORES,n);$finish;
   end
 end
endmodule
