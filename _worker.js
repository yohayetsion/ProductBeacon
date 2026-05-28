// Cloudflare Pages advanced-mode worker.
// Purpose: programmatic 301 redirects for retired URLs. The repo's `_redirects`
// file is NOT processed on this Pages project (it is served as a static asset),
// so redirects are handled here instead. All non-redirect requests pass through
// to static assets via env.ASSETS, preserving normal site behavior.

const REDIRECTS_EXACT = {
  "/research/state-of-cyber-2026/brief.html":
    "/research/state-of-cyber-2026/pre-call-brief.html",
  "/research/state-of-cyber-2026/brief.pdf":
    "/research/state-of-cyber-2026/pre-call-brief.pdf",
};

const REPORTS_PREFIX = "/reports/state-of-cyber-2026/";
const RESEARCH_PREFIX = "/research/state-of-cyber-2026/";

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    const path = url.pathname;

    // Exact-match retired URLs (brief.* -> pre-call-brief.*)
    if (REDIRECTS_EXACT[path]) {
      return Response.redirect(url.origin + REDIRECTS_EXACT[path] + url.search, 301);
    }

    // Prefix migration: /reports/state-of-cyber-2026/* -> /research/state-of-cyber-2026/*
    if (path.startsWith(REPORTS_PREFIX)) {
      const dest = RESEARCH_PREFIX + path.slice(REPORTS_PREFIX.length);
      return Response.redirect(url.origin + dest + url.search, 301);
    }

    // Everything else: serve the static asset unchanged.
    return env.ASSETS.fetch(request);
  },
};
