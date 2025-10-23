typedef struct {
    uint64_t phys_addr;   // physical address of buffer (set by driver)
    uint32_t length;      // bytes to transfer
    uint32_t control;     // flags: end_of_chain, interrupt_on_complete
} dma_desc_t;

// Setup descriptors for N buffers (ping-pong or ring)
for (int i = 0; i < N; ++i) {
    desc[i].phys_addr = buf_phys[i];      // CPU maps buffer and gives physical addr
    desc[i].length    = buf_size_bytes;   // must be aligned to bus burst size
    desc[i].control   = (i == N-1) ? EOC_FLAG : 0; // mark last descriptor
    // minimal CPU overhead; hardware DMA will chain them
}
// Kick the DMA engine; hardware will write incoming samples into buffers.
// ISR or polling handles completion and hands buffers to FPGA/DSP for replay.