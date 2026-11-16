# Deployment setup

## OIDC authentication

Configure one OIDC provider in Streamlit secrets and register the redirect URI
with that provider. Do not commit the secrets file or provider credentials.

```toml
[auth]
redirect_uri = "https://YOUR-APP-URL/oauth2callback"
cookie_secret = "GENERATE-A-LONG-RANDOM-SECRET"

[auth.google]
client_id = "YOUR-OIDC-CLIENT-ID"
client_secret = "YOUR-OIDC-CLIENT-SECRET"
server_metadata_url = "https://accounts.google.com/.well-known/openid-configuration"

[authorization]
passcode = "ali2027"
admin_emails = ["admin@example.org"]
agent_emails = ["agent@example.org"]
collation_emails = ["collation@example.org"]

[authorization.committees]
"Committee 1: Finance & Appropriations" = ["committee1@example.org"]

[supabase]
url = "https://YOUR-PROJECT.supabase.co"
service_role_key = "YOUR-SERVER-SIDE-SERVICE-ROLE-KEY"
```

Add authorized identities to each role allowlist. Committee access is granted
only by the matching committee list; administrators can administer committee
records. The app preserves anonymous access to public application forms. OIDC
proves identity, while the allowlists enforce application roles.
The executive, agent, and collation portals also require the shared
`authorization.passcode` before access. It defaults to `ali2027` when omitted;
set a strong private value in Streamlit secrets for production. A shared
passcode is not a substitute for configured OIDC role allowlists.

## Supabase storage

Run [`supabase_schema.sql`](./supabase_schema.sql) in the Supabase SQL editor.
It creates the submission table, a unique deduplication constraint (shared
across self-applied and vouched palliative cases, otherwise scoped per form),
and the private evidence bucket. The app uses the service-role key only on the
server for database and storage access. Never expose it to browsers or commit
it to source control. The storage bucket is private and has a 10 MB file limit.

Configure `supabase.url` and `supabase.service_role_key` in the deployment's
Streamlit secrets manager and local `.streamlit/secrets.toml` for development.
Alternatively, set `SUPABASE_URL` and `SUPABASE_SERVICE_ROLE_KEY` as environment
variables. The service-role key takes precedence over `supabase.anon_key`,
`SUPABASE_ANON_KEY`, or `SUPABASE_KEY`. An anonymous key works only if suitable
database and storage policies are explicitly configured; the supplied schema
does not grant anonymous access to submissions.
With the service-role key, no public/anonymous database or bucket policies are
required. Back up the
project and define retention/access procedures appropriate for the personal
data collected.

## Recruitment and election panels

The recruitment panel saves applications and append-only vetting decisions in
`portal_submissions`. Applicant identity and contact details are personal data;
restrict database access and define retention procedures before deployment.
The vetting firewall requires an OIDC-authenticated, allowlisted administrator
and the admin passcode, even when the general role configuration is open.

The constituency registry editor changes `data/constituency_baseline.json` on
the local filesystem and clears the local scraper cache. Changes can be lost on
redeployment and do not synchronize across application instances; concurrent
multi-instance editing is not supported. Use a writable, persistent
single-instance deployment for this editor.

Election results and uploaded EC8A files are held only in the agent's Streamlit
session. They are not shared across sessions or saved after the session ends.
The election war room requires agent access. Recruitment vetting is enabled
using the sidebar toggle on the recruitment page and remains administrator-only.

## Project verification documents

Install the project's Python dependencies, including pypdfium2 and Pillow, and
deploy the PDFs in the `MEDIA MEDIA MEDIA` directory. The viewer renders and
caches the selected page, and the original PDF remains available to download.

## Local cache files

Offline CSV/JSON caches are not the production store and should not contain
personal data. They are ignored by Git; existing local copies can remain in
place. Remove any committed personal data from repository history using the
repository's approved incident-response process.
