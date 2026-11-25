# Cẩm Nang Prompt & Chiến Thuật Làm Video Affiliate (`9:16`) Từ Ảnh Sản Phẩm

Tổng hợp quy tắc viết Prompt chuẩn tài liệu gốc **MiniMax H3 (`HMT-Official` / Official Docs)** & **P-H3-Image**, tối ưu riêng cho quy trình làm **video Affiliate (TikTok Shop, Shopee Video, Reels)** từ ảnh sản phẩm trên card **RTX 3080 10GB**.

---

## 1. Chiến Thuật "2 Bước & 3 Góc Máy" (Bí Quyết Không Méo Logo & Cao Chuyển Đổi)

Không bao giờ đưa thẳng ảnh sản phẩm vuông `1:1` nền trắng lấy từ sàn TMĐT vào model tạo video ngay. Hãy tách làm **2 bước**:

1. **Bước 1 — Dựng 3 Ảnh Keyframe `9:16` bằng P-H3-Image (8 steps/ảnh, cực nhanh):**
   - Lọc ảnh tĩnh rất rẻ (tạo 4 tấm mất vài chục giây, chọn tấm bàn tay đủ 5 ngón đẹp nhất và chữ trên bao bì nét 100%).
   - Chuẩn bị **3 góc ăn khách nhất của video AFF**:
     - **Góc 1 (Hook 0–4s — UGC Cầm Tay):** Bàn tay người thật cầm sản phẩm giơ lên trước cam điện thoại (tạo cảm giác review thật, không bị lướt qua như ảnh quảng cáo 3D).
     - **Góc 2 (Demo 4–9s — Cận Cảnh Chi Tiết):** Cận cảnh vòi xịt, chất kem, bánh lăn, đầu cọ hoặc bề mặt vật liệu dưới ánh sáng tự nhiên.
     - **Góc 3 (Chốt đơn 9–14s — Lifestyle Đặt Bàn):** Sản phẩm đặt trên mặt bàn thực tế, chừa **Safe Zone** trống 25% bên dưới cho chữ phụ đề + Giỏ hàng vàng TikTok Shop và 15% mép phải cho cột nút Tim/Bình luận/Chia sẻ.
2. **Bước 2 — Biến từng ảnh thành clip 4–5 giây bằng MiniMax H3 (8-step):**
   - Mỗi clip 4–5 giây vừa khít ngưỡng an toàn 10GB VRAM của RTX 3080, sau đó ghép 3 clip trong CapCut/Premiere thành video AFF 12–15 giây hoàn chỉnh.

---

## 2. Bộ Prompt Bước 1: Tạo Ảnh Sản Phẩm AFF Với P-H3-Image

Trong workflow *P-H3-Image: Image Edit*, nạp ảnh sản phẩm gốc vào **`<Picture 1>`**.

### Mẫu 1A — Ảnh UGC cầm tay đời thường (tự nhiên như chụp iPhone)
```text
Aspect ratio: 9:16
Request: Create an authentic handheld smartphone UGC photo showing a young Vietnamese woman's hand naturally holding the exact product from <Picture 1> in the upper-center of the 9:16 vertical frame, leaving clean negative space in the bottom quarter for captions. Keep the product's exact shape, real-world hand-held scale, cap structure, colors, logo, and all printed label text from <Picture 1> completely unchanged. Background is a softly blurred sunlit bedroom vanity table with morning window daylight, natural skin texture, shot on iPhone main camera, realistic contact shadows, no artificial CGI look.
```

### Mẫu 1B — Cặp Ảnh Đầu & Ảnh Cuối (dùng cho chế độ nối mượt FL2VA)
- **Tạo Ảnh Đầu (`start_frame.png`):**
```text
Aspect ratio: 9:16
Request: Place the exact product from <Picture 1> standing in the upper-center safe zone of a vertical 9:16 frame on a clean textured wooden desk beside a softly blurred coffee cup and green leaf, bathed in warm natural side window light with realistic shadows. Keep the exact product geometry, material finish, colors, and all printed label text from <Picture 1> 100% intact.
```
- **Tạo Ảnh Cuối (`end_frame.png` — nạp `start_frame.png` vào làm `<Picture 1>`):**
```text
Aspect ratio: 9:16
Request: Keep the exact same wooden desk, lighting, and product from <Picture 1>, shifted to a slightly closer three-quarter angle as a clean right hand gently touches the top cap of the product, keeping all printed logo and label text sharp and completely unchanged.
```

---

## 3. Bộ Prompt Bước 2: Tạo Video Sản Phẩm Chuẩn Cú Pháp MiniMax H3

