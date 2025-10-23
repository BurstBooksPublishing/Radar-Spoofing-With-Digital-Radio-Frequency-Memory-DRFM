volatile int head = 0; // DMA writes here (index), ISR increments
volatile int tail = 0; // DSP reads here
#define BUFSZ 4096
int16_t buffer[BUFSZ]; // sample buffer (signed 16-bit)

void dma_isr(void) { // called when DMA block complete
    // advance head atomically, minimal work
    head = (head + DMA_BLOCK_SIZE) % BUFSZ;
    // signal DSP task (lightweight semaphore)
}

void dsp_task(void) {
    while (running) {
        if (tail != head) {
            // process one block with simple operations
            process_block(&buffer[tail], BLOCK_LEN); // keep fast
            tail = (tail + BLOCK_LEN) % BUFSZ;
        } else {
            wait_for_semaphore(); // low-power wait
        }
    }
}

// process_block should be implemented in optimized code or FPGA.