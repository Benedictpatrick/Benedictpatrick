<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/header-dark.svg">
  <img src="assets/header-light.svg" width="100%" alt="Benedict Patrick. From the weights to the chip. I train my own models, write the engines that run them, and ship the tools around them.">
</picture>

<p>
  <a href="https://github.com/Benedictpatrick/portfolio"><b>Portfolio</b></a>&nbsp;&nbsp;&nbsp;
  <a href="https://www.linkedin.com/in/benedictpatrickcodes/"><b>LinkedIn</b></a>&nbsp;&nbsp;&nbsp;
  <a href="mailto:benedictpatrickjohn@gmail.com"><b>Email</b></a>&nbsp;&nbsp;&nbsp;
  <a href="https://huggingface.co/bencodez"><b>Hugging Face</b></a>&nbsp;&nbsp;&nbsp;
  <a href="https://www.npmjs.com/~bencodess"><b>npm</b></a>
</p>

I build AI that fits where it shouldn't: a $5 microcontroller, a budget phone, a browser tab. Most of my work sits between model architecture and the systems that run it.

<br>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/models-dark.svg">
  <img src="assets/models-light.svg" width="100%" alt="Models">
</picture>

<table>
  <tr>
    <td width="200" valign="top"><b>Core-1</b><br><sub>research, proof of concept</sub></td>
    <td valign="top">A language model designed for ordinary CPUs instead of rented GPUs. Every weight is <code>−1</code>, <code>0</code> or <code>+1</code>, packed at two bits each, so the model is sixteen times smaller than fp32 and multiplying becomes adding. A state space backbone keeps a fixed size state, so memory does not grow with every token. Validated at toy scale.</td>
  </tr>
  <tr>
    <td valign="top"><b>Phobos</b><br><sub>research</sub></td>
    <td valign="top">A hybrid architecture: Mamba-2 selective state space layers interleaved with sliding window attention, so attention comes back only where exact recall matters. The same codebase trains a parameter matched Transformer baseline, so every gain is measured, not assumed.</td>
  </tr>
  <tr>
    <td valign="top"><b><a href="https://huggingface.co/bencodez/Cipheron">Cipheron</a></b><br><sub>released, 0.5B, Apache 2.0</sub></td>
    <td valign="top">A small coding model trained for secure code review. It flags vulnerabilities and suggests safer implementations, fully offline. Strongest on SQL and command injection; the model card lists where it still falls short.</td>
  </tr>
</table>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/edge-dark.svg">
  <img src="assets/edge-light.svg" width="100%" alt="Edge">
</picture>

<table>
  <tr>
    <td width="200" valign="top"><b>Spark</b><br><sub>in training</sub></td>
    <td valign="top">Plain language in, tool calls out. A 3.6M parameter model, 2.2 MB on the chip, that runs fully offline on a $5 ESP32. Built for makers wiring their own devices.</td>
  </tr>
  <tr>
    <td valign="top"><b>Quanta Engine</b><br><sub>running on PC, phone next</sub></td>
    <td valign="top">An LLM inference engine written from scratch in C++, no llama.cpp underneath, aimed at the budget Android phones most people actually own. 4 bit mixed weights and batched prefill; first model Qwen2.5 0.5B.</td>
  </tr>
  <tr>
    <td valign="top"><b>thermollm</b><br><sub>in progress</sub></td>
    <td valign="top">A tool calling model under 100 MB. Grammar constrained decoding means every call it emits actually parses.</td>
  </tr>
</table>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/shipped-dark.svg">
  <img src="assets/shipped-light.svg" width="100%" alt="Shipped">
</picture>

<table>
  <tr>
    <td width="200" valign="top"><b><a href="https://www.npmjs.com/package/securevibe">securevibe</a></b><br><sub>on npm</sub></td>
    <td valign="top">A security scanner for code written fast. It finds the holes, proposes fixes, then rescans to prove each fix landed. Runs locally.<br><code>npm i -g securevibe</code></td>
  </tr>
  <tr>
    <td valign="top"><b><a href="https://benedictpatrick.github.io/smartgrep-web/">smartgrep</a></b><br><sub>on npm</sub></td>
    <td valign="top">Ask a codebase questions in plain English. Semantic search and answers with citations, entirely on your machine, with an MCP server for coding agents.<br><code>npm i -g smartgrep</code></td>
  </tr>
  <tr>
    <td valign="top"><b><a href="https://navoai.space">Navo</a></b><br><sub>live</sub></td>
    <td valign="top">A chat model that runs inside your browser tab on WebGPU. Nothing you type leaves your device. <a href="https://github.com/Benedictpatrick/Web-based-local-OfflineLLM">Source</a>.</td>
  </tr>
  <tr>
    <td valign="top"><b><a href="https://pyphone-studio.vercel.app">PyPhone Studio</a></b><br><sub>live</sub></td>
    <td valign="top">A real Python 3.11 interpreter on your phone, compiled to WebAssembly. Notebooks, pandas and matplotlib, plus an offline AI helper.</td>
  </tr>
</table>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/research-dark.svg">
  <img src="assets/research-light.svg" width="100%" alt="Research">
</picture>

<table>
  <tr>
    <td width="200" valign="top"><b><a href="https://github.com/Benedictpatrick/Parkinson-detection-">PARQ</a></b><br><sub>manuscript</sub></td>
    <td valign="top">Detecting Parkinson's disease from voice with a multitask, dual branch model. With Sai Dharshan A. and Dr Ashwini, Hindustan Institute of Technology and Science.</td>
  </tr>
  <tr>
    <td valign="top"><b>Cognitive Matter</b><br><sub>simulation</sub></td>
    <td valign="top">A spiking neural fabric simulated live in the browser that learns where you touch it. 4,096 neurons on sparse wiring at 5.1 ms per frame.</td>
  </tr>
</table>

<p>
  <code>C++</code> <code>Python</code> <code>PyTorch</code> <code>TypeScript</code> <code>WebGPU</code> <code>ONNX</code> <code>ESP32</code> <code>Ollama</code> <code>tree-sitter</code> <code>FastAPI</code> <code>Next.js</code>
</p>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/contact-dark.svg">
  <img src="assets/contact-light.svg" width="100%" alt="Contact">
</picture>

Open to internships, research collaborations and hard problems in small places. The fastest way to reach me is **[benedictpatrickjohn@gmail.com](mailto:benedictpatrickjohn@gmail.com)**.

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/footer-dark.svg">
  <img src="assets/footer-light.svg" width="100%" alt="">
</picture>
