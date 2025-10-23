/* Setup DMA for two buffers: buf0 and buf1 */
dma_start(buf0, len); // start DMA into buf0
dma_start(buf1, len); // start DMA into buf1
current = 0;
while (system_active) {
  if (dma_done(current)) {
    process_buffer(buf[current]); // small control/metadata updates
    dma_rearm(current); // re-enable DMA on this buffer
    current ^= 1; // switch buffers
  }
  // optionally poll or sleep briefly; keep ISR minimal
}