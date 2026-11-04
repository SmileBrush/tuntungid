import Link from "next/link";
import { DashboardShell, ErrorBox } from "../../components/dashboard-shell.jsx";
import { StageTracker, EmptyState } from "../../components/stage-tracker.jsx";
import { getSessionUser } from "../../lib/supabase/server.js";
import { REQUEST_KINDS, REQUEST_STATUSES, formatDate, stageLabel, canReviewProject } from "../../lib/stages.js";
import { RequestForm } from "./request-form.jsx";
import { ReviewForm } from "./review-form.jsx";

export const metadata = { title: "Dashboard Klien | Tuntung.id" };
export const dynamic = "force-dynamic";

export default async function KlienPage({ searchParams }) {
  const { p } = await searchParams;
  const { supabase, user } = await getSessionUser();

  const [profileRes, projectsRes] = await Promise.all([
    supabase.from("profiles").select("full_name, company").eq("id", user.id).maybeSingle(),
    supabase.from("projects").select("*").order("created_at", { ascending: true })
  ]);

  const name = profileRes.data?.full_name || user.email;
  const nav = [{ key: "proyek", label: "Proyek Saya", href: "/klien" }];

  if (projectsRes.error) {
    return (
      <DashboardShell roleLabel="Dashboard Klien" userName={name} nav={nav} active="proyek">
        <ErrorBox
          title="Data proyek gagal dimuat"
          hint="Muat ulang halaman. Jika masih gagal, hubungi admin Tuntung.id."
        />
      </DashboardShell>
    );
  }

  const projects = projectsRes.data;
  const project = projects.find((x) => x.id === p) || projects[0];

  let files = [];
  let requests = [];
  let existingReview = null;
  if (project) {
    const [filesRes, reqRes, revRes] = await Promise.all([
      supabase.from("project_files").select("*").eq("project_id", project.id).order("created_at", { ascending: false }),
      supabase.from("requests").select("*").eq("project_id", project.id).order("created_at", { ascending: false }),
      supabase.from("reviews").select("*").eq("project_id", project.id).maybeSingle()
    ]);
    files = filesRes.data || [];
    requests = reqRes.data || [];
    existingReview = revRes?.data || null;
  }

  return (
    <DashboardShell roleLabel="Dashboard Klien" userName={name} nav={nav} active="proyek">
      <p className="text-ink-2">Halo, {name}</p>

      {!project ? (
        <div className="mt-4">
          <EmptyState
            title="Belum ada proyek di akun Anda"
            hint="Admin Tuntung.id akan menambahkan proyek Anda. Hubungi kami bila ini seharusnya sudah ada."
          />
        </div>
      ) : (
        <>
          {projects.length > 1 && (
            <nav aria-label="Pilih proyek" className="mt-3 flex flex-wrap gap-2">
              {projects.map((x) => (
                <Link
                  key={x.id}
                  href={`/klien?p=${x.id}`}
                  aria-current={x.id === project.id ? "page" : undefined}
                  className={`min-h-[44px] px-4 rounded-xl inline-flex items-center text-sm font-semibold ${
                    x.id === project.id ? "bg-ink text-white" : "bg-white"
                  }`}
                >
                  {x.title}
                </Link>
              ))}
            </nav>
          )}

          <section className="mt-3 rounded-2xl bg-white p-5 sm:p-6">
            <h1 className="font-display font-bold text-2xl">{project.title}</h1>
            <p className="text-ink-2 mt-1">{stageLabel(project.stage)}</p>
            <div className="mt-5"><StageTracker stage={project.stage} /></div>
            <dl className="mt-5 grid gap-3 sm:grid-cols-2">
              <div className="rounded-2xl bg-soft p-4">
                <dt className="text-sm text-ink-2">Mulai</dt>
                <dd className="font-semibold mt-0.5 tabular-nums">{formatDate(project.start_date)}</dd>
              </div>
              <div className="rounded-2xl bg-soft p-4">
                <dt className="text-sm text-ink-2">Target rilis</dt>
                <dd className="font-semibold mt-0.5 tabular-nums">{formatDate(project.target_date)}</dd>
              </div>
            </dl>
          </section>

          <div className="mt-3 grid gap-3 lg:grid-cols-2">
            <section className="rounded-2xl bg-white p-5 sm:p-6">
              <h2 className="font-display font-bold text-lg">File serah terima</h2>
              {files.length === 0 ? (
                <div className="mt-3">
                  <EmptyState title="Belum ada file" hint="File muncul di sini setelah admin menambahkannya." />
                </div>
              ) : (
                <ul className="mt-3 space-y-2">
                  {files.map((f) => (
                    <li key={f.id}>
                      <a
                        href={f.url}
                        target="_blank"
                        rel="noreferrer"
                        className="min-h-[44px] px-4 rounded-xl bg-soft inline-flex w-full items-center justify-between gap-3 text-sm font-semibold hover:bg-line"
                      >
                        <span className="truncate">{f.label}</span>
                        <span className="text-brand shrink-0">Buka</span>
                      </a>
                    </li>
                  ))}
                </ul>
              )}
            </section>

            <section className="rounded-2xl bg-white p-5 sm:p-6">
              <h2 className="font-display font-bold text-lg">Kirim permintaan</h2>
              <div className="mt-3"><RequestForm projectId={project.id} /></div>
            </section>
          </div>

          <section className="mt-3 rounded-2xl bg-white p-5 sm:p-6">
            <h2 className="font-display font-bold text-lg">Riwayat permintaan</h2>
            {requests.length === 0 ? (
              <div className="mt-3">
                <EmptyState title="Belum ada permintaan" hint="Gunakan form di atas untuk meminta revisi atau fitur tambahan." />
              </div>
            ) : (
              <ul className="mt-3 space-y-3">
                {requests.map((r) => (
                  <li key={r.id} className="rounded-2xl bg-soft p-4">
                    <div className="flex flex-wrap items-center gap-2 text-sm font-semibold">
                      <span>{REQUEST_KINDS[r.kind]}</span>
                      <span className="rounded-lg bg-white px-2 py-0.5">{REQUEST_STATUSES[r.status]}</span>
                    </div>
                    <p className="mt-2">{r.message}</p>
                    {r.admin_reply && (
                      <p className="mt-2 rounded-xl bg-white p-3 text-sm">
                        <span className="font-semibold">Balasan admin: </span>
                        {r.admin_reply}
                      </p>
                    )}
                  </li>
                ))}
              </ul>
            )}
          </section>

          {canReviewProject(project.stage) ? (
            <section className="mt-3 rounded-2xl bg-white p-5 sm:p-6">
              <h2 className="font-display font-bold text-lg">Review &amp; Testimoni Proyek</h2>
              <p className="text-sm text-ink-2 mt-1">
                Proyek Anda telah memasuki tahap serah terima. Berikan ulasan jujur untuk membantu kami terus berkembang.
              </p>
              <div className="mt-4">
                <ReviewForm projectId={project.id} existingReview={existingReview} />
              </div>
            </section>
          ) : (
            <section className="mt-3 rounded-2xl bg-soft p-5 sm:p-6 text-center">
              <p className="font-display font-semibold text-ink">Ulasan &amp; Penilaian Klien</p>
              <p className="text-sm text-ink-2 mt-1">
                Formulir ulasan akan terbuka secara otomatis saat proyek Anda memasuki Tahap 5 (Serah Terima &amp; Garansi).
              </p>
            </section>
          )}
        </>
      )}
    </DashboardShell>
  );
}

