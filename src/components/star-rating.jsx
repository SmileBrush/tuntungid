export function StarIcon({ filled = true, className = "size-5" }) {
  return (
    <svg
      viewBox="0 0 24 24"
      fill={filled ? "currentColor" : "none"}
      stroke="currentColor"
      strokeWidth={filled ? "0" : "1.5"}
      strokeLinecap="round"
      strokeLinejoin="round"
      className={className}
      aria-hidden="true"
    >
      <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2" />
    </svg>
  );
}

export function StarRatingDisplay({ rating = 5, className = "flex items-center gap-1 text-gold" }) {
  const stars = [1, 2, 3, 4, 5];
  return (
    <div className={className} aria-label={`Rating ${rating} dari 5 bintang`}>
      {stars.map((n) => (
        <StarIcon key={n} filled={n <= rating} className="size-4" />
      ))}
    </div>
  );
}