### 4 Luật Cốt Lõi Của MiniMax H3 (Theo `HMT-Official`)
1. **Dòng mở đầu neo khung hình (Anchor Header):** Phải đặt ở dòng đầu tiên trước cả `integrated_multimodal_description`.
2. **Khóa vật thể ngay câu đầu `[Shot 1]`:** Mở bằng `<Picture 1>` và nhắc lại chi tiết màu sắc, kiểu dáng, chất liệu, chữ trên nhãn trong dấu ngoặc kép `"..."` trước khi mô tả chuyển động.
3. **Cụm từ vàng chống nhòe chữ/logo:** Mọi chuyển động camera đều phải gắn cụm **`with small amplitude at slow speed`**.
4. **Chiến thuật Âm thanh & Tiếng Việt cho AFF:**
   - MiniMax H3 hiện mới hỗ trợ chính thức ổn định 11 ngôn ngữ (chưa có Tiếng Việt trong nhóm ổn định chính thức; nếu ép đọc `<d>[Vietnamese]...</d>` giọng dễ chập chờn).
   - **Cách làm tốt nhất cho AFF Việt Nam:** Đặt `non_diegetic_music: N/A` (tắt nhạc nền AI để chèn nhạc xu hướng TikTok không bản quyền), tận dụng tối đa `overall_soundscape` để H3 sinh **âm thanh vật lý ASMR cực thật của sản phẩm** (tiếng gõ ngón tay lên vỏ nhám, tiếng mở nắp *click*, tiếng xịt sương, tiếng vải sột soạt), rồi lồng Voiceover tiếng Việt thật / TTS Việt bên ngoài!

---

### Mẫu 2A — Chế độ I2VA: Clip UGC Cầm Tay Nghiêng Nhẹ Đón Sáng (1 ảnh đầu → 5 giây)
*(Thay phần trong `[...]` bằng mô tả sản phẩm thực tế của bạn)*

```text
For the target video, at 0.00 seconds into the target video, <Picture 1> (from [Shot 1]) is fully referenced.

integrated_multimodal_description:
[Shot 1] Live-action, authentic handheld smartphone UGC product showcase. The shot opens exactly on <Picture 1>, framing the [e.g., matte white 30ml serum bottle with silver dropper cap and black printed logo "BRAND"] held naturally in a woman's right hand in the upper-center of the vertical frame against the sunlit bedroom background. The product's exact cylindrical silhouette, cap proportions, surface texture, color palette, and printed "BRAND" typography remain visually consistent and undistorted. Her wrist tilts the product gently by 15 degrees toward the window light so soft natural highlights glide smoothly across the packaging, while her index finger lightly taps the side of the bottle once. The camera pushes in with small amplitude at slow speed with subtle natural handheld breathing, keeping the label crisp in focus.

overall_soundscape:
Quiet natural indoor room tone, a soft crisp fingernail tap on the bottle surface, and subtle sleeve fabric movement synchronized with her wrist tilt.

non_diegetic_music: N/A
```

---

### Mẫu 2B — Chế độ FL2VA: Nối Khung Đầu & Khung Cuối (Giữ Logo Nét Nhất!)
*(Nạp `start_frame.png` vào `Picture 1`, `end_frame.png` vào `Picture 2`, thời lượng `5.00 giây`)*

```text
How the reference pictures align with the target video — Picture 1 (from Shot 1) aligns with the 0.00-second mark of the target video; Picture 2 (from Shot 1) aligns with the 5.00-second mark of the target video.

integrated_multimodal_description:
[Shot 1] Live-action, commercial lifestyle product b-roll. The shot begins in the exact framing and warm window lighting established by Picture 1, showing the [e.g., matte black wireless mouse with metallic scroll wheel and "BRAND" mark] resting on the textured wooden desk. The camera pushes in and arcs slightly right with small amplitude at slow speed while a right hand smoothly enters from the side with natural five-finger anatomy and gently rests on the top surface, converging naturally into the exact hand position, camera angle, lighting, and sharp label details established by Picture 2 at the end of the shot.

overall_soundscape:
Warm quiet room ambience, subtle skin movement, and a soft muted contact sound as fingertips rest gently on the product near the end of the shot.

non_diegetic_music: N/A
```

---

### Mẫu 2C — Chế độ Ref2VA: Ghép Sản Phẩm (`<Picture 1>`) + Người Mẫu (`<Picture 2>`)
*(Bắt buộc giữ đúng thứ tự **6 trường** và dùng marker **`fully_preserved`**)*

