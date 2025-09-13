-- Prasyarat
CREATE EXTENSION IF NOT EXISTS pgcrypto;

-- =========================
-- ENUM & DOMAIN
-- =========================
DO $$
BEGIN
  IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'consumption_type') THEN
    CREATE TYPE consumption_type AS ENUM ('Food', 'Drink');
  END IF;
  IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'feeling_scale') THEN
    CREATE TYPE feeling_scale AS ENUM ('very_bad','bad','neutral','good','very_good');
  END IF;
  IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'care_role') THEN
    CREATE TYPE care_role AS ENUM ('cardiologist','nurse','clinic','family','other');
  END IF;
  IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'med_route') THEN
    CREATE TYPE med_route AS ENUM ('oral','sublingual','inhalation','topical','intravenous','other');
  END IF;
  IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'symptom_type') THEN
    CREATE TYPE symptom_type AS ENUM (
      'shortness_of_breath','chest_pain','palpitations','fatigue',
      'dizziness','swelling','weight_gain','orthopnea','other'
    );
  END IF;
END$$;

-- =========================
-- USERS & CONTACTS
-- =========================
CREATE TABLE users (
  user_id        UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  username       TEXT NOT NULL UNIQUE,
  email          TEXT NOT NULL UNIQUE,
  password_hash  TEXT NOT NULL,
  first_name     TEXT NOT NULL,
  last_name      TEXT,
  avatar_url     TEXT,
  address        TEXT,
  tel_no         TEXT,
  created_at     timestamptz NOT NULL DEFAULT now(),
  updated_at     timestamptz NOT NULL DEFAULT now()
);

-- Satu kontak darurat kustom per user
CREATE TABLE emergency_contacts (
  emergency_contact_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id              UUID NOT NULL UNIQUE REFERENCES users(user_id) ON DELETE CASCADE,
  contact_label        TEXT NOT NULL,
  contact_number       TEXT NOT NULL,
  created_at           timestamptz NOT NULL DEFAULT now(),
  updated_at           timestamptz NOT NULL DEFAULT now()
);

-- Opsi: daftar kontak care team (opsional tapi sering diminta klinisi)
CREATE TABLE care_contacts (
  care_contact_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id         UUID NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
  role            care_role NOT NULL,
  name            TEXT NOT NULL,
  phone           TEXT,
  notes           TEXT,
  created_at      timestamptz NOT NULL DEFAULT now(),
  updated_at      timestamptz NOT NULL DEFAULT now()
);

-- =========================
-- MEDICATIONS & REMINDERS
-- =========================
CREATE TABLE medications (
  medication_id  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id        UUID NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
  name           TEXT NOT NULL,
  description    TEXT,
  condition_tag  TEXT,            -- mis. "Setelah Makan"
  dosage_amount  NUMERIC(10,3),   -- mis. 5.000
  dosage_unit    TEXT,            -- mg, ml, tablet
  route          med_route,       -- cara pemberian
  active         BOOLEAN NOT NULL DEFAULT TRUE,
  start_date     DATE,
  end_date       DATE,
  created_at     timestamptz NOT NULL DEFAULT now(),
  updated_at     timestamptz NOT NULL DEFAULT now()
);

-- Jadwal fleksibel (bisa tiap hari / hari tertentu / PRN)
CREATE TABLE medication_schedules (
  schedule_id       UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  medication_id     UUID NOT NULL REFERENCES medications(medication_id) ON DELETE CASCADE,
  time_of_day       TIME NOT NULL,                -- "08:00:00"
  days_of_week      INT[],                        -- 1=Mon .. 7=Sun; NULL = tiap hari
  timezone          TEXT NOT NULL DEFAULT 'Asia/Jakarta',
  as_needed         BOOLEAN NOT NULL DEFAULT FALSE,   -- PRN
  interval_days     INT NOT NULL DEFAULT 1,           -- tiap N hari (default harian)
  remind_offset_min INT,                               -- mis. -15 utk reminder 15 mnt sebelum
  start_date        DATE,
  end_date          DATE,
  created_at        timestamptz NOT NULL DEFAULT now(),
  updated_at        timestamptz NOT NULL DEFAULT now()
);

-- Log minum obat: bisa terkait schedule (planned) atau ad-hoc
CREATE TABLE medication_logs (
  medication_log_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  medication_id     UUID NOT NULL REFERENCES medications(medication_id) ON DELETE CASCADE,
  schedule_id       UUID REFERENCES medication_schedules(schedule_id) ON DELETE SET NULL,
  planned_at        timestamptz,                     -- waktu yang seharusnya
  taken_at          timestamptz NOT NULL,            -- waktu nyata dikonfirmasi user
  taken             BOOLEAN NOT NULL DEFAULT TRUE,   -- centang/undo
  notes             TEXT,
  created_at        timestamptz NOT NULL DEFAULT now(),
  updated_at        timestamptz NOT NULL DEFAULT now()
);

