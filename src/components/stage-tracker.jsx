import { STAGES, stageState } from "../lib/stages.js";

export function StageTracker({ stage, compact = false }) {
  return (
    <ol className={compact ? "flex gap-1.5" : "grid gap-2.5 sm:grid-cols-5"} aria-label="Tahap proyek">
      {STAGES.map((s) => {
        const state = stageState(s.number, stage);
        if (compact) {
          return (
            <li
              key={s.number}
              title={s.name}
              className={`h-2 flex-1 rounded-full ${
                state === "done" ? "bg-brand" : state === "active" ? "bg-gold" : "bg-line"
              }`}
            >
              <span className="sr-only">{`${s.name}: ${state === "done" ? "selesai" : state === "active" ? "sedang berjalan" : "belum mulai"}`}</span>
            </li>
          );
        }
        return (
          <li
            key={s.number}
            className={`rounded-2xl p-3.5 ${
              state === "active" ? "bg-ink text-white" : state === "done" ? "bg-ok-bg text-ink" : "bg-soft text-ink-2"
            }`}
          >
            <span className="text-sm font-semibold tabular-nums">
              {state === "done" ? "Selesai" : state === "active" ? "Berjalan" : `Tahap ${s.number}`}
            </span>
            <p className="font-display font-semibold text-sm mt-1 leading-snug">{s.name}</p>
          </li>
        );
      })}
    </ol>
  );
}

export function EmptyState({ title, hint, action }) {
  return (
    <div className="rounded-2xl bg-soft p-6 text-center">
      <p className="font-display font-semibold">{title}</p>
      {hint && <p className="text-sm text-ink-2 mt-1">{hint}</p>}
      {action}
    </div>
  );
}

