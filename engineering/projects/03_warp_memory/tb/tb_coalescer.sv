`timescale 1ns/1ps
module tb_coalescer;
 parameter LANES=32;
 reg clk=0,reset=1;always #5 clk=~clk;
 reg wv=0,qr=0,rv=0,orr=0;wire wr,qv,rr,ov,err;
 reg [31:0] wt=0,rt=0;reg [LANES-1:0] mask=0;reg [LANES*32-1:0] addresses=0;
 wire [31:0] qa,qt,ot,sectors,active,latency;reg [255:0] rd=0;wire [LANES*32-1:0] od;
 warp_coalescer #(.LANES(LANES)) dut(clk,reset,wv,wr,wt,mask,addresses,qv,qr,qa,qt,rv,rr,rt,rd,ov,orr,ot,od,err,sectors,active,latency);
 reg pool[0:LANES-1];reg [31:0] pa[0:LANES-1];integer delay_left[0:LANES-1],issue_order[0:LANES-1];integer reordered=0;
 reg req_wait=0,out_wait=0,rsp_consumed=0;reg [31:0] scan_address;reg [63:0] held_req;reg [LANES*32-1:0] held_out;
 string infile,outfile;integer fi,fo,tmp,seed=1,count,case_id=0,i,j,n=0,pick,start,requests=0,answers=0,highest_outstanding=0,inflight=0;
 function [31:0] memory_word(input [31:0] address);memory_word=32'h9e3779b9^((address>>2)*32'h01010101);endfunction
 initial begin
   if($test$plusargs("VCD"))begin $dumpfile("tb_coalescer.vcd");$dumpvars(0,tb_coalescer);end
   for(i=0;i<LANES;i=i+1)begin pool[i]=0;pa[i]=0;delay_left[i]=0;end
   if(!$value$plusargs("INPUT=%s",infile))$fatal(1,"INPUT");if(!$value$plusargs("OUTPUT=%s",outfile))$fatal(1,"OUTPUT");
   if($value$plusargs("SEED=%d",seed))begin end
   tmp=$urandom(seed);fi=$fopen(infile,"r");fo=$fopen(outfile,"w");tmp=$fscanf(fi,"%d",count);
   repeat(3)@(negedge clk);reset=0;
   for(case_id=0;case_id<count;case_id=case_id+1)begin
     while(!wr)@(negedge clk);
     tmp=$fscanf(fi,"%h",mask);for(j=0;j<LANES;j=j+1)begin tmp=$fscanf(fi,"%h",scan_address);addresses[j*32+:32]=scan_address;end
     wt=case_id;wv=1;@(negedge clk);wv=0;
     while(!wr)@(negedge clk);
   end
   $fclose(fi);$fclose(fo);$display("METRIC cases=%0d requests=%0d responses=%0d max_outstanding=%0d reordered=%0d",count,requests,answers,highest_outstanding,reordered);$display("PASS coalescer");$finish;
 end
 always @(negedge clk)if(!reset)begin
   qr=($urandom%3!=0);orr=($urandom%4==0);
   if(!rv||rsp_consumed)begin
     rv=0;pick=-1;start=$urandom%LANES;
     for(integer k=0;k<LANES;k=k+1)begin
       integer idx;idx=(start+k)%LANES;
       if(pool[idx]&&delay_left[idx]==0&&pick==-1)pick=idx;
     end
     if(pick!=-1)begin
       rv=1;rt=pick;for(integer k=0;k<8;k=k+1)rd[k*32+:32]=memory_word(pa[pick]+k*4);
     end
   end
 end
 always @(posedge clk)if(!reset)begin
   rsp_consumed=rv&&rr;
   n=n+1;if(n>200000)$fatal(1,"timeout");
   if(req_wait&&(!qv||{qa,qt}!==held_req))$fatal(1,"request changed under backpressure");
   if(out_wait&&(!ov||od!==held_out))$fatal(1,"output changed under backpressure");
   req_wait=qv&&!qr;held_req={qa,qt};out_wait=ov&&!orr;held_out=od;
   for(i=0;i<LANES;i=i+1)if(pool[i]&&delay_left[i]>0)delay_left[i]=delay_left[i]-1;
   if(rv&&rr)begin if(!pool[rt])$fatal(1,"unknown response");for(integer k=0;k<LANES;k=k+1)if(pool[k]&&issue_order[k]<issue_order[rt])reordered=reordered+1; pool[rt]=0;answers=answers+1;inflight=inflight-1;end
   if(qv&&qr)begin
     if(qt>=LANES||pool[qt]||qa[4:0]!=0)$fatal(1,"invalid request");
     pool[qt]=1;issue_order[qt]=requests;pa[qt]=qa;delay_left[qt]=4+$urandom%20;requests=requests+1;inflight=inflight+1;
     if(inflight>highest_outstanding)highest_outstanding=inflight;
   end
   if(ov&&orr)begin
     $fwrite(fo,"%0d %0d %0d %0d %0d",ot,err,sectors,active,latency);
     for(i=0;i<LANES;i=i+1)$fwrite(fo," %08x",od[i*32+:32]);$fwrite(fo,"\n");
   end
 end
endmodule
