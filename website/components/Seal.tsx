type SealProps = {
  size?: number;
  className?: string;
  muted?: boolean;
  stamp?: boolean;
  stamped?: boolean;
  "aria-hidden"?: boolean | "true" | "false";
};

/** Concentric ring + tick — wax-seal signature glyph. Use sparingly. */
export function Seal({
  size = 24,
  className = "",
  muted = false,
  stamp = false,
  stamped = false,
  "aria-hidden": ariaHidden = true,
}: SealProps) {
  const stroke = muted ? "var(--text-muted)" : "var(--seal)";
  return (
    <svg
      width={size}
      height={size}
      viewBox="0 0 32 32"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      className={`${stamp ? "seal-stamp" : ""} ${stamped ? "is-inview" : ""} ${className}`}
      aria-hidden={ariaHidden}
    >
      <circle cx="16" cy="16" r="13" stroke={stroke} strokeWidth="2" />
      <circle cx="16" cy="16" r="8" stroke={stroke} strokeWidth="1.5" />
      <path
        d="M16 8v8l5 3"
        stroke={stroke}
        strokeWidth="1.75"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
    </svg>
  );
}
