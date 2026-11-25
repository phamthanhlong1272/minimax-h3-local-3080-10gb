# AGENTS.md — Chỉ Thị Cài Đặt Tự Động Cho AI Agent (RTX 3080 10GB + 32GB RAM)

Tài liệu này dành cho AI Agent chạy trên máy cá nhân của người dùng (Windows, **NVIDIA RTX 3080 10GB VRAM**, **32GB DDR5 RAM**). Hãy đọc kỹ toàn bộ quy tắc dưới đây trước khi tải bất kỳ model hay chạy bất kỳ lệnh cài đặt nào.

---

## 1. QUY TẮC BẮT BUỘC & CÁC ĐIỀU CẤM (CRITICAL CONSTRAINTS)

1. **TUYỆT ĐỐI KHÔNG tải các model định dạng `NVFP4`** (ví dụ `qwen3vl_32b_minimax_h3_nvfp4_awq.safetensors` hoặc DiT `nvfp4`):
   - Lý do: RTX 3080 thuộc kiến trúc **Ampere (Compute Capability 8.6)**, không có phần cứng giải mã NVFP4 (chỉ có trên RTX 50-series Blackwell).
2. **TUYỆT ĐỐI KHÔNG tải hoặc load `Qwen3-VL-32B` bản gốc (BF16/FP16 ~15.7GB+)** trên máy 32GB RAM:
   - Lý do: Kết hợp với DiT sẽ gây tràn 32GB RAM vật lý và làm treo cứng Windows.
   - **Giải pháp bắt buộc:** Phải cài `nicolab28/ComfyUI-ClipProj` (`>= 0.1.13`) và dùng **`Qwen3-VL-4B (FP8)`** (~4.5–5GB) kèm file ánh xạ `mmh3-4b-ClipProj-v3.1-mlp.safetensors`.
3. **TUYỆT ĐỐI KHÔNG tải bản MiniMax H3 BF16/FP16 đầy đủ (40–120GB)** hoặc GGUF từ `Q5` trở lên:
   - Chỉ tải **GGUF `Q3_K_M` (~8.9GB — ưu tiên số 1 để test ổn định)** hoặc **`Q4_K_S` (~11GB)**.
4. **Tắt / Bypass `prompt_upsampler` (`p-h3-image_prompt_upsampler_w4a8`)** nếu thiếu RAM:
   - Tiết kiệm ngay 6.7GB RAM; người dùng sẽ viết prompt chuẩn bằng AI bên ngoài theo mẫu trong `docs/03-PROMPT-GUIDE-VIDEO-AFFILIATE-SAN-PHAM.md`.
5. **Luôn dùng `VAE Decode (Tiled)` (`tile_size = 512` hoặc `384`)**:
   - Không bao giờ dùng `VAE Decode` thường cho P-H3-Image (8MP) hoặc MiniMax H3 Video vì sẽ báo lỗi `CUDA out of memory` ở bước cuối cùng sau khi đã chạy xong 8/8 steps.

---

## 2. QUY TRÌNH THỰC THI TỪNG BƯỚC CHO AI AGENT

### Bước 1: Kiểm tra môi trường máy (`Pre-flight Check`)
Chạy `python scripts/setup_helper.py check` (hoặc kiểm tra trực tiếp) để xác nhận:
- GPU nhận đúng RTX 3080 (~10GB VRAM) qua `nvidia-smi`.
- Ổ đĩa đích cài ComfyUI còn trống **tối thiểu 60 GB** (SSD NVMe).
- Kiểm tra dung lượng **Windows Pagefile** (Virtual Memory): nếu tổng Commit Limit dưới 55 GB, hãy hướng dẫn hoặc nhắc người dùng nâng Pagefile trên ổ SSD lên `32768 MB – 65536 MB` (32–64 GB).
- Hỏi người dùng xem trên máy đã có sẵn thư mục `ComfyUI` (Portable hay Git hay Stability Matrix) chưa; nếu chưa, hỏi đường dẫn ổ SSD muốn cài mới.

### Bước 2: Cập nhật ComfyUI & Cài đặt Tăng tốc
- Đảm bảo **ComfyUI `>= v0.45.0`** (bắt buộc để hỗ trợ native kiến trúc `minimax_h3` và `PH3ImageConditioning`).
- Kiểm tra phiên bản PyTorch + CUDA trong môi trường Python của ComfyUI, cài đặt **`sageattention`** tương thích (`pip install sageattention` hoặc wheel prebuilt phù hợp Windows + Python + Torch + CUDA).
- Chạy `python scripts/setup_helper.py install-nodes --comfy-dir "<đường_dẫn_ComfyUI>"` để clone và cài `requirements.txt` cho các Custom Nodes:
  1. `https://github.com/city96/ComfyUI-GGUF`
  2. `https://github.com/nicolab28/ComfyUI-ClipProj`
  3. `https://github.com/monnky/ComfyUI-VDN-Minimax-H3`
  4. `https://github.com/larryvrh/ComfyUI-MiniMax-H3-Turbo`
  5. `https://github.com/nkxx188/ComfyUI-MiniMaxH3-Easy` *(giúp gom gọn node dễ thao tác)*