```text
subject_definitions:
<Subject 1> is the exact commercial product shown in <Picture 1>: [mô tả chi tiết hình dáng, kích thước cầm tay, màu sắc, chất liệu, nắp và chữ "BRAND" trên nhãn].
<Subject 2> is the young Vietnamese female creator in <Picture 2>, wearing a casual beige knit top in a bright sunlit living room.

summary:
[reference generation] The target video creates a vertical smartphone UGC clip where <Subject 2> holds <Subject 1> in the upper-center safe zone and presents it naturally to the camera while preserving exact product geometry and label clarity.

retention_analysis:
<Subject 1> (appears in [Shot 1]): fully_preserved - the product retains its exact silhouette, realistic palm-sized scale, colors, cap structure, and readable "BRAND" label design from <Picture 1>.
<Subject 2> (appears in [Shot 1]): fully_preserved - the creator retains her facial identity, hairstyle, beige knit top, and sunlit living room setting from <Picture 2>.

detailed_description:
The target video uses realistic vertical smartphone UGC videography with soft natural daylight, authentic skin texture, and sharp product focus.
[Shot 1] A vertical medium close-up frames <Subject 2> smiling warmly with closed lips in her sunlit living room while holding <Subject 1> clearly at chest height in the center-upper frame. She brings <Subject 1> slightly closer toward the lens so focus locks crisply onto the preserved "BRAND" label and surface finish, gives a gentle approving nod, and tilts the item by 10 degrees to catch soft window highlights. The camera pushes in with small amplitude at slow speed with subtle handheld realism.

overall_soundscape:
Clean indoor room tone, soft knit fabric rustle as she raises her arm, and subtle finger contact against the product packaging.

non_diegetic_music: N/A
```

---

## 4. 6 Lỗi Khó Nhất Khi Làm Video AFF Từ Ảnh & Cách Sửa Triệt Để

| Lỗi thực tế | Nguyên nhân | Cách khắc phục triệt để |
| :--- | :--- | :--- |
| **1. Chữ nhỏ / Logo trên bao bì bị nhòe, chảy chữ ("Text Melting")** | Nén GGUF Q3/Q4 + xoay sản phẩm góc lớn (> 40°) khiến model phải tự đoán và vẽ lại chữ. | - Giữ góc nghiêng/xoay **dưới 15–20°** + luôn dùng `with small amplitude at slow speed`.<br>- Ưu tiên chế độ **FL2VA** (khóa cả ảnh đầu và ảnh cuối đều có logo nét).<br>- Với bao bì dày đặc chữ nhỏ tiếng Việt: dùng chuyển động **zoom thẳng nhẹ (`push-in`)** thay vì xoay ngang. |
| **2. Sai kích thước sản phẩm ("Scale Shift" — lọ 30ml to như chai nước suối)** | Ảnh tách nền không có vật đối chiếu tỷ lệ *(dễ vi phạm chính sách mô tả sai sản phẩm của TikTok Shop)*. | - Luôn tạo ảnh Bước 1 có **bàn tay cầm** hoặc đặt cạnh vật quen thuộc (tách cà phê, điện thoại, bàn phím) và ghi rõ dung tích thực tế (`compact 30ml bottle fitting comfortably inside her palm`). |
| **3. Bàn tay cầm sản phẩm bị thừa ngón, xuyên qua chai** | Bắt model video tự sinh bàn tay thò vào cầm nắm phức tạp từ hư không. | - Cho bàn tay **cầm sẵn sản phẩm ngay từ Bước 1 (P-H3-Image)**. Tạo 4 ảnh tĩnh chọn tấm bàn tay 5 ngón chuẩn nhất rồi mới chuyển sang I2VA làm chuyển động nghiêng cổ tay nhẹ. |
| **4. Nhìn giống CGI quảng cáo giả (khách lướt bỏ trong 1 giây đầu)** | Dùng từ khóa `8k, hyper-detailed, 3D render, studio luxury` làm da và vỏ hộp bóng nhựa. | - Đổi sang từ khóa **UGC đời thực**: `authentic handheld smartphone UGC, natural window daylight, subtle handheld micro-movement, lived-in background`.<br>- Giữ đúng **6–8 steps, CFG = 1.0, scheduler `simple`**. |
| **5. Sản phẩm bị chữ phụ đề & Giỏ hàng TikTok che khuất** | Đặt sản phẩm ở 1/3 dưới màn hình hoặc sát rìa phải. | - Luôn khóa vị trí sản phẩm bằng cụm `in the upper-center of the 9:16 vertical frame, leaving clean negative space in the bottom quarter`. |
| **6. Kênh bị đánh giá nội dung AI lặp lại / kém tương tác** | Đăng 1 clip 5s tĩnh hoặc để giọng AI lỗi dấu tiếng Việt. | - Ghép **3 clip 4–5s khác góc** (UGC cầm tay + Macro chi tiết + Lifestyle) thành video 12–15s + chèn text hook 2s đầu + lồng giọng đọc tiếng Việt thật hoặc TTS Việt chuẩn. |
