# Khon Tid Buak Character Quiz — recovered source

โฟลเดอร์นี้กู้คืนจากเวอร์ชันที่เผยแพร่อยู่บน Netlify เมื่อวันที่ 2 ตุลาคม 2026

## ไฟล์หลัก

- `index.html` — เวอร์ชัน standalone ที่แก้ไขและ deploy ได้โดยตรง ไม่ต้องใช้ runtime ของ bundle เดิม
- `bundled-template.html` — template ที่แยกตรงจาก bundle เดิม เก็บไว้ใช้อ้างอิง
- `assets/` — รูปภาพ ฟอนต์ และ runtime เดิมที่ฝังอยู่ในหน้าเว็บ

## เปิดดูบนเครื่อง

เปิด `index.html` โดยตรงได้ หรือรัน local server จากโฟลเดอร์นี้:

```powershell
python -m http.server 8765
```

แล้วเปิด `http://127.0.0.1:8765/`

## Deploy ขึ้น Netlify

นำทั้งโฟลเดอร์ `tidbuak-character-recovered` ไป deploy ได้เลย โดยให้ `index.html` อยู่ที่ root ของ site

## หมายเหตุ

ไฟล์ `index.html` รวม CSS และ JavaScript ของ Quiz/มินิเกมไว้ในไฟล์เดียว ส่วนรูปภาพและฟอนต์อ้างอิงแบบ relative path จาก `assets/` จึงไม่ต้องพึ่ง CDN ภายนอก
