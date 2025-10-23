# pseudocode: conditioner extracts PRI and pulse width; generator synthesizes complex baseband spike
for epoch in range(epochs):
    for x_batch, y_batch in dataloader:
        # x_batch: raw I/Q frames, y_batch: target echoes
        params = conditioner(x_batch)            # # learnable extraction
        s_hat = generator(params)               # # synthesize spoof
        loss_recon = ((y_batch - s_hat).abs()**2).mean()
        loss_reg = reg_weight * regularizer(params) 
        loss = loss_recon + loss_reg
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
# inference: run conditioner then generator in low-precision on FPGA