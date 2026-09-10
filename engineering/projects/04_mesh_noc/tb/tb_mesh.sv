`timescale 1ns/1ps
module tb_mesh;
 parameter NX=2,NY=2,DEPTH=4,PACKETS=120;localparam N=NX*NY;
 reg clk=0,reset=1;always #5 clk=~clk;
 reg [N-1:0] iv=0,orr=0;wire [N-1:0] ir,ov;reg [N*64-1:0] id=0;wire [N*64-1:0] od;
 mesh_noc #(.NX(NX),.NY(NY),.DEPTH(DEPTH)) dut(clk,reset,iv,ir,id,ov,orr,od);
 integer sent[0:N-1],injection_time[0:N*PACKETS-1];reg seen[0:N*PACKETS-1];reg [63:0] expected[0:N*PACKETS-1];
 reg [N-1:0] consumed=0,waiting=0;reg [N*64-1:0] held=0;
 integer cycle=0,received=0,total_latency=0,max_latency=0,seed=1,tmp,pattern=0,rate=60,sink_rate=70;
 integer dest,seq,src,key,lat;reg [63:0] packet;
 string outfile;integer fo;
 initial begin
   if($test$plusargs("VCD"))begin $dumpfile("tb_mesh.vcd");$dumpvars(0,tb_mesh);end
   if($value$plusargs("SEED=%d",seed))begin end
   if($value$plusargs("PATTERN=%d",pattern))begin end
   if($value$plusargs("RATE=%d",rate))begin end
   if($value$plusargs("SINK_RATE=%d",sink_rate))begin end
   if(!$value$plusargs("OUTPUT=%s",outfile))$fatal(1,"OUTPUT");
   tmp=$urandom(seed);fo=$fopen(outfile,"w");
   for(integer i=0;i<N;i=i+1)sent[i]=0;
   for(integer i=0;i<N*PACKETS;i=i+1)begin seen[i]=0;injection_time[i]=-1;expected[i]=0;end
   repeat(4)@(negedge clk);reset=0;
 end
 always @(negedge clk)if(!reset)begin
   for(integer node=0;node<N;node=node+1)begin
     // Force sink progress at least once every eight cycles.
     orr[node]=(cycle%8==0)||($urandom%100<sink_rate);
     if(consumed[node])iv[node]=0;
     if(!iv[node]&&sent[node]<PACKETS&&$urandom%100<rate)begin
       case(pattern)
         0:dest=$urandom%N;
         1:dest=N-1-node;
         2:dest=0;
         default:dest=(node+1)%N;
       endcase
       packet=0;packet[7:0]=dest%NX;packet[15:8]=dest/NX;
       packet[23:16]=node;packet[39:24]=sent[node];packet[63:40]=$urandom;
       id[node*64+:64]=packet;iv[node]=1;
     end
   end
 end
 always @(posedge clk)if(!reset)begin
   cycle=cycle+1;consumed=iv&ir;
   if(cycle>150000)$fatal(1,"mesh failed to drain received=%0d",received);
   for(integer node=0;node<N;node=node+1)begin
     if(waiting[node]&&(!ov[node]||od[node*64+:64]!==held[node*64+:64]))$fatal(1,"unstable ejection");
     if(iv[node]&&ir[node])begin
       key=node*PACKETS+sent[node];injection_time[key]=cycle;expected[key]=id[node*64+:64];sent[node]=sent[node]+1;
     end
     if(ov[node]&&orr[node])begin
       packet=od[node*64+:64];src=packet[23:16];seq=packet[39:24];key=src*PACKETS+seq;
       if(src>=N||seq>=PACKETS||packet[7:0]!=node%NX||packet[15:8]!=node/NX)$fatal(1,"misroute/invalid identity");
       if(seen[key]||injection_time[key]<0||packet!==expected[key])$fatal(1,"duplicate, corruption, or phantom packet");
       seen[key]=1;lat=cycle-injection_time[key];total_latency=total_latency+lat;if(lat>max_latency)max_latency=lat;
       received=received+1;$fdisplay(fo,"%0d %0d %0d %0d",src,seq,node,lat);
     end
   end
   waiting=ov&~orr;held=od;
   if(received==N*PACKETS)begin
     for(integer i=0;i<N*PACKETS;i=i+1)if(!seen[i])$fatal(1,"missing packet");
     $display("METRIC nx=%0d ny=%0d depth=%0d pattern=%0d rate=%0d sink_rate=%0d packets=%0d cycles=%0d total_latency=%0d max_latency=%0d",NX,NY,DEPTH,pattern,rate,sink_rate,received,cycle,total_latency,max_latency);
     $fclose(fo);$display("PASS mesh");$finish;
   end
 end
endmodule
