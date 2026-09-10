`timescale 1ns/1ps
module tb_scratchpad;
 parameter LANES=32,BANKS=8,WORDS=256;
 reg clk=0,reset=1;always #5 clk=~clk;
 reg iv=0,store=0,orr=0;wire ir,ov,err;reg [LANES-1:0] mask=0;
 reg [LANES*32-1:0] addresses=0,values=0;wire [LANES*32-1:0] data;wire [31:0] cycles;
 banked_scratchpad #(.LANES(LANES),.BANKS(BANKS),.WORDS(WORDS)) dut(clk,reset,iv,ir,store,mask,addresses,values,ov,orr,data,err,cycles);
 string infile,outfile;integer fi,fo,tmp,count,op,i,n=0,seed=1;
 reg [31:0] scan_address,scan_value;reg waited=0;reg [LANES*32-1:0] held;
 initial begin
   if($test$plusargs("VCD"))begin $dumpfile("tb_scratchpad.vcd");$dumpvars(0,tb_scratchpad);end
   if(!$value$plusargs("INPUT=%s",infile))$fatal(1,"INPUT");if(!$value$plusargs("OUTPUT=%s",outfile))$fatal(1,"OUTPUT");
   if($value$plusargs("SEED=%d",seed))begin end
   tmp=$urandom(seed);fi=$fopen(infile,"r");fo=$fopen(outfile,"w");tmp=$fscanf(fi,"%d",count);
   repeat(3)@(negedge clk);reset=0;
   for(op=0;op<count;op=op+1)begin
     while(!ir)@(negedge clk);
     tmp=$fscanf(fi,"%d %h",store,mask);
     for(i=0;i<LANES;i=i+1)begin tmp=$fscanf(fi,"%h %h",scan_address,scan_value);addresses[i*32+:32]=scan_address;values[i*32+:32]=scan_value;end
     iv=1;@(negedge clk);iv=0;while(!ir)@(negedge clk);
   end
   $fclose(fi);$fclose(fo);$display("PASS scratchpad operations=%0d",count);$finish;
 end
 always @(negedge clk)if(!reset)orr=($urandom%4==0);
 always @(posedge clk)if(!reset)begin
   n=n+1;if(n>200000)$fatal(1,"timeout");
   if(waited&&(!ov||data!==held))$fatal(1,"unstable scratchpad response");
   waited=ov&&!orr;held=data;
   if(ov&&orr)begin
     $fwrite(fo,"%0d %0d",err,cycles);for(integer k=0;k<LANES;k=k+1)$fwrite(fo," %08x",data[k*32+:32]);$fwrite(fo,"\n");
   end
 end
endmodule
