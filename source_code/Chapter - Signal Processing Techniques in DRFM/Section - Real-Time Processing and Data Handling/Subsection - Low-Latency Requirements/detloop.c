volatile bool buf_ready[2] = {false,false};
int cur = 0;

// ISR or DMA completion callback (runs in deterministic context)
void dma_callback(int buf_idx) {
    buf_ready[buf_idx] = true; // signal processing thread
}

// Processing thread (real-time priority)
while (system_running) {
    int proc_idx = cur ^ 1; // process the buffer not currently being filled
    if (!buf_ready[proc_idx]) {
        wait_for_event(); // block on deterministic RTOS primitive
        continue;
    }
    // process samples in-place or via FPGA co-processor (no copies)
    process_buffer(proc_idx); // e.g., apply delay, phase adjust, re-synthesis
    dma_start_transmit(proc_idx); // schedule DMA to DAC
    buf_ready[proc_idx] = false;
    cur = proc_idx; // switch buffers
}