# === Build Stage (Tahap Build) ===
FROM node:20-bookworm-slim AS builder
WORKDIR /app

ENV NEXT_TELEMETRY_DISABLED=1

COPY package*.json ./

# --- PERBAIKAN UTAMA ---
# Menginstal 'build-essential'. Paket ini berisi kumpulan library C/C++
# yang dibutuhkan oleh banyak native module, termasuk lightningcss,
# dan merupakan solusi paling andal untuk error "Cannot find module...".
RUN apt-get update && apt-get install -y libc6 build-essential --no-install-recommends && rm -rf /var/lib/apt/lists/*

# Install dependencies secara konsisten dari lock file
RUN npm ci --no-audit --no-fund

# Salin sisa source code
COPY . .

# Jalankan proses build Next.js
RUN npm run build


# === Runtime Stage (Tahap Runtime) ===
# Memulai lagi dari base image yang sama untuk keamanan dan ukuran kecil
FROM node:20-bookworm-slim
WORKDIR /app
ENV NODE_ENV=production NEXT_TELEMETRY_DISABLED=1
COPY --from=builder /app ./
EXPOSE 3000
CMD ["npm","start"]