-- =========================
-- HEART FAILURE DIARY
-- =========================
CREATE TABLE heart_diaries (
  diary_id     UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id      UUID NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
  diary_date   DATE NOT NULL,
  notes        TEXT,
  created_at   timestamptz NOT NULL DEFAULT now(),
  updated_at   timestamptz NOT NULL DEFAULT now(),
  CONSTRAINT uq_diary UNIQUE (user_id, diary_date)
);

-- Vital harian (boleh multi entri per hari, catat waktu ukur)
CREATE TABLE vital_signs (
  vital_id        UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  diary_id        UUID NOT NULL REFERENCES heart_diaries(diary_id) ON DELETE CASCADE,
  measured_at     timestamptz NOT NULL,
  height_cm       NUMERIC(5,1),              -- cm
  weight_kg       NUMERIC(5,2),              -- kg
  bmi             NUMERIC(4,1),
  systolic        INT,
  diastolic       INT,
  heart_rate      INT,
  oxygen_saturation INT,                     -- SpO2 %
  body_temp_c     NUMERIC(4,2),
  created_at      timestamptz NOT NULL DEFAULT now(),
  updated_at      timestamptz NOT NULL DEFAULT now(),
  -- Validasi rentang realistis
  CONSTRAINT ck_bp CHECK (
    (systolic IS NULL OR (systolic BETWEEN 50 AND 260)) AND
    (diastolic IS NULL OR (diastolic BETWEEN 30 AND 200))
  ),
  CONSTRAINT ck_hr CHECK (heart_rate IS NULL OR heart_rate BETWEEN 20 AND 250),
  CONSTRAINT ck_spo2 CHECK (oxygen_saturation IS NULL OR oxygen_saturation BETWEEN 30 AND 100),
  CONSTRAINT ck_temp CHECK (body_temp_c IS NULL OR body_temp_c BETWEEN 30 AND 45)
);

-- Konsumsi (makan/minum) + opsi dukung CHF (natrium/cairan)
CREATE TABLE daily_consumptions (
  consumption_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  diary_id       UUID NOT NULL REFERENCES heart_diaries(diary_id) ON DELETE CASCADE,
  type           consumption_type NOT NULL,
  name           TEXT NOT NULL,
  portion        TEXT,
  sodium_mg      INT,
  fluid_ml       INT,
  note           TEXT,
  occurred_at    timestamptz NOT NULL,
  created_at     timestamptz NOT NULL DEFAULT now(),
  updated_at     timestamptz NOT NULL DEFAULT now()
);

-- Aktivitas fisik
CREATE TABLE daily_activities (
  activity_id   UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  diary_id      UUID NOT NULL REFERENCES heart_diaries(diary_id) ON DELETE CASCADE,
  name          TEXT NOT NULL,
  duration_min  INT NOT NULL,
  heart_rate    INT,
  user_feeling  feeling_scale,
  note          TEXT,
  occurred_at   timestamptz NOT NULL,
  created_at    timestamptz NOT NULL DEFAULT now(),
  updated_at    timestamptz NOT NULL DEFAULT now(),
  CONSTRAINT ck_act_hr CHECK (heart_rate IS NULL OR heart_rate BETWEEN 20 AND 250)
);

-- Penilaian gejala (skala 0-4; 0=tidak ada, 4=berat)
CREATE TABLE diary_symptoms (
  symptom_id    UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  diary_id      UUID NOT NULL REFERENCES heart_diaries(diary_id) ON DELETE CASCADE,
  type          symptom_type NOT NULL,
  severity      SMALLINT NOT NULL CHECK (severity BETWEEN 0 AND 4),
  note          TEXT,
  occurred_at   timestamptz NOT NULL,
  created_at    timestamptz NOT NULL DEFAULT now(),
  updated_at    timestamptz NOT NULL DEFAULT now()
);

-- =========================
-- PATIENT EDUCATION
-- =========================
CREATE TABLE education_modules (
  module_id    UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  slug         TEXT NOT NULL UNIQUE,
  title        TEXT NOT NULL,
  description  TEXT,
  cover_url    TEXT,
  language     TEXT DEFAULT 'id',
  is_published BOOLEAN NOT NULL DEFAULT TRUE,
  created_at   timestamptz NOT NULL DEFAULT now(),
  updated_at   timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE education_sections (
  section_id   UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  module_id    UUID NOT NULL REFERENCES education_modules(module_id) ON DELETE CASCADE,
  title        TEXT NOT NULL,
  body_md      TEXT,   -- simpan markdown/HTML ringan
  "order"      INT NOT NULL DEFAULT 1,
  created_at   timestamptz NOT NULL DEFAULT now(),
  updated_at   timestamptz NOT NULL DEFAULT now()
);

-- Progress belajar per user
CREATE TABLE education_progress (
  progress_id  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id      UUID NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
  module_id    UUID NOT NULL REFERENCES education_modules(module_id) ON DELETE CASCADE,
  completed_at timestamptz,
  UNIQUE(user_id, module_id)
);
