# แผนปรับสถาปัตยกรรมใหม่: Khon Tid Buak Activity Game

## 1. วิสัยทัศน์และเป้าหมาย

สร้างประสบการณ์กิจกรรมบนมือถือที่พนักงานโรงงานเปิดผ่าน QR code เล่นควิซและมินิเกมได้ง่าย รวดเร็ว รองรับหลายภาษา และให้ผู้จัดกิจกรรมเห็นภาพรวมการเข้าร่วมได้ โดยออกแบบระบบและโค้ดใหม่ให้ดูแลต่อได้ ไม่ยึดโครงสร้างเดิมที่เกิดจากการกู้คืน

เป้าหมายรอบแรกคือ **กิจกรรมหนึ่งงาน ผู้เล่นจำนวนมาก เล่นแบบไม่ต้องกรอกข้อมูลส่วนตัว และมีหน้าจอผู้ดูแลสำหรับดูจำนวนผู้เล่น/ผลรวม** ยังไม่ถือว่า leaderboard, ระบบรางวัลอัตโนมัติ หรือการจัดการหลายโรงงานเป็น requirement จนกว่าจะยืนยัน

## 2. สิ่งที่พบในของเดิม

- `index.html` รวม UI, เกม, scoring และคำแปลไทย อังกฤษ เมียนมา และลาวไว้ในไฟล์เดียว
- `app.py` เป็น static file server ไม่ใช่ application backend และ bind ที่ `0.0.0.0`
- ไม่มี schema, API, authentication, automated tests หรือขั้นตอน deploy ระบบ backend ในปัจจุบัน
- มี assets และเนื้อหาจากเวอร์ชันกู้คืนที่นำมาใช้เป็น reference หรือย้ายเฉพาะส่วนที่ผ่านการตรวจสอบได้

สิ่งเหล่านี้ใช้เป็นข้อมูลตั้งต้นเท่านั้น ไม่ใช่ข้อจำกัดของสถาปัตยกรรมใหม่

## 3. สถาปัตยกรรมเป้าหมายที่แนะนำ

### Frontend

- **React + TypeScript + Vite** เป็นเว็บแอปแบบ SPA: เหมาะกับประสบการณ์โต้ตอบบนมือถือ ไม่ต้องใช้ server-side rendering หรือ SEO แบบเว็บไซต์เนื้อหา และ deploy เป็น static assets ได้
- ใช้ **React Router** แยกเส้นทางผู้เล่นและผู้ดูแล เช่น `/e/:eventSlug` และ `/admin` โดยไม่แยกเป็นหลายแอปใน MVP
- ใช้ **Tailwind CSS** สำหรับ layout/responsive design และทำหน้าจอผู้เล่นให้เน้นการแตะ เล่นง่ายบนมือถือ ส่วนหน้า admin เน้นอ่านตารางและข้อมูล
- ใช้ **i18next/react-i18next** แยกข้อความเป็น resource files สำหรับ `th`, `en`, `my`, `lo`; ห้ามฝัง translation ก้อนใหญ่รวมกับ game logic
- ใช้ React state/context สำหรับ state ที่จำเป็นใน MVP; เพิ่ม state library เมื่อมีปัญหาการส่ง state ข้าม feature จริงเท่านั้น
- เกมทั้งหกเริ่มจาก React/CSS และ game logic แบบ pure TypeScript แยกจาก UI ยังไม่ต้องใช้ game engine จนกว่าจะมีเกมที่ต้องการ animation/physics ซับซ้อน

### Backend และข้อมูล

