# MiniMax H3 & P-H3-Image Local trên RTX 3080 10GB (Video Affiliate Sản Phẩm)

Bộ tài liệu nghiên cứu, tổng hợp hệ sinh thái open-source và kịch bản cài đặt tự động dành cho cấu hình **NVIDIA RTX 3080 (10GB VRAM) + 32GB RAM DDR5** trên Windows, phục vụ mục tiêu **tạo ảnh & video giới thiệu sản phẩm / Affiliate (TikTok Shop, Shopee Video, Reels 9:16) từ ảnh tham chiếu**.

---

## Mục tiêu của Repo này

1. **Đọc nghiên cứu tối nay:** Tổng hợp đầy đủ ưu/nhược điểm của các hệ thống chạy video AI local trên card 10GB VRAM năm 2026, cách ép chạy **MiniMax H3 (33B)** bằng combo **GGUF + ClipProj 4B + 8-Step Turbo LoRA + VDN + SageAttention**, và bộ công thức Prompt chuẩn làm video Affiliate không méo chữ/logo.
2. **Giao cho AI Agent tự cài đặt trên máy ở nhà:** Đã có sẵn file [`AGENTS.md`](./AGENTS.md) và script hỗ trợ [`scripts/setup_helper.py`](./scripts/setup_helper.py) để AI (Antigravity / Claude Code / Cursor / Codex) đọc và tự động thiết lập môi trường chuẩn xác mà không tải nhầm bản nặng gây tràn RAM/VRAM.

---

## Câu lệnh giao việc nhanh cho AI tối nay

Sau khi `git clone` repo này về máy có RTX 3080 10GB, mở AI Agent tại thư mục repo và nhắn:

```text
Hãy đọc kỹ file AGENTS.md và docs/02-CHECKLIST-SETUP-A-Z-COMFYUI-H3.md trong repo này. Kiểm tra cấu hình máy hiện tại của tôi (GPU, VRAM, RAM, ổ cứng trống, bản ComfyUI nếu đã có), sau đó lên kế hoạch và cài đặt bộ ComfyUI + MiniMax H3 8-step + P-H3-Image tối ưu cho RTX 3080 10GB + 32GB RAM theo đúng các quy tắc an toàn trong AGENTS.md.
```

---

## Cấu trúc tài liệu trong Repo

| File | Nội dung chính |
| :--- | :--- |
| [`AGENTS.md`](./AGENTS.md) | **Chỉ thị thực thi cho AI Agent ở máy nhà**: quy tắc cấm (tránh `NVFP4`, tránh `Qwen3-VL-32B`), thứ tự cài đặt, kiểm tra VRAM/RAM và bài test nghiệm thu. |
| [`docs/01-TONG-QUAN-HE-SINH-THAI-10GB-VRAM.md`](./docs/01-TONG-QUAN-HE-SINH-THAI-10GB-VRAM.md) | So sánh 5 hệ thống video local tốt nhất cho 3080 10GB (`Wan2GP`, `MiniMax H3 8-step`, `LTX-2.3`, `FramePack-Studio`, `VACE`), các kênh YouTube & repo cộng đồng đánh giá cao nhất. |
| [`docs/02-CHECKLIST-SETUP-A-Z-COMFYUI-H3.md`](./docs/02-CHECKLIST-SETUP-A-Z-COMFYUI-H3.md) | **Checklist cài đặt A → Z**: cấu hình Windows Pagefile, cài Custom Nodes, bảng link tải từng file model & đúng thư mục lưu, cờ chạy `.bat`, nối node ComfyUI và bảng gỡ lỗi OOM. |
| [`docs/03-PROMPT-GUIDE-VIDEO-AFFILIATE-SAN-PHAM.md`](./docs/03-PROMPT-GUIDE-VIDEO-AFFILIATE-SAN-PHAM.md) | **Cẩm nang Prompt Video Affiliate (`9:16`)**: quy trình 2 bước (Ảnh P-H3-Image → Video H3 I2VA / FL2VA / Ref2VA), mẫu prompt copy-paste chuẩn `HMT-Official`, xử lý tiếng Việt/ASMR và cách trị 6 lỗi méo logo/sai tỷ lệ/thừa ngón tay. |
| [`scripts/setup_helper.py`](./scripts/setup_helper.py) | Script Python kiểm tra phần cứng Windows (GPU, RAM, ổ đĩa), tự động tạo cây thư mục `models/` và clone bộ Custom Nodes chuẩn vào ComfyUI. |

---

## Tóm tắt kiến trúc sống còn cho RTX 3080 10GB + 32GB RAM

Bản gốc MiniMax H3 nặng 33B tham số + Text Encoder `Qwen3-VL-32B` (~15.7GB), đòi hỏi 24–60GB VRAM và 64GB+ RAM. Để chạy mượt trên **10GB VRAM + 32GB RAM**, bắt buộc thay thế 4 mảnh ghép:

1. **Diffusion Model:** Dùng bản lượng tử hóa **GGUF `Q3_K_M` (~8.9GB)** hoặc **`Q4_K_S` (~11GB)** qua `city96/ComfyUI-GGUF` *(tuyệt đối không dùng `NVFP4` vì RTX 3080 là kiến trúc Ampere)*.
2. **Text Encoder:** Dùng **`nicolab28/ComfyUI-ClipProj`** + **`Qwen3-VL-4B (FP8)`** (~4.5–5GB) + `mmh3-4b-ClipProj-v3.1-mlp.safetensors` thay cho bản 32B gốc *(tiết kiệm ~11GB RAM/VRAM)*.
3. **Tăng tốc & Giữ VRAM chuỗi dài:** Kết hợp **Turbo LoRA 8-step** (`Wuli-art/MiniMax-H3-Turbo` hoặc `larryvrh` v4) + **VideoDeltaNet (`monnky/ComfyUI-VDN-Minimax-H3`)** + **SageAttention**.
4. **Giải mã hình ảnh không văng cuối bước render:** Luôn dùng **`VAE Decode (Tiled)`** (`tile_size = 512`) và render gốc ở `480×864` (5 giây, 24 fps, 8 steps, CFG 1.0, scheduler `simple`) rồi upscale ở bước hậu kỳ.
