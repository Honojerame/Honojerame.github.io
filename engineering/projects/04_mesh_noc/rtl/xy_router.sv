// Port order: local, north, east, south, west. Destination: x[7:0], y[15:8].
module xy_router #(parameter integer X=0,Y=0,DEPTH=4)(
 input wire clk,reset,input wire [4:0] in_valid,output wire [4:0] in_ready,input wire [319:0] in_data,
 output reg [4:0] out_valid,input wire [4:0] out_ready,output reg [319:0] out_data
);
 wire [4:0] fv;reg [4:0] fr;wire [319:0] fd;
 reg [4:0] locked;integer rr[0:4],owner[0:4],grant[0:4],route[0:4];
 integer p,j,idx;reg found;
 genvar g;generate for(g=0;g<5;g=g+1)begin:input_queue
   rv_fifo #(.WIDTH(64),.DEPTH(DEPTH)) fifo(clk,reset,in_valid[g],in_ready[g],in_data[g*64+:64],fv[g],fr[g],fd[g*64+:64]);
 end endgenerate
 always @* begin
   for(integer q=0;q<5;q=q+1)begin
     if(fd[q*64+:8]>X)route[q]=2;else if(fd[q*64+:8]<X)route[q]=4;
     else if(fd[q*64+8+:8]>Y)route[q]=3;else if(fd[q*64+8+:8]<Y)route[q]=1;else route[q]=0;
   end
   fr=0;out_valid=0;out_data=0;found=0;idx=0;
   for(p=0;p<5;p=p+1)begin
     grant[p]=owner[p];found=locked[p];
     if(!locked[p])begin
       grant[p]=rr[p];
       for(j=0;j<5;j=j+1)begin
         idx=rr[p]+j;if(idx>=5)idx=idx-5;
         if(!found&&fv[idx]&&route[idx]==p)begin grant[p]=idx;found=1;end
       end
     end
     if(found)begin
       out_valid[p]=fv[grant[p]];out_data[p*64+:64]=fd[grant[p]*64+:64];
       if(out_ready[p])fr[grant[p]]=1;
     end
   end
 end
 always @(posedge clk)begin
   if(reset)begin locked<=0;for(integer k=0;k<5;k=k+1)begin rr[k]<=0;owner[k]<=0;end end
   else for(integer k=0;k<5;k=k+1)if(out_valid[k])begin
     if(out_ready[k])begin locked[k]<=0;rr[k]<=(grant[k]==4)?0:grant[k]+1;end
     else begin locked[k]<=1;owner[k]<=grant[k];end
   end
 end
endmodule