- ใช้ **Supabase** เป็น managed backend: PostgreSQL, Auth, Row Level Security (RLS), Edge Functions และ Realtime เฉพาะส่วนที่ต้องการอัปเดตสด
- เก็บ schema และการเปลี่ยนฐานข้อมูลเป็น SQL migrations ใน repository; สร้าง TypeScript database types จาก schema เพื่อให้ frontend ใช้ชนิดข้อมูลชุดเดียวกัน
- Frontend ติดต่อ Supabase ด้วย project URL และ public anon/publishable key เท่านั้น ห้ามใส่ `service_role` key หรือ secret ใน client bundle
- ใช้ Supabase Edge Functions สำหรับการสร้าง session, ส่งผลเกม/ควิซที่ต้องตรวจสอบ และงานที่ต้องใช้ privileged access; อย่าเชื่อคะแนนจาก client โดยตรงหากคะแนนใช้ตัดสินรางวัล
- เปิด RLS ทุกตารางที่ client เข้าถึง และกำหนด policy แบบ least privilege ก่อนเชื่อม frontend
- เก็บภาพ/ฟอนต์คงที่ใน `public/` ของเว็บ; ใช้ Supabase Storage เฉพาะเมื่อผู้ดูแลต้องอัปโหลดรูปหรือสื่อสำหรับ event ผ่านระบบ

### โครงสร้างระบบโดยรวม

```text
ผู้เล่นบนมือถือ ── QR / URL ──> React + Vite Web App
									  │
									  ├── Supabase Auth (ผู้เล่นแบบไม่ระบุตัวตน / ผู้ดูแล)
									  ├── Supabase Edge Functions (สร้าง session / ส่งผลที่ตรวจสอบ)
									  └── PostgreSQL + RLS (event / content / sessions / aggregate results)

ผู้ดูแลกิจกรรม ──> /admin ── Auth ──> ข้อมูลเฉพาะ event ที่ได้รับสิทธิ์
```

## 4. โครงสร้าง repository ที่เสนอ

เริ่มเป็น repository เดียว ไม่จำเป็นต้องทำ monorepo สำหรับแอปขนาดนี้

```text
.
├── src/
│   ├── app/                 # router, providers, app shell
│   ├── routes/              # player event route และ admin routes
│   ├── features/
│   │   ├── events/          # event lookup, join flow, event settings
│   │   ├── quiz/            # quiz UI, answer flow, result mapping
│   │   ├── games/           # game registry และเกมแยกตาม character
│   │   ├── results/         # บันทึกผลและสรุปผลฝั่งผู้เล่น
│   │   └── admin/           # จัดการ event/content และ dashboard
│   ├── components/          # UI components ที่ใช้ร่วมกัน
│   ├── i18n/                # config และ th/en/my/lo resources
│   ├── lib/                 # supabase client, validation, utilities
│   └── styles/              # global styles และ design tokens
├── public/                  # logo, fonts, static images
├── supabase/
│   ├── migrations/          # schema, indexes, RLS policies
│   ├── seed.sql             # development/demo content เท่านั้น
│   └── functions/           # Edge Functions
├── tests/                   # domain, component และ integration tests
├── .env.example             # ชื่อตัวแปรเท่านั้น ห้ามใส่ secret จริง
├── AGENTS.md                # ปรับคำสั่ง agent ให้ตรง stack ใหม่
└── README.md                # setup, run, test, deploy และ Supabase setup
```

ไม่ย้ายทุกไฟล์เดิมตามไปโดยอัตโนมัติ: เลือกย้ายเฉพาะข้อความ/ภาพ/คำถาม/กติกาเกมที่เจ้าของยืนยันว่าถูกต้อง ส่วน `bundled-template.html` และไฟล์ runtime ที่กู้คืนให้เก็บเป็น archive/reference แยกจาก source ใหม่

## 5. ข้อมูลและการเข้าถึง

### ตารางเริ่มต้นที่เสนอ