### Bước 3: Tải Model đúng phiên bản nhẹ cho 10GB VRAM
Dùng `huggingface_hub` (`hf download` / Python `snapshot_download` / `hf_hub_download` có resume) để tải chính xác vào cây thư mục của ComfyUI (xem chi tiết tại `docs/02-CHECKLIST-SETUP-A-Z-COMFYUI-H3.md`):
1. **Model Ảnh `P-H3-Image` (nếu test tạo ảnh sản phẩm trước):**
   - Repo: `Abiray/MiniMax-H3-Image-GGUF` hoặc `LSDJesus/MiniMax-H3-Image-GGUF` → chọn bản `Q3_K_M.gguf` → lưu vào `ComfyUI/models/unet/`.
2. **Model Video `MiniMax-H3` (I2V / FL2VA / Ref2VA):**
   - Repo: `unsloth/MiniMax-H3-GGUF` → chọn bản `Q3_K_M.gguf` → lưu vào `ComfyUI/models/unet/`.
3. **Text Encoder 4B + ClipProj:**
   - Tải `mmh3-4b-ClipProj-v3.1-mlp.safetensors` từ `NicoLab28/ClipProj-MiniMax-H3` → lưu vào `ComfyUI/models/clip_projections/`.
   - Tải model `Qwen3-VL-4B` (FP8/safetensors theo đúng README của `NicoLab28/ClipProj-MiniMax-H3`) → lưu vào `ComfyUI/models/text_encoders/`.
4. **Video VAE & Audio VAE:**
   - Từ `Comfy-Org/MiniMax-H3`: tải Video VAE (`int8_convrot` hoặc `fp16`) và Audio VAE (`fp32`) → lưu vào `ComfyUI/models/vae/`.
5. **Turbo LoRA 8-step:**
   - Từ `Wuli-art/MiniMax-H3-Turbo` (bản `FL2VA 8-step` / `Ref2VA 8-step`) hoặc `larryvrh/MiniMax-H3-Turbo-Lora` (`minimax_h3_turbo_v4_step600_ema.safetensors`) → lưu vào `ComfyUI/models/loras/`.
6. **VDN Weights:**
   - Từ `OpenVDN/vdn-minimax-h3` theo hướng dẫn của `monnky/ComfyUI-VDN-Minimax-H3` → lưu vào `ComfyUI/models/vdn/`.

### Bước 4: Tạo Script Khởi Chạy Tối Ưu (`run_3080_10gb.bat`)
Tạo file `.bat` khởi chạy ComfyUI với cờ bảo vệ VRAM:
```bat
@echo off
REM Tối ưu riêng cho RTX 3080 10GB + 32GB RAM
python -s main.py --use-sage-attention --reserve-vram 1.0
pause
```
*(Nếu dùng ComfyUI Portable thì trỏ `.\python_embeded\python.exe -s ComfyUI\main.py --windows-standalone-build --use-sage-attention --reserve-vram 1.0`. Nếu gặp OOM khi test thực tế, thêm `--lowvram`).*

### Bước 5: Bài Test Nghiệm Thu (Smoke Test)
1. **Test 1 (Ảnh sản phẩm 9:16):** Chạy thử tạo 1 ảnh `9:16` từ ảnh sản phẩm mẫu ở **8 steps, CFG = 1.0, scheduler `simple`, `VAE Decode (Tiled)` = 512**.
2. **Test 2 (Video nháp I2VA / FL2VA):** Chạy thử clip **5 giây, 24 fps** ở phân giải nháp an toàn **`384 × 672`** (hoặc `480 × 864`), **8 steps, CFG = 1.0, scheduler `simple`**, kiểm tra log VRAM không vượt ngưỡng crash và file `.mp4` xuất ra có cả hình lẫn âm thanh stereo 32kHz.

---

## 3. TÙY CHỌN DỰ PHÒNG (FALLBACK) NẾU NGƯỜI DÙNG MUỐN NHANH GỌN HƠN
Nếu người dùng muốn một giao diện All-in-One không cần nối node ComfyUI để làm video sản phẩm nhanh bằng **Wan 2.2 TI2V-5B** hoặc **LTX-2.3 Distilled** + **MMAudio**, hãy cài đặt thêm **[Wan2GP](https://github.com/deepbeepmeep/Wan2GP)** trong một môi trường ảo (`venv` / `conda`) tách biệt hoàn toàn với ComfyUI.
