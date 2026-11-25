# Tổng Quan Hệ Sinh Thái Chạy AI Video Local Trên RTX 3080 10GB + 32GB RAM (2026)

Tài liệu tổng hợp các hệ thống mã nguồn mở (GitHub / Hugging Face), kênh YouTube và kinh nghiệm cộng đồng (`r/comfyui`, `r/StableDiffusion`) phù hợp nhất cho bài toán **tạo video giới thiệu sản phẩm / Affiliate từ ảnh tham chiếu** trên cấu hình **RTX 3080 10GB VRAM + 32GB RAM DDR5**.

---

## 1. Bảng So Sánh 5 Hệ Thống Video Local Phù Hợp Nhất

| Hệ thống / Repo GitHub | Độ khó cài | Điểm mạnh nhất cho Video Sản phẩm | Audio gốc | Độ ổn định trên 3080 10GB |
| :--- | :--- | :--- | :---: | :--- |
| **1. [Wan2GP](https://github.com/deepbeepmeep/Wan2GP)** | Dễ (Web UI sẵn, không nối node) | **All-in-One cho GPU 8–12GB VRAM**: tự động offload sang 32GB RAM, tích hợp sẵn Wan 2.2 (5B/14B), LTX-2.3, HunyuanVideo 1.5, Qwen-Image, Flux 2, MMAudio. | Có (qua LTX-2 / MMAudio) | **Rất tốt** |
| **2. ComfyUI + [MiniMax H3](https://github.com/MiniMax-AI/MiniMax-H3) (8-step)** | Khá phức tạp | **Đa ảnh tham chiếu (Ref2VA) + nối First-Last Frame (FL2VA)** kèm âm thanh vật lý stereo rất thật; dùng chung kiến trúc với P-H3-Image. | Có (Stereo 32kHz native) | **Trung bình – Khá** *(bắt buộc GGUF Q3/Q4 + ClipProj 4B + VDN)* |
| **3. ComfyUI + LTX-2 / LTX-2.3 (GGUF)** | Trung bình (có template sẵn) | **Tốc độ render nhanh nhất**, làm được clip ~10s ở 720p kèm âm thanh, có Latent Upscaler 2-pass cực hợp 10GB VRAM. | Có (Stereo native) | **Tốt** *(dùng Q4_K_M + Gemma 3 12B FP8)* |
| **4. [FramePack-Studio](https://github.com/FP-Studio/framepack-studio)** *(fork từ [lllyasviel/FramePack](https://github.com/lllyasviel/FramePack))* | Dễ (App riêng) | **Làm video I2V dài (15–30s+)** trên VRAM từ 6GB nhờ nén ngữ cảnh frame; có **Timestamped Prompts** đổi góc/hành động theo từng giây. | Không | **Tốt** *(cần Pagefile 64GB + SageAttention + TeaCache)* |
| **5. ComfyUI + [VACE](https://github.com/ali-vilab/VACE)** *(Wan2.1-VACE)* | Khá phức tạp | **Chuyên kiểm soát vật thể (R2V)**: đưa ảnh sản phẩm + mask/depth để ép sản phẩm chuyển động đúng quỹ đạo, ít biến dạng. | Không | **Tốt** *(bản `Wan2.1-VACE-1.3B` rất nhẹ; bản 14B dùng GGUF Q4)* |

---

## 2. Hệ Sinh Thái MiniMax H3 Trên ComfyUI: Các Repo Được Đánh Giá Cao Nhất

### A. Nhóm làm gọn giao diện & dễ sử dụng
- **[nkxx188/ComfyUI-MiniMaxH3-Easy](https://github.com/nkxx188/ComfyUI-MiniMaxH3-Easy):** Nén hệ thống dây nối phức tạp của T2V, I2V, First-Last-Frame và Ref2VA vào 1 node gọn, hỗ trợ gõ thoại inline và kéo thả nhiều ảnh/audio tham chiếu.
- **[CharlesMod/h3-studio](https://github.com/CharlesMod/h3-studio):** Hỗ trợ định dạng cấu trúc prompt schema chuẩn mà MiniMax H3 yêu cầu.
- **[javawock7618/comfy-MiniMax-H3-workflows](https://huggingface.co/javawock7618/comfy-MiniMax-H3-workflows):** Kho workflow `.json` dựng sẵn cho First-Last-Frame, R2V, T2V có tích hợp Block Sparse Attention và memory offloading.
- **[LeonQ8/ComfyUI-ALLinONE-MinimaxH3](https://github.com/LeonQ8/ComfyUI-ALLinONE-MinimaxH3):** Gộp T2V, I2V, R2V, masking và keyframing trong 1 node.

### B. Nhóm làm Video Dài / Nhiều Cảnh (Multi-shot TVC 15–30s)
- **[seesee75-commits/ComfyUI-MiniMaxH3-Director](https://github.com/seesee75-commits/ComfyUI-MiniMaxH3-Director):** Trình biên tập Timeline & Storyboard ngay trong ComfyUI — quản lý nhân vật/sản phẩm, âm thanh, keyframe và nối cảnh (shot-chaining) kèm live preview.
- **[tritant/ComfyUI_MiniMax_H3_Extender](https://github.com/tritant/ComfyUI_MiniMax_H3_Extender)** *(cùng các nhánh cộng đồng `ComfyUI-H3-Motion-Context`, `comfyui-obvpm-timeline`)*: Nối nhiều đoạn clip 5s thành video dài mà giữ liền mạch chuyển động, màu sắc sản phẩm và âm thanh nhờ disk caching / truyền latent.

### C. Nhóm tối ưu VRAM thấp (8GB–10GB) & Tăng tốc 8-step
- **[city96/ComfyUI-GGUF](https://github.com/city96/ComfyUI-GGUF):** Bắt buộc để chạy các bản lượng tử hóa GGUF:
  - Video GGUF: [unsloth/MiniMax-H3-GGUF](https://huggingface.co/unsloth/MiniMax-H3-GGUF)
  - Ảnh GGUF: [Abiray/MiniMax-H3-Image-GGUF](https://huggingface.co/Abiray/MiniMax-H3-Image-GGUF), [LSDJesus/MiniMax-H3-Image-GGUF](https://huggingface.co/LSDJesus/MiniMax-H3-Image-GGUF)
- **[nicolab28/ComfyUI-ClipProj](https://github.com/nicolab28/ComfyUI-ClipProj)** + **[NicoLab28/ClipProj-MiniMax-H3](https://huggingface.co/NicoLab28/ClipProj-MiniMax-H3):** Thay thế `Qwen3-VL-32B` (~15.7GB) bằng **`Qwen3-VL-4B (FP8)`** (~4.5–5.2GB) — mảnh ghép quan trọng nhất để không tràn 32GB RAM.
- **[monnky/ComfyUI-VDN-Minimax-H3](https://github.com/monnky/ComfyUI-VDN-Minimax-H3)** + **[OpenVDN/vdn-minimax-h3](https://huggingface.co/OpenVDN/vdn-minimax-h3):** Thay thế quadratic softmax attention bằng VideoDeltaNet, cắt giảm mạnh mức ăn VRAM khi sinh chuỗi video.
- **[Wuli-art/MiniMax-H3-Turbo](https://huggingface.co/Wuli-art/MiniMax-H3-Turbo)** & **[larryvrh/ComfyUI-MiniMax-H3-Turbo](https://github.com/larryvrh/ComfyUI-MiniMax-H3-Turbo)** ([weights](https://huggingface.co/larryvrh/MiniMax-H3-Turbo-Lora)): Giảm số bước lặp từ 20+ steps xuống **6–8 steps** (tăng tốc ~3 lần). Bản `v4` của `larryvrh` và bản `FL2VA / Ref2VA 8-step` của `Wuli-art` giữ chi tiết tĩnh/sản phẩm tự nhiên, không bị giả nhựa và không rè tiếng như 4-step.
- **[H3-Tiny/MiniMax-H3-Tiny-ComfyUI](https://huggingface.co/H3-Tiny/MiniMax-H3-Tiny-ComfyUI):** Bản cắt tỉa cấu trúc từ 33B xuống 17B / 14B chạy native không cần custom node.
- **[ByronLeeeee/ComfyUI-MiniMax-H3-Optimization-Suite](https://github.com/ByronLeeeee/ComfyUI-MiniMax-H3-Optimization-Suite):** Tối ưu Sage2 Attention & quản lý VRAM chuỗi dài *(bỏ qua phần NVFP4 vì chỉ dành cho RTX 50-series)*.

---

## 3. Tài Liệu & Kênh YouTube Tham Khảo Đáng Chú Ý

1. **Hướng dẫn Tiếng Việt chuẩn cú pháp Prompt MiniMax H3:**
   - YouTube: *"MiniMax H3 trên ComfyUI, bạn đã biết cách dùng chưa?"* (`https://www.youtube.com/watch?v=qPPLOW4OdPw`)
   - Tài liệu gốc đi kèm: [`tuyenhm68/HMT-Official/002-minimax-h3-guide`](https://github.com/tuyenhm68/HMT-Official/blob/main/002-minimax-h3-guide/README.md) *(Lưu ý: hướng dẫn này viết cho máy 24GB VRAM + 64GB RAM, cần áp dụng bảng chuyển đổi GGUF + ClipProj trong `docs/02-CHECKLIST-SETUP-A-Z-COMFYUI-H3.md` để chạy trên 3080 10GB).*
2. **Hướng dẫn ép chạy 8GB–12GB VRAM của cộng đồng quốc tế:**
   - **RareTutor / AI Learning +:** *"Run Minimax H3 on 8GB VRAM! Fast 8 Step VDN ComfyUI Tutorial"* (kết hợp VDN + 8-step Turbo + SageAttention).
   - **The Local Lab:** *"Fastest MiniMax H3 Setup AI Video in 4 Steps on 12GB VRAM"* (tối ưu cờ `--vram-headroom` / `--reserve-vram` và CUDA).

---

## 4. Nhóm Model Dựng Ảnh Sản Phẩm (Bước 1 Trước Khi Làm Video)

Để sản phẩm giữ nguyên 100% logo, nhãn chữ và đúng kích thước ngoài đời trước khi đưa vào tạo video:
1. **P-H3-Image (Pruna AI — GGUF Q3_K_M / Q4_K_S):** Hỗ trợ tới **8 ảnh tham chiếu** (`<Picture 1>`..`<Picture 8>`), hiểu sâu không gian 3D & ánh sáng nhờ kế thừa kiến trúc MiniMax H3, chạy chỉ **8 steps, CFG = 1.0**.
2. **Qwen-Image-Edit (GGUF):** Rất mạnh về tách nền, ghép sản phẩm vào bối cảnh mới và giữ chữ in sắc nét.
3. **Flux Kontext (GGUF Q4):** Mạnh về đổi góc ánh sáng studio, mặt bàn nước/đá/gỗ mà giữ nguyên hình khối vật thể.
