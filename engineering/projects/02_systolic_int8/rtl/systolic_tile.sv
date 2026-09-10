module systolic_tile #(parameter integer N=4,K_MAX=16)(
 input wire clk,reset,
 input wire cfg_valid,output wire cfg_ready,input wire cfg_is_b,
 input wire [31:0] cfg_index,input wire [7:0] cfg_data,
 input wire start_valid,output wire start_ready,
 input wire [31:0] start_k,start_rows,start_cols,
 output wire out_valid,input wire out_ready,output wire [31:0] out_index,
 output wire signed [31:0] out_data,output wire out_last,
 output reg done,error,output reg [31:0] compute_cycles,output_stalls,useful_macs
);
 localparam IDLE=0,RUN=1,DRAIN=2;
 reg [1:0] state;reg [31:0] tick,k_count,rows,cols,result_index;
 reg signed [7:0] a_mem[0:N*K_MAX-1],b_mem[0:N*K_MAX-1];
 wire signed [7:0] a_pipe[0:N*N-1],b_pipe[0:N*N-1];
 wire signed [31:0] accum[0:N*N-1];
 wire descriptor_ok=(start_k>0&&start_k<=K_MAX&&start_rows>0&&start_rows<=N&&start_cols>0&&start_cols<=N);
 assign cfg_ready=(state==IDLE&&cfg_index<N*K_MAX);
 assign start_ready=(state==IDLE&&!cfg_valid);
 wire clear=start_valid&&start_ready&&descriptor_ok;
 assign out_valid=(state==DRAIN);assign out_index=result_index;
 assign out_data=accum[result_index];assign out_last=(result_index==N*N-1);
 genvar r,c;
 generate for(r=0;r<N;r=r+1)begin:row
   for(c=0;c<N;c=c+1)begin:col
     wire signed [7:0] ai,bi;
     if(c==0)begin:a_edge assign ai=(state==RUN&&r<rows&&tick>=r&&tick<k_count+r)?a_mem[r*K_MAX+tick-r]:8'sd0; end
     else begin:a_link assign ai=a_pipe[r*N+c-1];end
     if(r==0)begin:b_edge assign bi=(state==RUN&&c<cols&&tick>=c&&tick<k_count+c)?b_mem[(tick-c)*N+c]:8'sd0;end
     else begin:b_link assign bi=b_pipe[(r-1)*N+c];end
     mac_pe pe(clk,reset,clear,state==RUN,ai,bi,a_pipe[r*N+c],b_pipe[r*N+c],accum[r*N+c]);
   end
 end endgenerate
 always @(posedge clk)begin
   if(reset)begin state<=IDLE;tick<=0;k_count<=0;rows<=0;cols<=0;result_index<=0;done<=0;error<=0;compute_cycles<=0;output_stalls<=0;useful_macs<=0;end
   else begin
     done<=0;error<=0;
     if(cfg_valid&&cfg_ready)begin
       if(cfg_is_b)b_mem[cfg_index]<=cfg_data;else a_mem[cfg_index]<=cfg_data;
     end
     if(start_valid&&start_ready)begin
       if(!descriptor_ok)error<=1;
       else begin
         state<=RUN;k_count<=start_k;rows<=start_rows;cols<=start_cols;tick<=0;
         compute_cycles<=0;output_stalls<=0;useful_macs<=start_rows*start_cols*start_k;result_index<=0;
       end
     end
     if(state==RUN)begin
       compute_cycles<=compute_cycles+1;tick<=tick+1;
       if(tick==k_count+2*N-3)state<=DRAIN;
     end
     if(state==DRAIN)begin
       if(!out_ready)output_stalls<=output_stalls+1;
       else if(out_last)begin state<=IDLE;done<=1;end
       else result_index<=result_index+1;
     end
   end
 end
endmodule
