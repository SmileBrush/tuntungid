export const STAGES = [
  { number: 1, name: "Konsultasi dan Diagnosa", note: "Audit alur kerja Anda" },
  { number: 2, name: "Prototype (MVP)", note: "Desain dan kerangka data" },
  { number: 3, name: "Eksekusi dan Development", note: "Aplikasi dibangun" },
  { number: 4, name: "Testing dan Training", note: "Uji bersama tim Anda" },
  { number: 5, name: "Serah Terima dan Garansi", note: "Garansi bug 30 hari" }
];

export const REQUEST_KINDS = {
  revisi: "Revisi",
  fitur_tambahan: "Fitur Tambahan"
};

export const REQUEST_STATUSES = {
  baru: "Baru",
  diproses: "Diproses",
  selesai: "Selesai"
};

export function normalizeStage(value) {
  const n = Number.parseInt(value, 10);
  if (Number.isNaN(n)) return 1;
  return Math.min(5, Math.max(1, n));
}

export function stageState(stageNumber, currentStage) {
  if (stageNumber < currentStage) return "done";
  if (stageNumber === currentStage) return "active";
  return "pending";
}

export function stageLabel(currentStage) {
  const s = STAGES[normalizeStage(currentStage) - 1];
  return `Tahap ${s.number} dari 5: ${s.name}`;
}

export function formatDate(iso) {
  if (!iso) return "Belum ditentukan";
  const d = new Date(`${iso}T00:00:00`);
  if (Number.isNaN(d.getTime())) return "Belum ditentukan";
  return d.toLocaleDateString("id-ID", { day: "numeric", month: "short", year: "numeric" });
}

