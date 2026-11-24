-- הקמת מסד הנתונים של האתר ב-Supabase.
-- מריצים פעם אחת: Supabase > SQL Editor > מדביקים > Run.
-- לפני ההרצה מחליפים את OWNER_EMAIL במייל של בעל העסק. רק המייל הזה יוכל להיכנס לאזור הניהול.

-- מי מנהל את האתר
create table if not exists public.admins (
  email text primary key
);
alter table public.admins enable row level security;
-- בלי מדיניות גישה: אף אחד לא יכול לקרוא או לשנות את הטבלה מבחוץ.

insert into public.admins (email) values ('OWNER_EMAIL') on conflict do nothing;

create or replace function public.is_admin()
returns boolean
language sql
stable
security definer
set search_path = public
as $$
  select exists (select 1 from public.admins where email = auth.jwt() ->> 'email');
$$;

-- תוכן האתר: כל טקסט, תמונה, צבע ופרט קשר ששונו מאזור הניהול
create table if not exists public.site_content (
  key text primary key check (char_length(key) <= 100),
  value text not null check (char_length(value) <= 20000),
  updated_at timestamptz not null default now()
);
alter table public.site_content enable row level security;

drop policy if exists "content is public" on public.site_content;
create policy "content is public" on public.site_content
  for select using (true);

drop policy if exists "admin edits content" on public.site_content;
create policy "admin edits content" on public.site_content
  for all to authenticated using (public.is_admin()) with check (public.is_admin());

-- פניות מהטופס
create table if not exists public.leads (
  id uuid primary key default gen_random_uuid(),
  created_at timestamptz not null default now(),
  name text not null check (char_length(name) between 1 and 80),
  phone text not null check (char_length(phone) between 7 and 20),
  service text check (char_length(service) <= 60),
  message text check (char_length(message) <= 1000),
  status text not null default 'חדש' check (status in ('חדש', 'בטיפול', 'נסגר'))
);
alter table public.leads enable row level security;

drop policy if exists "anyone can send a lead" on public.leads;
create policy "anyone can send a lead" on public.leads
  for insert to anon, authenticated with check (status = 'חדש');

drop policy if exists "admin reads leads" on public.leads;
create policy "admin reads leads" on public.leads
  for select to authenticated using (public.is_admin());

drop policy if exists "admin updates leads" on public.leads;
create policy "admin updates leads" on public.leads
  for update to authenticated using (public.is_admin()) with check (public.is_admin());

drop policy if exists "admin deletes leads" on public.leads;
create policy "admin deletes leads" on public.leads
  for delete to authenticated using (public.is_admin());

-- תמונות: לוגו ותמונות שמועלות מאזור הניהול
insert into storage.buckets (id, name, public)
values ('site', 'site', true)
on conflict (id) do nothing;

drop policy if exists "site images are public" on storage.objects;
create policy "site images are public" on storage.objects
  for select using (bucket_id = 'site');

drop policy if exists "admin uploads images" on storage.objects;
create policy "admin uploads images" on storage.objects
  for insert to authenticated with check (bucket_id = 'site' and public.is_admin());

drop policy if exists "admin replaces images" on storage.objects;
create policy "admin replaces images" on storage.objects
  for update to authenticated using (bucket_id = 'site' and public.is_admin());
