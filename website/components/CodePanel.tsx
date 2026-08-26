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
    <div className="min-w-0">
      <div className="code-shell overflow-hidden">
        <div className="flex items-center justify-between gap-3 border-b border-border px-4 py-2.5">
          <p className="min-w-0 truncate font-body text-sm font-medium text-text">
            {label}
          </p>
          <div className="shrink-0">
            <CopyButton text={code} />
          </div>
        </div>
        <pre className="overflow-x-auto px-4 py-4 font-mono text-xs leading-relaxed text-text sm:text-sm">
          <code>{code}</code>
        </pre>
      </div>
      {note ? (
        <p className="mt-2 text-sm leading-relaxed text-text-muted">
          {noteHref ? (
            <>
              {note.replace(noteHref, "").trim()}{" "}
              <a
                href={`mailto:${noteHref}`}
                className="break-all text-seal hover:text-seal-hover"
              >
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
