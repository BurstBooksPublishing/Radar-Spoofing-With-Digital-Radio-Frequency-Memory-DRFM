/* writer: ADC DMA fills SRAM page; host moves to DRAM page */
volatile uint16_t *sram_page = SRAM_BASE;    // small, deterministic SRAM page
uint8_t dram_page_index = 0;
const int PAGE_SAMPLES = 16384;              // samples per SRAM page

// DMA interrupt handler (called when SRAM page is full)
void dma_irq_handler(void) {
    // mark page ready for transfer
    sram_page_ready = true;
}

// background transfer task
void transfer_task(void) {
    while (1) {
        if (sram_page_ready) {
            // copy with DMA engine to DRAM (large burst transfer)
            dma_memcpy( DRAM_BASE + (dram_page_index * PAGE_BYTES),
                        sram_page, PAGE_BYTES );
            // acknowledge and reuse SRAM page
            sram_page_ready = false;
            dram_page_index = (dram_page_index + 1) % DRAM_PAGES;
        }
        // other work: DSP on recent SRAM, handle retransmit queue
    }
}