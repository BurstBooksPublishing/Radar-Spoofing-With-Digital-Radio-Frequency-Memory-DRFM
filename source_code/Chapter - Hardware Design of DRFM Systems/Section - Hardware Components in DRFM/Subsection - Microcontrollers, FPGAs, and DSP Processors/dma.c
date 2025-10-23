/* Configure DMA descriptor for FPGA stream */ 
dma_desc.src = FPGA_STREAM_ADDR;    // source is FPGA stream interface
dma_desc.dst = phys_buffer;         // destination in RAM
dma_desc.len = buffer_bytes;
dma_desc.flags = DMA_FLAG_INT_ON_COMPLETION;

/* Program ADC/DAC control registers via memory-mapped IO */
mmio_write(REG_ADC_CTRL, ADC_ENABLE | ADC_SAMPLE_RATE_100MHZ); // start ADC

/* Start DMA transfer (non-blocking) */
dma_start(&dma_desc);

/* Wait or poll for completion; process buffer in ISR or task */
while (!dma_completed(&dma_desc)) {
    /* do low-priority housekeeping */
}
process_buffer(phys_buffer);  // apply configuration updates or pass to DSP