- `events`: slug, ชื่อ, สถานะ, วันจัดงาน, locale ที่เปิดใช้ และค่าการตั้งค่าระดับ event
- `event_admins`: ความสัมพันธ์ระหว่าง event กับบัญชีผู้ดูแล
- `characters`: character key, สี/ภาพ และ metadata ที่ไม่เปลี่ยนตามภาษา
- `localized_content` หรือชุดตาราง content ที่มี locale: คำถาม ตัวเลือก คำอธิบาย และข้อความเกม
- `game_sessions`: event, anonymous participant/session, locale, สถานะ, เวลาเริ่ม/จบ และผลลัพธ์ที่จำเป็น
- `quiz_answers`: เพิ่มเฉพาะเมื่อทีมต้องการวิเคราะห์คำตอบรายข้อจริง ๆ; ค่าเริ่มต้นไม่เก็บคำตอบดิบ
- `game_results`: game key, score, duration และข้อมูลสรุปที่จำเป็น โดยแยกคะแนนที่ client ส่งมากับคะแนนที่ server ตรวจแล้วให้ชัดเจน

กำหนด foreign keys, constraints, indexes, retention และ unique/idempotency rules ใน migrations ก่อนเปิดใช้งานจริง หลีกเลี่ยงการเก็บชื่อพนักงาน, รหัสพนักงาน หรือข้อมูลระบุตัวบุคคลใน MVP

### รูปแบบการยืนยันตัวตน

- ผู้เล่น: ใช้ Supabase anonymous sign-in หรือ session token ที่ออกโดย Edge Function เพื่อผูก session โดยไม่บังคับสมัครสมาชิก
- ผู้ดูแล: ใช้บัญชีที่เชิญ/อนุมัติเท่านั้น; ห้ามเปิด public admin registration
- RLS ต้องทำให้ผู้เล่นอ่านได้เฉพาะ event ที่เผยแพร่และเขียนได้เฉพาะ session ของตนเอง ส่วน admin เข้าถึงได้เฉพาะ event ที่มีสิทธิ์
- หากมี leaderboard หรือรางวัลที่มีมูลค่า ต้องออกแบบ server-authoritative score/anti-cheat เพิ่มก่อนเปิดใช้; คะแนนที่คำนวณจาก browser อย่างเดียวแก้ไขได้

## 6. ประสบการณ์ใช้งาน MVP

### ผู้เล่น

1. สแกน QR ที่ระบุ event และเปิดหน้า join โดยไม่ต้องค้นหางานเอง
2. เลือกภาษา หรือใช้ภาษาที่บันทึกไว้ในอุปกรณ์
3. เริ่มควิซ ตอบคำถาม ดูผล character และเล่นเกมที่เกี่ยวข้อง
4. ส่งผล session แบบไม่ระบุตัวตนเมื่อออนไลน์ และแสดงสถานะชัดเจนหากส่งไม่สำเร็จ
5. เริ่มใหม่ได้โดยไม่เห็นหรือแก้ผลของผู้เล่นคนอื่น

### ผู้จัดกิจกรรม

- เข้าหน้า admin แบบ authenticated เพื่อเลือก event ที่ได้รับสิทธิ์
- ดูจำนวนผู้เข้าร่วม จำนวน session ที่จบ สัดส่วนภาษา และผลรวมตาม character/game
- export เฉพาะข้อมูลที่จำเป็นต่อการสรุปกิจกรรม; หลีกเลี่ยงการ export ข้อมูลรายบุคคลหากไม่มี requirement
- การแก้คำถาม/คำแปลผ่าน UI เป็นความสามารถระยะถัดไป ไม่จำเป็นต้องทำก่อน MVP หากเนื้อหายังเปลี่ยนไม่บ่อย

## 7. ความเสี่ยงและข้อกำหนดหน้างาน

