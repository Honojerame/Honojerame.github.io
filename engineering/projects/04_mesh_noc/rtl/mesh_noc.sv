module mesh_noc #(parameter integer NX=2,NY=2,DEPTH=4)(
 input wire clk,reset,
 input wire [NX*NY-1:0] inject_valid,output wire [NX*NY-1:0] inject_ready,input wire [NX*NY*64-1:0] inject_data,
 output wire [NX*NY-1:0] eject_valid,input wire [NX*NY-1:0] eject_ready,output wire [NX*NY*64-1:0] eject_data
);
 wire [4:0] iv[0:NX*NY-1],ir[0:NX*NY-1],ov[0:NX*NY-1],orr[0:NX*NY-1];
 wire [319:0] id[0:NX*NY-1],od[0:NX*NY-1];
 genvar x,y;
 generate for(y=0;y<NY;y=y+1)begin:row
  for(x=0;x<NX;x=x+1)begin:col
   localparam T=y*NX+x;
   assign iv[T][0]=inject_valid[T];assign inject_ready[T]=ir[T][0];assign id[T][0+:64]=inject_data[T*64+:64];
   assign eject_valid[T]=ov[T][0];assign orr[T][0]=eject_ready[T];assign eject_data[T*64+:64]=od[T][0+:64];
   if(y>0)begin:north
     assign iv[T][1]=ov[T-NX][3];assign id[T][64+:64]=od[T-NX][192+:64];assign orr[T][1]=ir[T-NX][3];
   end else begin:north_boundary assign iv[T][1]=0;assign id[T][64+:64]=0;assign orr[T][1]=0;end
   if(x<NX-1)begin:east
     assign iv[T][2]=ov[T+1][4];assign id[T][128+:64]=od[T+1][256+:64];assign orr[T][2]=ir[T+1][4];
   end else begin:east_boundary assign iv[T][2]=0;assign id[T][128+:64]=0;assign orr[T][2]=0;end
   if(y<NY-1)begin:south
     assign iv[T][3]=ov[T+NX][1];assign id[T][192+:64]=od[T+NX][64+:64];assign orr[T][3]=ir[T+NX][1];
   end else begin:south_boundary assign iv[T][3]=0;assign id[T][192+:64]=0;assign orr[T][3]=0;end
   if(x>0)begin:west
     assign iv[T][4]=ov[T-1][2];assign id[T][256+:64]=od[T-1][128+:64];assign orr[T][4]=ir[T-1][2];
   end else begin:west_boundary assign iv[T][4]=0;assign id[T][256+:64]=0;assign orr[T][4]=0;end
   xy_router #(.X(x),.Y(y),.DEPTH(DEPTH)) router(clk,reset,iv[T],ir[T],id[T],ov[T],orr[T],od[T]);
  end
 end endgenerate
endmodule
