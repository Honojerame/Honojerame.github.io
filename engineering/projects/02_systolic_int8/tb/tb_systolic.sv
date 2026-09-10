`timescale 1ns/1ps
module tb_systolic;
 parameter N=4,K_MAX=16;
 reg clk=0,reset=1;always #5 clk=~clk;
 reg cv=0,cb=0,sv=0,ordy=0;wire cr,sr,ov,last,done,error;
 reg [31:0] ci=0,kk=1,rr=N,cc=N;reg [7:0] cd=0;
 wire [31:0] oi,od,cycles,stalls,macs;
 systolic_tile #(.N(N),.K_MAX(K_MAX)) dut(clk,reset,cv,cr,cb,ci,cd,sv,sr,kk,rr,cc,ov,ordy,oi,od,last,done,error,cycles,stalls,macs);
 reg [7:0] vectors[0:2*N*K_MAX-1];string infile,outfile;integer seed=1,tmp,i,fd,received=0,clocks=0;
 reg waiting=0;reg [64:0] held;
 initial begin
   if($test$plusargs("VCD"))begin $dumpfile("tb_systolic.vcd");$dumpvars(0,tb_systolic);end
   if(!$value$plusargs("INPUT=%s",infile))$fatal(1,"INPUT");
   if(!$value$plusargs("OUTPUT=%s",outfile))$fatal(1,"OUTPUT");
   if($value$plusargs("SEED=%d",seed))begin end
   tmp=$urandom(seed);$readmemh(infile,vectors);fd=$fopen(outfile,"w");
   repeat(3)@(negedge clk);reset=0;
   // Invalid descriptor must report an error without entering RUN.
   kk=0;sv=1;@(negedge clk);sv=0;if(!error||!sr)$fatal(1,"descriptor rejection");
   for(i=0;i<2*N*K_MAX;i=i+1)begin
     repeat($urandom%3)@(negedge clk);
     cv=1;cb=(i>=N*K_MAX);ci=i%(N*K_MAX);cd=vectors[i];
     @(negedge clk);if(!cr)$fatal(1,"preload unexpectedly blocked");cv=0;
   end
   if(!$value$plusargs("K=%d",kk))$fatal(1,"K");
   if(!$value$plusargs("ROWS=%d",rr))$fatal(1,"ROWS");
   if(!$value$plusargs("COLS=%d",cc))$fatal(1,"COLS");
   sv=1;@(negedge clk);sv=0;
 end
 always @(negedge clk)if(!reset)ordy=($urandom%4==0);
 always @(posedge clk)if(!reset)begin
   clocks=clocks+1;if(clocks>20000)$fatal(1,"timeout");
   if(waiting&&(!ov||{oi,od,last}!==held))$fatal(1,"unstable output");
   waiting=ov&&!ordy;held={oi,od,last};
   if(ov&&ordy)begin
     if(oi!=received||last!=(received==N*N-1))$fatal(1,"index/last mismatch");
     $fdisplay(fd,"%0d %0d",oi,$signed(od));received=received+1;
   end
   if(done)begin
     if(received!=N*N)$fatal(1,"wrong output count");
     $display("METRIC n=%0d k=%0d rows=%0d cols=%0d compute_cycles=%0d output_stalls=%0d useful_macs=%0d",N,kk,rr,cc,cycles,stalls,macs);
     $fclose(fd);$display("PASS systolic");$finish;
   end
 end
endmodule
