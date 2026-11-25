# Checklist Setup A → Z: MiniMax H3 (8-Step) & P-H3-Image Trên RTX 3080 10GB + 32GB RAM

Hướng dẫn từng bước để thiết lập và chạy thử nghiệm thành công trên máy **Windows + RTX 3080 (10GB VRAM) + 32GB RAM DDR5**.

---

## BƯỚC 1: Chuẩn Bị Hệ Thống Windows (Bắt Buộc Trước Khi Chạy)

- [ ] **Dung lượng ổ SSD trống:** Tối thiểu **50–60 GB** (cho bộ model GGUF + ClipProj + VAE + LoRA + cache).
- [ ] **Mở rộng Windows Pagefile (Virtual Memory) trên ổ SSD NVMe:**
  - Mở *System Properties → Advanced → Performance Settings → Advanced → Virtual Memory → Change*.
  - Bỏ tích *Automatically manage paging file size*, chọn ổ SSD tốc độ cao → chọn *Custom size*:
    - **Initial size (MB):** `32768` (32 GB)
    - **Maximum size (MB):** `65536` (64 GB)
  - Bấm **Set** → **OK** → Khởi động lại máy.
  - *Lý do:* Khi ComfyUI nạp và chuyển đổi model vào/ra VRAM, tổng bộ nhớ cấp phát tức thời có thể chạm 35–45 GB; nếu không có Pagefile đủ lớn trên SSD, ComfyUI sẽ tự văng không báo lỗi.
- [ ] **Giải phóng VRAM trước khi render:** Tắt *Hardware Acceleration* trong Chrome/Edge hoặc đóng trình duyệt/ứng dụng quay màn hình để dành trọn ~9.2–9.5 GB VRAM trống cho ComfyUI.

---

## BƯỚC 2: Cài Đặt / Cập Nhật ComfyUI & Custom Nodes

- [ ] **Cập nhật ComfyUI lên bản mới nhất (`>= v0.45.0`):**
  - Bản Portable: chạy `update\update_comfyui.bat`.
  - Bản Git: chạy `git pull` và `python -m pip install -r requirements.txt`.
- [ ] **Cài đặt `SageAttention`:**
  - Giúp tăng tốc độ tính toán attention của video lên **30–50%** và hạ đỉnh tiêu thụ VRAM trên kiến trúc Ampere (RTX 3080).
  - Lệnh cài trong môi trường Python của ComfyUI: `pip install sageattention` (hoặc cài file `.whl` biên dịch sẵn cho Windows khớp phiên bản Python/PyTorch/CUDA).
