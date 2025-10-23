volatile uint8_t bufferA[BUF_SIZE]; // buffer A
volatile uint8_t bufferB[BUF_SIZE]; // buffer B
volatile int active = 0; // 0->A filled, 1->B filled

// DMA complete callback (runs in ISR context)
void dma_complete_callback(void) {
  if (active == 0) {
    // mark A ready for processing and restart DMA to B
    start_dma_transfer(bufferB, BUF_SIZE); // // restart DMA to other buffer
    active = 1;
  } else {
    // mark B ready and restart DMA to A
    start_dma_transfer(bufferA, BUF_SIZE);
    active = 0;
  }
}

// processing task (runs in main loop or worker thread)
void processing_task(void) {
  while (1) {
    if (active == 1) {
      process_frame(bufferA); // // process captured data
    } else {
      process_frame(bufferB);
    }
    // small sleep or yield; ensure processing <= buffer fill time
  }
}