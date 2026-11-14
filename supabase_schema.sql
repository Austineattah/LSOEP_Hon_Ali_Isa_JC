create table if not exists public.portal_submissions (
    id uuid primary key default gen_random_uuid(),
    submission_type text not null,
    dedupe_scope text not null,
    dedupe_key text,
    payload jsonb not null,
    created_at timestamptz not null default now(),
    constraint portal_submissions_scope_dedupe_unique
        unique (dedupe_scope, dedupe_key)
);

alter table public.portal_submissions enable row level security;
revoke all on public.portal_submissions from anon, authenticated;
grant all on public.portal_submissions to service_role;

insert into storage.buckets (id, name, public, file_size_limit, allowed_mime_types)
values (
    'private-evidence',
    'private-evidence',
    false,
    10485760,
    array['application/pdf', 'image/jpeg', 'image/png']
)
on conflict (id) do nothing;