- **เครือข่ายโรงงาน/สถานที่จัดงาน:** ยืนยันว่าอุปกรณ์มี internet access ถึง Supabase ได้ และทดสอบจำนวนผู้เล่นพร้อมกันตามตัวเลขจริงก่อนวันงาน
- **การขาดการเชื่อมต่อ:** MVP ต้องตรวจ connection และแจ้งผู้ใช้เมื่อส่งผลไม่ได้; การเล่น offline พร้อม sync ภายหลังเป็นงานแยก เพราะต้องจัดการ queue, duplicate submissions และข้อมูลหมดอายุ
- **คะแนนและของรางวัล:** browser เป็น client ที่แก้ไขได้ ห้ามใช้คะแนน client เป็นหลักฐานรับรางวัลที่ต้องมีความยุติธรรมโดยไม่มี server validation
- **ข้อมูลพนักงาน:** ค่าเริ่มต้นไม่เก็บข้อมูลระบุตัวบุคคล กำหนด retention และลบข้อมูล event ตามนโยบายองค์กร
- **หลาย event/โรงงาน:** ใส่ `event_id` ในข้อมูลที่เกี่ยวข้องตั้งแต่ต้น แต่ยังไม่ทำ multi-tenant administration ซับซ้อนเกิน MVP
- **การเข้าถึงบนมือถือ:** ออกแบบ touch targets, ตัวอักษรหลายภาษา, ความเร็วโหลด และอุปกรณ์หน้าจอเล็กเป็นเกณฑ์หลัก
- **ไฟล์ server เดิม:** `app.py` ไม่ใช้เป็น production backend; ระหว่างพัฒนาใช้ Vite dev server และ production ใช้ static hosting ที่เชื่อมกับ Supabase

## 8. Roadmap

### Phase 0: Product decisions และ acceptance criteria

- ระบุผู้ใช้งานและ flow จริงของผู้เล่น/ผู้จัดกิจกรรม
- ยืนยันว่าต้องมี leaderboard, รางวัล, export, การจัดการ content และ event หลายงานหรือไม่
- ยืนยันจำนวนผู้เล่นพร้อมกันโดยประมาณ, อุปกรณ์/เบราว์เซอร์เป้าหมาย และคุณภาพเครือข่าย ณ สถานที่จัดงาน
- ยืนยันว่าจะเก็บข้อมูลอะไร ระยะเวลาเก็บเท่าไร และผู้มีสิทธิ์ดูผลเป็นใคร
- ตรวจสอบข้อความ คำถาม character และกติกาเกมทั้ง 4 ภาษา โดยใช้ของเดิมเป็น reference ไม่ใช่ข้อเท็จจริงที่ต้องรับช่วงโดยไม่ตรวจ

**ผลลัพธ์:** MVP scope, acceptance criteria และการตัดสินใจเรื่องข้อมูล/เครือข่ายที่เจ้าของผลิตภัณฑ์อนุมัติ

### Phase 1: Foundation และ design system

- สร้าง React + TypeScript + Vite app พร้อม lint, format, typecheck และ test scripts
- วาง routing, design tokens, responsive shell, i18n และ Supabase client
- สร้าง environment แยก local/staging/production และ `.env.example`
- ปรับ `AGENTS.md` ซึ่งปัจจุบันมีข้อกำหนดแบบ static-only ให้สอดคล้องกับ architecture ใหม่ก่อนเริ่ม implementation

**ผลลัพธ์:** app scaffold ที่รันและตรวจคุณภาพได้ ไม่มีข้อมูลลับอยู่ใน repository

### Phase 2: Supabase schema และ security

- สร้าง migrations สำหรับ events, content, sessions และสิทธิ์ admin
- กำหนด indexes, constraints, data retention และ RLS policies
- ใช้ Supabase local development สำหรับ migration/seed และตรวจสิทธิ์ผู้เล่นกับ admin แยกบทบาท
- เพิ่ม Edge Function เฉพาะ operation ที่ต้องตรวจข้อมูลหรือ privileged access

**ผลลัพธ์:** migrations ทำซ้ำได้ และมี tests ยืนยันว่า role หนึ่งอ่าน/เขียนข้ามขอบเขตของตนไม่ได้

### Phase 3: Player experience

