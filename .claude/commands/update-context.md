Run the session-end update procedure defined in CLAUDE.md ("Session-end update").

Follow every step exactly:
1. Read the current STATUS.md first (do not regenerate from memory).
2. Append completed/discovered items to DONE.md — append only, dated, FULL detail (do not compress a pasted digest).
3. Rewrite STATUS.md whole; delete done items; keep under ~100 lines.
4. Update a docs/ file only if an area changed materially.
5. Run ./build-context.sh.
6. Commit all changes in one commit (`context: <date> — <headline>`) AND push.
7. Show me `git diff --stat` before committing and wait for my yes. After pushing, tell me verbatim: "Now drag PROJECT-CONTEXT.md into project knowledge (replace the old one)."

If a digest is included below, fold it into steps 2–3 in full. If not, base the update on what we did in this repo session.

DIGEST: $ARGUMENTS
