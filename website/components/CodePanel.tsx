import { CopyButton } from "@/components/CopyButton";

export function CodePanel({
  label,
  code,
  note,
  noteHref,
}: {
  label: string;
  code: string;
  note?: string;
  noteHref?: string;
}) {
  return (
    <div>
      <p className="mb-3 font-body text-sm font-medium text-text">{label}</p>
      <div className="relative border border-border bg-surface">
        <div className="absolute right-2 top-2 z-10">
          <CopyButton text={code} />
        </div>
        <pre className="overflow-x-auto px-4 py-4 pr-20 font-mono text-xs leading-relaxed text-text sm:text-sm">
          <code>{code}</code>
        </pre>
      </div>
      {note ? (
        <p className="mt-2 text-sm text-text-muted">
          {noteHref ? (
            <>
              {note.replace(noteHref, "").trim()}{" "}
              <a href={`mailto:${noteHref}`} className="text-seal hover:text-seal-hover">
                {noteHref}
              </a>
            </>
          ) : (
            note
          )}
        </p>
      ) : null}
    </div>
  );
}