- ทำ event join/QR route, language selection และ anonymous session
- พัฒนาควิซและผล character จาก content model ที่ยืนยันแล้ว
- แยก game logic ต่อเกม และทำมินิเกมทั้งหกพร้อม timer, reset และ touch behavior
- บันทึกเฉพาะ session/result ที่ตกลงไว้ พร้อม handling การส่งซ้ำและ network failure

**ผลลัพธ์:** ผู้เล่นทำ flow จบได้บนมือถือในทุกภาษาที่กำหนด โดยไม่ต้องมีบัญชีส่วนตัว

### Phase 4: Admin และ activity reporting

- ทำ admin login และ event-scoped authorization
- แสดง aggregate metrics ที่ต้องใช้จริงและ export แบบจำกัดข้อมูล
- เพิ่ม realtime เฉพาะเมื่อผู้จัดงานต้องเห็นยอดสด; หากไม่จำเป็นให้ใช้ query/refresh ตามช่วงเวลา

**ผลลัพธ์:** ผู้จัดกิจกรรมดูภาพรวมได้โดยไม่มีสิทธิ์เกินหน้าที่

### Phase 5: QA, load readiness และ rollout

- Unit tests สำหรับ scoring/game rules/i18n mapping; component tests สำหรับ flow สำคัญ
- Integration tests สำหรับ Supabase migrations, Edge Functions และ RLS
- วัดเวลาโหลดและทดสอบ concurrent load ตามตัวเลขจาก Phase 0
- ทดลองใช้งานบนอุปกรณ์จริงและเครือข่ายจริง พร้อม fallback เมื่อ internet ใช้งานไม่ได้
- ตั้ง staging/production Supabase แยกกัน, secrets ในระบบ deploy, logging ที่ไม่เก็บ PII เกินจำเป็น และขั้นตอน rollback

**ผลลัพธ์:** ผ่าน acceptance criteria, security checks และ rehearsal ก่อนเปิดให้พนักงานใช้งานจริง

## 9. Definition of Done สำหรับ MVP

- ผู้เล่นเปิดจาก QR บนมือถือ ทำควิซและเกมจบได้โดยไม่ต้องสร้างบัญชีส่วนตัว
- รองรับ locale ที่เจ้าของยืนยัน โดยข้อความและเนื้อหาไม่ตกหล่นใน flow หลัก
- event แยกข้อมูลจากกันและ RLS ป้องกันการอ่าน/เขียนข้อมูลข้าม session หรือ event
- ไม่มี `service_role` key หรือ secret ใน frontend, git history หรือไฟล์ตัวอย่าง
- admin ต้อง authenticate และเห็นเฉพาะ event ที่ได้รับสิทธิ์
- แสดงสถานะ/ข้อผิดพลาดที่ผู้ใช้เข้าใจได้เมื่อ Supabase หรือเครือข่ายไม่พร้อม
- automated checks และ manual device/network checklist ผ่าน โดยรายงานผลตามจริง

## 10. สมมติฐานเริ่มต้นที่ควรยืนยัน

1. MVP ไม่เก็บชื่อหรือรหัสพนักงาน และไม่ทำ leaderboard สาธารณะ
2. เก็บเพียง event/session, locale, character result, score และเวลาที่จำเป็น โดยกำหนดวันลบข้อมูลก่อน production
3. ผู้เล่นต้องมี internet access ระหว่างเล่น; offline queue ยังไม่รวมใน MVP
4. ผู้ดูแลเป็นกลุ่มเล็กที่ได้รับเชิญ ไม่เปิดสมัคร admin เอง
5. ภาษาเริ่มต้นยังคง Thai, English, Myanmar และ Lao จนกว่าจะมีการยืนยันเปลี่ยนแปลง

หากข้อใดไม่ตรง โดยเฉพาะเรื่องรางวัล, leaderboard, การระบุตัวพนักงาน หรือ offline operation ต้องปรับ data model และ security design ก่อนเริ่มทำ feature ส่วนนั้น