- [ ] **Cài đặt 5 Custom Nodes cốt lõi** (qua **ComfyUI Manager** hoặc dùng `python scripts/setup_helper.py install-nodes`):
  1. [city96/ComfyUI-GGUF](https://github.com/city96/ComfyUI-GGUF) — Đọc trọng số GGUF `Q3_K_M` / `Q4_K_S`.
  2. [nicolab28/ComfyUI-ClipProj](https://github.com/nicolab28/ComfyUI-ClipProj) *(bản `>= 0.1.13`)* — Dùng `Qwen3-VL-4B` thay cho `Qwen3-VL-32B`.
  3. [monnky/ComfyUI-VDN-Minimax-H3](https://github.com/monnky/ComfyUI-VDN-Minimax-H3) — Cơ chế VideoDeltaNet tiết kiệm VRAM cho chuỗi khung hình video.
  4. [larryvrh/ComfyUI-MiniMax-H3-Turbo](https://github.com/larryvrh/ComfyUI-MiniMax-H3-Turbo) — Hỗ trợ Turbo LoRA 8-step.
  5. [nkxx188/ComfyUI-MiniMaxH3-Easy](https://github.com/nkxx188/ComfyUI-MiniMaxH3-Easy) — Gom gọn dây nối T2V / I2V / FL2VA / Ref2VA.

---

## BƯỚC 3: Danh Sách File Cần Tải & Đúng Thư Mục Lưu

> ⚠️ **CẢNH BÁO CHO RTX 3080:** Không tải bất kỳ file nào có hậu tố **`nvfp4`** (chỉ dành cho RTX 50-series) và không tải **`Qwen3-VL-32B`** bản gốc (~15.7 GB).

| Nhóm | Nguồn tải (Hugging Face) | Tên / Loại File khuyên chọn | Thư mục lưu trong `ComfyUI/` | Dung lượng |
| :--- | :--- | :--- | :--- | :-: |
| **1. Video DiT (GGUF)** | [unsloth/MiniMax-H3-GGUF](https://huggingface.co/unsloth/MiniMax-H3-GGUF) | Bản **`Q3_K_M.gguf`** *(an toàn nhất)* hoặc **`Q4_K_S.gguf`** *(nét hơn)* | `models/unet/` | ~9–11 GB |
| **2. Image DiT (GGUF)** *(cho P-H3-Image)* | [Abiray/MiniMax-H3-Image-GGUF](https://huggingface.co/Abiray/MiniMax-H3-Image-GGUF) hoặc [LSDJesus/MiniMax-H3-Image-GGUF](https://huggingface.co/LSDJesus/MiniMax-H3-Image-GGUF) | `MiniMax-H3-Image-Pruned-Q3_K_M.gguf` *(hoặc `Q4_K_S`)* | `models/unet/` | ~8.9–11.5 GB |
| **3. Text Encoder 4B** | Hugging Face *(theo repo hướng dẫn của ClipProj)* | `Qwen3-VL-4B` bản `fp8` / `safetensors` | `models/text_encoders/` | ~4.5–5 GB |
| **4. ClipProj Matrix** | [NicoLab28/ClipProj-MiniMax-H3](https://huggingface.co/NicoLab28/ClipProj-MiniMax-H3) | **`mmh3-4b-ClipProj-v3.1-mlp.safetensors`** | `models/clip_projections/` | ~53 MB |
| **5. Video & Audio VAE** | [Comfy-Org/MiniMax-H3](https://huggingface.co/Comfy-Org/MiniMax-H3) | `minimax_h3_video_vae_int8_convrot.safetensors` + `minimax_h3_audio_vae_fp32.safetensors` *(với P-H3-Image có thêm `p-h3-image_vae_int8_convrot.safetensors`)* | `models/vae/` | ~4–6 GB |
| **6. Turbo LoRA 8-step** | [Wuli-art/MiniMax-H3-Turbo](https://huggingface.co/Wuli-art/MiniMax-H3-Turbo) **hoặc** [larryvrh/MiniMax-H3-Turbo-Lora](https://huggingface.co/larryvrh/MiniMax-H3-Turbo-Lora) | Bản **FL2VA / Ref2VA 8-step** *(Wuli-art)* hoặc `minimax_h3_turbo_v4_step600_ema.safetensors` *(larryvrh)* | `models/loras/` | ~1–2 GB |
| **7. VDN Adapter** | [OpenVDN/vdn-minimax-h3](https://huggingface.co/OpenVDN/vdn-minimax-h3) | Trọng số nhánh VDN-H3 | `models/vdn/` | Nhẹ |

---

## BƯỚC 4: Cấu Hình File Khởi Chạy ComfyUI (`.bat`)

Tạo file `run_3080_10gb.bat` cạnh file chạy gốc của ComfyUI:

### Với bản ComfyUI Windows Portable:
```bat
@echo off
.\python_embeded\python.exe -s ComfyUI\main.py --windows-standalone-build --use-sage-attention --reserve-vram 1.0
pause
```

### Với bản cài Git / Venv:
```bat
@echo off
call venv\Scripts\activate
python -s main.py --use-sage-attention --reserve-vram 1.0
pause
```

- `--use-sage-attention`: Kích hoạt SageAttention giảm VRAM và tăng tốc.
- `--reserve-vram 1.0`: Giữ lại 1.0 GB VRAM cho hệ điều hành để tránh treo driver màn hình khi VRAM tiến sát 10 GB.
- Nếu gặp lỗi `CUDA out of memory` ngay bước đầu, thêm `--lowvram` vào cuối dòng lệnh.

---

## BƯỚC 5: Cách Lắp Sơ Đồ Node & Thông Số Chạy Thử Lần Đầu

1. Mở ComfyUI → vào **Workflow → Browse Templates → Video** → chọn **MiniMax H3 I2V** (hoặc **FL2VA / R2V**).
2. Thực hiện **4 điểm thay thế** để chạy vừa 10GB VRAM + 32GB RAM:
   - **Đổi Model Loader:** Thay `Load Diffusion Model` gốc bằng **`Unet Loader (GGUF)`** → trỏ tới file `Q3_K_M.gguf`.
   - **Đổi Text Encoder:** Thay bộ nạp Qwen 32B gốc bằng **`ClipProj Loader`** → chọn `Qwen3-VL-4B` + `mmh3-4b-ClipProj-v3.1-mlp.safetensors` → nối vào cổng Conditioning/CLIP. *(Nếu mở template P-H3-Image, nhớ **Bypass** node `prompt_upsampler` để tiết kiệm 6.7GB RAM).*
   - **Chèn VDN + 8-Step Turbo:** Nối theo chuỗi: `Unet Loader (GGUF)` → **VDN Patch Node** → **MiniMax-H3 Turbo LoRA (8-step)** → `SamplerCustomAdvanced`.
   - **Đổi giải mã VAE:** Thay `VAE Decode` thường bằng **`VAE Decode (Tiled)`** với `tile_size = 512` (hoặc `384` nếu vẫn chật VRAM).
3. **Thông số Vàng cho bài test đầu tiên trên RTX 3080 10GB:**
   - **Độ phân giải test nháp:** `384 × 672` (siêu an toàn, test chuyển động & seed nhanh) → sau đó nâng lên **`480 × 864`** (dọc 9:16) hoặc **`768 × 432`** (ngang 16:9).
   - **Thời lượng:** `5 giây` | **FPS:** `24`.
   - **Steps:** `8` *(tuyệt đối không tăng lên 20 steps khi đang bật Turbo LoRA)*.
   - **Scheduler:** `simple` | **CFG:** `1.0` *(không dùng negative prompt)*.

---

## BƯỚC 6: Bảng Gỡ Lỗi Nhanh (Troubleshooting)

| Triệu chứng lỗi | Nguyên nhân | Cách khắc phục ngay |
| :--- | :--- | :--- |
| **Báo `CUDA out of memory` ngay khi bắt đầu chạy Sampler** | Đỉnh VRAM vượt quá 10GB | Hạ độ phân giải xuống `384×672`, bật `--lowvram`, tăng `--reserve-vram 1.5`, kiểm tra node **VDN Patch** đã gắn đúng trước Sampler chưa. |
| **Chạy xong đủ 8/8 steps rồi mới văng `CUDA out of memory`** | Tràn VRAM ở bước giải mã khung hình VAE | Bắt buộc chuyển sang **`VAE Decode (Tiled)`** và hạ `tile_size` xuống `256` hoặc `384`. |
| **Cửa sổ ComfyUI tự đóng phụt hoặc máy đơ cứng** | Tràn 32GB RAM hệ thống | Kiểm tra lại Pagefile 32–64GB (Bước 1), đảm bảo đang dùng **ClipProj 4B** và đã **Bypass** node `prompt_upsampler`. |
| **Ảnh / Video bị gắt nét, da/vỏ hộp bóng nhựa ("crunchy")** | Đặt dư số steps hoặc sai sampler | Giữ đúng **6–8 steps**, `CFG = 1.0`, `scheduler = simple`, thử đổi sampler sang `LCM` hoặc `res_multistep`. |
| **Âm thanh bị rè, méo hoặc đứt quãng** | Hạ steps quá thấp (4 steps) | Giữ nguyên **8 steps** (không dùng 4 steps khi cần lấy âm thanh đồng bộ). |
| **Báo lỗi không nhận kiến trúc `minimax_h3`** | ComfyUI hoặc `ComfyUI-GGUF` quá cũ | Cập nhật ComfyUI lên `>= v0.45.0` và `git pull` mới nhất trong thư mục `custom_nodes/ComfyUI-GGUF`. |
