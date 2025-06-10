module top (
    input wire clk,
    input wire [23:0] io_in,
    output wire [23:0] io_out,
    io_oeb
);

    localparam COUNTER_WIDTH = 24;
    localparam PRESCALE_WIDTH = 16;
    localparam PRESCALE_LIMIT = 10;

    // WARNING: Don't change these values for MPW5!
    localparam OUTPUT_ENABLE = 1'b1;
    localparam OUTPUT_DISABLE = 1'b0;

    wire rst;
    wire use_prescaler;
    reg [COUNTER_WIDTH-1:0] ctr;
    reg [PRESCALE_WIDTH-1:0] prescale;

    always @(posedge clk) begin
        if (rst) ctr <= 0;
        else begin
            if (use_prescaler) begin
                if (prescale == PRESCALE_LIMIT) ctr <= ctr + 1'b1;
            end else begin
                ctr <= ctr + 1'b1;
            end
        end
    end

    always @(posedge clk) begin
        if (rst) prescale <= 0;
        else begin
            if (prescale == PRESCALE_LIMIT) prescale <= 0;
            else prescale <= prescale + 1'b1;
        end
    end

    // Inputs

    assign io_oeb[23:22] = {2{OUTPUT_DISABLE}};
    assign rst = io_in[23];
    assign use_prescaler = io_in[22];

    // Outputs

    // Route the reset through for debugging
    assign io_out[21] = rst;
    assign io_out[20:6] = ctr[22:8];
    // Don't use high frequency signals for easier
    // observability
    assign io_out[5:0] = ctr[23:18];
    assign io_oeb[21:0] = {22{OUTPUT_ENABLE}};
endmodule
