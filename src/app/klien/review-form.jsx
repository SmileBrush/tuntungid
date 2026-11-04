"use client";

import { useActionState, useState } from "react";
import { submitReviewAction } from "./actions.js";
import { StarIcon } from "../../components/star-rating.jsx";

export function ReviewForm({ projectId, existingReview }) {
  const [state, formAction, pending] = useActionState(submitReviewAction, null);
  const [selectedRating, setSelectedRating] = useState(existingReview?.rating || 5);

  return (
    <form action={formAction} className="space-y-4" noValidate>
      <input type="hidden" name="project_id" value={projectId} />
      <input type="hidden" name="rating" value={selectedRating} />

      <div>
        <label className="block text-sm font-semibold mb-2">Penilaian Bintang (1 - 5)</label>
        <div className="flex items-center gap-2" role="group" aria-label="Pilih rating bintang">
          {[1, 2, 3, 4, 5].map((star) => {
            const isFilled = star <= selectedRating;
            return (
              <button
                key={star}
                type="button"
                onClick={() => setSelectedRating(star)}
                className={`min-h-[44px] min-w-[44px] rounded-xl flex items-center justify-center transition-colors ${
                  isFilled ? "bg-gold text-ink" : "bg-soft text-ink-2"
                }`}
                aria-label={`Beri ${star} bintang`}
              >
                <StarIcon filled={isFilled} className="size-5" />
              </button>
            );
          })}
          <span className="text-sm font-semibold ml-2 tabular-nums">{selectedRating} dari 5 Bintang</span>
        </div>
      </div>

      <div>
        <label htmlFor="feedback" className="block text-sm font-semibold mb-1.5">
          Ulasan &amp; Kesan Kerja Sama
        </label>
        <textarea
          id="feedback"
          name="feedback"
          rows={4}
          required
          defaultValue={existingReview?.feedback || ""}
          placeholder="Ceritakan bagaimana aplikasi ini membantu efisiensi dan alur kerja bisnis Anda..."
          className="w-full rounded-xl bg-soft px-3 py-2.5 text-base"
        />
      </div>

      {existingReview && (
        <div className="p-3 rounded-xl bg-soft text-xs text-ink-2">
          <span>Status ulasan Anda: </span>
          <strong className="text-ink">
            {existingReview.is_published
              ? "Disetujui Admin (Tampil di Landing Page)"
              : "Menunggu Peninjauan Admin"}
          </strong>
        </div>
      )}

      {state?.error && (
        <p role="alert" className="rounded-xl bg-danger-bg p-3 text-sm font-medium text-danger">
          {state.error}
        </p>
      )}

      {state?.ok && (
        <p role="status" className="rounded-xl bg-ok-bg p-3 text-sm font-medium">
          {state.message}
        </p>
      )}

      <button
        type="submit"
        disabled={pending}
        className="min-h-[48px] px-5 rounded-xl bg-brand text-white font-semibold hover:bg-brand-hover"
      >
        {pending ? "Menyimpan Ulasan..." : existingReview ? "Perbarui Ulasan" : "Kirim Ulasan Resmi"}
      </button>
    </form>
  );
}
