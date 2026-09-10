// Five-stage, in-order RV32I integer core. See docs/architecture.md for contracts.
module rv32_core #(parameter integer HART_ID=0)(
 input wire clk, reset,
 output wire [31:0] imem_addr, input wire [31:0] imem_rdata,
 output wire mem_valid, output wire [31:0] mem_addr, mem_wdata,
 output wire [3:0] mem_wstrb, input wire mem_ready, input wire [31:0] mem_rdata,
 output reg halted,
 output wire trace_valid, output wire [31:0] trace_pc, trace_insn, trace_value,
 output wire [4:0] trace_rd, output wire trace_trap, output wire [3:0] trace_cause,
 output reg [31:0] cycles, retired, memory_stalls, load_stalls, redirects
);
 reg [31:0] regs[0:31];
 reg [31:0] pc, d_pc,d_insn,x_pc,x_insn,x_a,x_b;
 reg d_valid,x_valid,stop_fetch;
 reg m_valid,m_load,m_store,m_we,m_trap;
 reg [31:0] m_pc,m_insn,m_value,m_addr,m_data;
 reg [4:0] m_rd; reg [2:0] m_size; reg [3:0] m_mask,m_cause;
 reg w_valid,w_we,w_trap; reg [31:0] w_pc,w_insn,w_value;
 reg [4:0] w_rd; reg [3:0] w_cause;
 wire [6:0] op=x_insn[6:0]; wire [2:0] f3=x_insn[14:12];
 wire [6:0] f7=x_insn[31:25];
 wire [4:0] rs1=x_insn[19:15],rs2=x_insn[24:20],rd=x_insn[11:7];
 wire [31:0] imm_i={{20{x_insn[31]}},x_insn[31:20]};
 wire [31:0] imm_s={{20{x_insn[31]}},x_insn[31:25],x_insn[11:7]};
 wire [31:0] imm_b={{19{x_insn[31]}},x_insn[31],x_insn[7],x_insn[30:25],x_insn[11:8],1'b0};
 wire [31:0] imm_j={{11{x_insn[31]}},x_insn[31],x_insn[19:12],x_insn[20],x_insn[30:21],1'b0};
 reg [31:0] a,b,alu,addr,store_data,target,rhs,loaded,shifted;
 reg we,ld,st,trap,redirect,take; reg [3:0] mask,cause;
 wire blocked=m_valid&&(m_load||m_store)&&!mem_ready;
 wire [6:0] dop=d_insn[6:0];
 wire uses1=(dop==7'h03||dop==7'h13||dop==7'h23||dop==7'h33||dop==7'h63||dop==7'h67);
 wire uses2=(dop==7'h23||dop==7'h33||dop==7'h63);
 wire hazard=x_valid&&(op==7'h03)&&(rd!=0)&&d_valid&&
   ((uses1&&d_insn[19:15]==rd)||(uses2&&d_insn[24:20]==rd));
 wire [4:0] drs1=d_insn[19:15],drs2=d_insn[24:20];
 wire [31:0] da=drs1==0?0:(w_valid&&w_we&&w_rd==drs1?w_value:regs[drs1]);
 wire [31:0] db=drs2==0?0:(w_valid&&w_we&&w_rd==drs2?w_value:regs[drs2]);
 assign imem_addr=pc;
 assign mem_valid=m_valid&&(m_load||m_store)&&!m_trap;
 assign mem_addr={m_addr[31:2],2'b00};
 assign mem_wdata=m_data; assign mem_wstrb=m_store?m_mask:4'b0;
 assign trace_valid=w_valid; assign trace_pc=w_pc; assign trace_insn=w_insn;
 assign trace_rd=(w_we&&!w_trap)?w_rd:5'b0; assign trace_value=w_value;
 assign trace_trap=w_trap; assign trace_cause=w_cause;
 always @* begin
   a=x_a; b=x_b;
   if(w_valid&&w_we&&w_rd!=0) begin
     if(rs1==w_rd) a=w_value; if(rs2==w_rd) b=w_value;
   end
   if(m_valid&&m_we&&!m_load&&!m_trap&&m_rd!=0) begin
     if(rs1==m_rd) a=m_value; if(rs2==m_rd) b=m_value;
   end
   if(rs1==0) a=0; if(rs2==0) b=0;
   alu=0; addr=0; store_data=0; target=0; rhs=0;
   we=0; ld=0; st=0; trap=0; cause=2; redirect=0; take=0; mask=0;
   case(op)
    7'h37: begin we=1; alu={x_insn[31:12],12'b0}; end
    7'h17: begin we=1; alu=x_pc+{x_insn[31:12],12'b0}; end
    7'h6f: begin we=1; alu=x_pc+4; redirect=1; target=x_pc+imm_j; end
    7'h67: begin we=1; alu=x_pc+4; redirect=1; target=(a+imm_i)&32'hfffffffe; if(f3!=0)trap=1; end
    7'h63: begin
      case(f3)
       0:take=(a==b); 1:take=(a!=b); 4:take=($signed(a)<$signed(b));
       5:take=($signed(a)>=$signed(b)); 6:take=(a<b); 7:take=(a>=b);
       default:trap=1;
      endcase
      redirect=take; target=x_pc+imm_b;
    end
    7'h13,7'h33: begin
      we=1; rhs=(op==7'h13)?imm_i:b;
      case(f3)
       0:begin
         alu=(op==7'h33&&f7==7'h20)?a-rhs:a+rhs;
         if(op==7'h33&&f7!=0&&f7!=7'h20)trap=1;
       end
       1:begin alu=a<<rhs[4:0]; if(f7!=0)trap=1; end
       2:begin alu={31'b0,($signed(a)<$signed(rhs))}; if(op==7'h33&&f7!=0)trap=1; end
       3:begin alu={31'b0,(a<rhs)}; if(op==7'h33&&f7!=0)trap=1; end
       4:begin alu=a^rhs; if(op==7'h33&&f7!=0)trap=1; end
       5:begin
         if(f7==7'h20)alu=$signed(a)>>>rhs[4:0]; else alu=a>>rhs[4:0];
         if(f7!=0&&f7!=7'h20)trap=1;
       end
       6:begin alu=a|rhs; if(op==7'h33&&f7!=0)trap=1; end
       7:begin alu=a&rhs; if(op==7'h33&&f7!=0)trap=1; end
      endcase
    end
    7'h03: begin
      ld=1; we=1; addr=a+imm_i;
      if(f3!=0&&f3!=1&&f3!=2&&f3!=4&&f3!=5)trap=1;
      else if(((f3==1||f3==5)&&addr[0])||(f3==2&&addr[1:0]!=0))begin trap=1;cause=4;end
    end
    7'h23: begin
      st=1; addr=a+imm_s; store_data=b<<(8*addr[1:0]);
      case(f3) 0:mask=4'b0001<<addr[1:0]; 1:mask=4'b0011<<addr[1:0]; 2:mask=15; default:trap=1; endcase
      if((f3==1&&addr[0])||(f3==2&&addr[1:0]!=0))begin trap=1;cause=6;end
    end
    7'h0f: begin if(f3!=0||x_insn[19:15]!=0||rd!=0)trap=1; end
    7'h73: begin trap=1; if(x_insn==32'h00000073)cause=11; else if(x_insn==32'h00100073)cause=3; end
    default:trap=1;
   endcase
   if(redirect&&target[1:0]!=0&&!trap)begin trap=1;cause=0;end
   if(trap)begin we=0;ld=0;st=0;redirect=0;end
   shifted=mem_rdata>>(8*m_addr[1:0]); loaded=shifted;
   case(m_size)
    0:loaded={{24{shifted[7]}},shifted[7:0]}; 1:loaded={{16{shifted[15]}},shifted[15:0]};
    4:loaded={24'b0,shifted[7:0]}; 5:loaded={16'b0,shifted[15:0]}; default:loaded=shifted;
   endcase
 end
 integer i;
 always @(posedge clk) begin
   if(reset)begin
     pc<=0;d_valid<=0;x_valid<=0;m_valid<=0;w_valid<=0;stop_fetch<=0;halted<=0;
     d_pc<=0;d_insn<=0;x_pc<=0;x_insn<=0;x_a<=0;x_b<=0;
     m_load<=0;m_store<=0;m_we<=0;m_trap<=0;m_pc<=0;m_insn<=0;m_value<=0;m_addr<=0;m_data<=0;
     m_rd<=0;m_size<=0;m_mask<=0;m_cause<=0;
     w_we<=0;w_trap<=0;w_pc<=0;w_insn<=0;w_value<=0;w_rd<=0;w_cause<=0;
     cycles<=0;retired<=0;memory_stalls<=0;load_stalls<=0;redirects<=0;
     for(i=0;i<32;i=i+1)regs[i]<=0;
     regs[10]<=HART_ID;
   end else begin
     if(!halted)cycles<=cycles+1;
     if(w_valid)begin
       if(w_we&&w_rd!=0&&!w_trap)regs[w_rd]<=w_value;
       if(w_trap)halted<=1; else retired<=retired+1;
     end
     regs[0]<=0;
     w_valid<=0;
     if(blocked)begin
       memory_stalls<=memory_stalls+1;
       // Retain a forwarding result when WB drains during a memory stall.
       x_a<=a; x_b<=b;
     end else begin
       w_valid<=m_valid; w_pc<=m_pc;w_insn<=m_insn;w_rd<=m_rd;
       w_we<=m_we;w_trap<=m_trap;w_cause<=m_cause;w_value<=m_load?loaded:m_value;
       m_valid<=x_valid;m_pc<=x_pc;m_insn<=x_insn;m_rd<=rd;m_we<=we;
       m_load<=ld;m_store<=st;m_value<=alu;m_addr<=addr;m_data<=store_data;m_mask<=mask;m_size<=f3;
       m_trap<=trap;m_cause<=cause;
       if(x_valid&&(redirect||trap))begin
         x_valid<=0;d_valid<=0;
         if(trap)stop_fetch<=1;
         else begin pc<=target;redirects<=redirects+1;end
       end else if(hazard)begin x_valid<=0;load_stalls<=load_stalls+1;end
       else begin
         x_valid<=d_valid;x_pc<=d_pc;x_insn<=d_insn;x_a<=da;x_b<=db;
         d_valid<=!stop_fetch&&!halted;d_pc<=pc;d_insn<=imem_rdata;
         if(!stop_fetch&&!halted)pc<=pc+4;
       end
     end
   end
 end
endmodule
