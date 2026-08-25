import { GITHUB } from "@/lib/site";
import { SITE, SUPPORT } from "@/lib/content";

export function Footer() {
  return (
    <footer className="border-t border-border py-12">
      <div className="mx-auto max-w-narrow space-y-4 px-gutter text-center font-mono text-xs text-muted">
        <p>
          {SUPPORT}{" "}
          <a
            href={GITHUB.issuesNew}
            className="text-foreground hover:text-accent"
            target="_blank"
            rel="noopener noreferrer"
          >
            Issue
          </a>
          {" · "}
          <a
            href={GITHUB.discussions}
            className="text-foreground hover:text-accent"
            target="_blank"
            rel="noopener noreferrer"
          >
            Discussion
          </a>
        </p>
        <p>Early Access · MIT · v{SITE.version}</p>
      </div>
    </footer>
  );
}
