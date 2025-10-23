#include 
#include 

// Buffer descriptors (comments explain purpose).
typedef struct {
    void* addr;       // pointer to buffer memory
    size_t len;       // length in bytes
    volatile int in_use; // flag set by DMA/hardware
} buf_desc_t;

// Submit next buffer to DMA (pseudo-call to platform DMA API).
void submit_to_dma(buf_desc_t* desc) {
    // Platform-specific DMA submit; ensure alignment and burst-friendly size.
    dma_submit(desc->addr, desc->len); // comment: platform DMA
    desc->in_use = 1; // mark busy
}

// Poll DMA completion and flip buffers (polling for simplicity).
void process_double_buffer(buf_desc_t* a, buf_desc_t* b) {
    if (!a->in_use) submit_to_dma(a);
    if (!b->in_use) submit_to_dma(b);
    // ... processing loop where CPU/FPGA manipulates the buffer not in use.
}