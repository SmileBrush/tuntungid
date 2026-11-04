import { DashboardShell, ErrorBox } from "../../components/dashboard-shell.jsx";
import { StageTracker, EmptyState } from "../../components/stage-tracker.jsx";
import { getSessionUser } from "../../lib/supabase/server.js";
import { REQUEST_KINDS, REQUEST_STATUSES, STAGES, stageLabel } from "../../lib/stages.js";
import {
  addFileAction,
  replyRequestAction,
  updateScheduleAction,
  updateStageAction,
  togglePortfolioPublishAction,
  deletePortfolioAction,
  toggleReviewPublishAction,
  deleteReviewAction
} from "./actions.js";
import { CreateClientForm } from "./create-client-form.jsx";
import { PortfolioForm } from "./portfolio-form.jsx";
import { StarRatingDisplay } from "../../components/star-rating.jsx";

export const metadata = { title: "Dashboard Admin | Tuntung.id" };
export const dynamic = "force-dynamic";

const field = "w-full min-h-[44px] rounded-xl bg-soft px-3 text-base";
const btn = "min-h-[44px] px-4 rounded-xl bg-ink text-white text-sm font-semibold hover:bg-brand";

export default async function AdminPage({ searchParams }) {
  const { tab = "proyek" } = await searchParams;
  const { supabase, user } = await getSessionUser();

  const [projectsRes, requestsRes, filesRes, profilesRes, portfoliosRes, reviewsRes] = await Promise.all([
    supabase.from("projects").select("*, profiles(full_name, company)").order("created_at", { ascending: false }),
    supabase.from("requests").select("*, projects(title, profiles(full_name))").order("created_at", { ascending: false }),
    supabase.from("project_files").select("*").order("created_at", { ascending: false }),
    supabase.from("profiles").select("*").order("created_at", { ascending: false }),
    supabase.from("portfolios").select("*").order("created_at", { ascending: false }),
    supabase.from("reviews").select("*, projects(title), profiles(full_name, company)").order("created_at", { ascending: false })
  ]);

  const failed = [projectsRes, requestsRes, filesRes, profilesRes].find((r) => r.error);
  const projects = projectsRes.data || [];
  const requests = requestsRes.data || [];
  const files = filesRes.data || [];
  const profiles = profilesRes.data || [];
  const portfolios = portfoliosRes.data || [];
  const reviews = reviewsRes.data || [];
  const newCount = requests.filter((r) => r.status === "baru").length;
  const pendingReviewsCount = reviews.filter((r) => !r.is_published).length;

  const nav = [
    { key: "proyek", label: "Proyek", href: "/admin" },
    { key: "permintaan", label: "Permintaan", href: "/admin?tab=permintaan", badge: newCount || null },
    { key: "portofolio", label: "Portofolio", href: "/admin?tab=portofolio" },
    { key: "review", label: "Review Klien", href: "/admin?tab=review", badge: pendingReviewsCount || null },
    { key: "klien", label: "Klien", href: "/admin?tab=klien" }
  ];

  return (
    <DashboardShell roleLabel="Dashboard Admin" userName={user.email} nav={nav} active={tab}>
      {failed && (
        <div className="mb-4">
          <ErrorBox
            title="Data gagal dimuat dari Supabase"
            hint="Pastikan supabase/schema.sql sudah dijalankan di SQL Editor dan akun ini memiliki app_metadata role admin."
          />
        </div>
      )}

      {tab === "proyek" && (
        <section>
          <h1 className="font-display font-bold text-2xl">Proyek</h1>
          {projects.length === 0 ? (
            <div className="mt-4">
              <EmptyState
                title="Belum ada proyek"
                hint="Buat akun klien lebih dulu. Proyek pertama dibuat bersamaan."
                action={
                  <a href="/admin?tab=klien" className="mt-4 min-h-[44px] px-4 rounded-xl bg-brand text-white text-sm font-semibold inline-flex items-center hover:bg-brand-hover">
                    Buat Akun Klien
                  </a>
                }
              />
            </div>
          ) : (
            <ul className="mt-4 space-y-3">
              {projects.map((p) => {
                const pFiles = files.filter((f) => f.project_id === p.id);
                return (
                  <li key={p.id}>
                    <details className="rounded-2xl bg-white group">
                      <summary className="list-none p-5 min-h-[44px]">
                        <div className="flex flex-wrap items-center justify-between gap-2">
                          <div>
                            <h2 className="font-display font-bold text-lg">{p.title}</h2>
                            <p className="text-sm text-ink-2">
                              {p.profiles?.full_name}
                              {p.profiles?.company ? `, ${p.profiles.company}` : ""}
                            </p>
                          </div>
                          <p className="text-sm font-semibold">{stageLabel(p.stage)}</p>
                        </div>
                        <div className="mt-3"><StageTracker stage={p.stage} compact /></div>
                      </summary>

                      <div className="grid gap-4 p-5 pt-0 lg:grid-cols-2">
                        <form action={updateStageAction} className="rounded-2xl bg-soft p-4 space-y-2">
                          <input type="hidden" name="project_id" value={p.id} />
                          <label htmlFor={`stage-${p.id}`} className="block text-sm font-semibold">Tahap proyek</label>
                          <select id={`stage-${p.id}`} name="stage" defaultValue={p.stage} className={field}>
                            {STAGES.map((s) => (
                              <option key={s.number} value={s.number}>{`${s.number}. ${s.name}`}</option>
                            ))}
                          </select>
                          <button type="submit" className={btn}>Simpan Tahap</button>
                        </form>

                        <form action={updateScheduleAction} className="rounded-2xl bg-soft p-4 space-y-2">
                          <input type="hidden" name="project_id" value={p.id} />
                          <div className="grid grid-cols-2 gap-2">
                            <div>
                              <label htmlFor={`start-${p.id}`} className="block text-sm font-semibold mb-1">Mulai</label>
                              <input id={`start-${p.id}`} type="date" name="start_date" defaultValue={p.start_date || ""} className={field} />
                            </div>
                            <div>
                              <label htmlFor={`target-${p.id}`} className="block text-sm font-semibold mb-1">Target rilis</label>
                              <input id={`target-${p.id}`} type="date" name="target_date" defaultValue={p.target_date || ""} className={field} />
                            </div>
                          </div>
                          <button type="submit" className={btn}>Simpan Jadwal</button>
                        </form>

                        <div className="rounded-2xl bg-soft p-4 lg:col-span-2">
                          <h3 className="font-display font-semibold">File serah terima</h3>
                          {pFiles.length === 0 ? (
                            <p className="text-sm text-ink-2 mt-1">Belum ada file. Tambahkan tautan di bawah.</p>
                          ) : (
                            <ul className="mt-2 space-y-1.5 text-sm">
                              {pFiles.map((f) => (
                                <li key={f.id}>
                                  <a href={f.url} target="_blank" rel="noreferrer" className="font-semibold text-brand hover:underline">
                                    {f.label}
                                  </a>
                                </li>
                              ))}
                            </ul>
                          )}
                          <form action={addFileAction} className="mt-3 grid gap-2 sm:grid-cols-[1fr_1.4fr_auto]">
                            <input type="hidden" name="project_id" value={p.id} />
                            <label className="sr-only" htmlFor={`label-${p.id}`}>Nama file</label>
                            <input id={`label-${p.id}`} name="label" placeholder="Nama file" required className={field} />
                            <label className="sr-only" htmlFor={`url-${p.id}`}>Tautan file</label>
                            <input id={`url-${p.id}`} name="url" type="url" placeholder="https://..." required className={field} />
                            <button type="submit" className={btn}>Tambah File</button>
                          </form>
                        </div>
                      </div>
                    </details>
                  </li>
                );
              })}
            </ul>
          )}
        </section>
      )}

      {tab === "permintaan" && (
        <section>
          <h1 className="font-display font-bold text-2xl">Permintaan klien</h1>
          {requests.length === 0 ? (
            <div className="mt-4">
              <EmptyState title="Belum ada permintaan masuk" hint="Permintaan revisi dan fitur tambahan dari klien muncul di sini." />
            </div>
          ) : (
            <ul className="mt-4 space-y-3">
              {requests.map((r) => (
                <li key={r.id} className="rounded-2xl bg-white p-5">
                  <div className="flex flex-wrap items-center gap-2 text-sm font-semibold">
                    <span>{REQUEST_KINDS[r.kind]}</span>
                    <span className="rounded-lg bg-soft px-2 py-0.5">{REQUEST_STATUSES[r.status]}</span>
                    <span className="text-ink-2 font-medium">
                      {r.projects?.title}, {r.projects?.profiles?.full_name}
                    </span>
                  </div>
                  <p className="mt-2">{r.message}</p>
                  <form action={replyRequestAction} className="mt-3 grid gap-2 sm:grid-cols-[1fr_auto_auto]">
                    <input type="hidden" name="request_id" value={r.id} />
                    <label className="sr-only" htmlFor={`reply-${r.id}`}>Balasan untuk klien</label>
                    <input id={`reply-${r.id}`} name="admin_reply" defaultValue={r.admin_reply || ""} placeholder="Tulis balasan untuk klien" className={field} />
                    <label className="sr-only" htmlFor={`status-${r.id}`}>Status</label>
                    <select id={`status-${r.id}`} name="status" defaultValue={r.status === "baru" ? "diproses" : r.status} className={field}>
                      <option value="diproses">Diproses</option>
                      <option value="selesai">Selesai</option>
                      <option value="baru">Baru</option>
                    </select>
                    <button type="submit" className={btn}>Kirim Balasan</button>
                  </form>
                </li>
              ))}
            </ul>
          )}
        </section>
      )}

      {tab === "portofolio" && (
        <section>
          <h1 className="font-display font-bold text-2xl">Portofolio Proyek</h1>
          <div className="mt-4 rounded-2xl bg-white p-5 sm:p-6">
            <h2 className="font-display font-bold text-lg">Tambah Portofolio Baru</h2>
            <p className="text-sm text-ink-2 mt-1 mb-4">
              Portofolio yang Anda simpan akan langsung tampil pada etalase karya di Landing Page.
            </p>
            <PortfolioForm />
          </div>

          <div className="mt-4 rounded-2xl bg-white p-5 sm:p-6">
            <h2 className="font-display font-bold text-lg">Daftar Portofolio ({portfolios.length})</h2>
            {portfolios.length === 0 ? (
              <div className="mt-3">
                <EmptyState
                  title="Belum ada portofolio"
                  hint="Gunakan form di atas untuk menambahkan hasil kerja aplikasi pertama Anda."
                />
              </div>
            ) : (
              <div className="mt-4 grid gap-4 sm:grid-cols-2">
                {portfolios.map((item) => (
                  <article key={item.id} className="rounded-2xl bg-soft p-4 flex flex-col justify-between">
                    <div>
                      {item.image_url && (
                        <div className="overflow-hidden rounded-xl bg-line mb-3 aspect-video">
                          <img
                            src={item.image_url}
                            alt={item.title}
                            className="w-full h-full object-cover"
                            loading="lazy"
                          />
                        </div>
                      )}
                      <div className="flex flex-wrap items-center justify-between gap-1 text-xs font-semibold">
                        <span className="px-2 py-0.5 rounded-md bg-white text-ink">{item.sector}</span>
                        <span
                          className={`px-2 py-0.5 rounded-md font-semibold ${
                            item.is_published ? "bg-ok-bg text-brand" : "bg-line text-ink-2"
                          }`}
                        >
                          {item.is_published ? "Tampil di Beranda" : "Disembunyikan"}
                        </span>
                      </div>
                      <h3 className="font-display font-bold text-base text-ink mt-2">{item.title}</h3>
                      <p className="text-xs text-brand font-medium mt-0.5">{item.tech_stack}</p>
                      <p className="text-sm text-ink-2 mt-2 leading-relaxed">{item.summary}</p>
                      {item.demo_url && (
                        <a
                          href={item.demo_url}
                          target="_blank"
                          rel="noreferrer"
                          className="mt-2 text-xs font-bold text-brand hover:underline inline-block"
                        >
                          Buka Demo Web ↗
                        </a>
                      )}
                    </div>

                    <div className="mt-4 pt-3 flex items-center justify-between gap-2">
                      <form action={togglePortfolioPublishAction}>
                        <input type="hidden" name="portfolio_id" value={item.id} />
                        <input type="hidden" name="is_published" value={String(item.is_published)} />
                        <button
                          type="submit"
                          className={`min-h-[38px] px-3 rounded-lg text-xs font-bold ${
                            item.is_published
                              ? "bg-white text-ink-2 hover:bg-line"
                              : "bg-brand text-white hover:bg-brand-hover"
                          }`}
                        >
                          {item.is_published ? "Sembunyikan" : "Tampilkan"}
                        </button>
                      </form>

                      <form action={deletePortfolioAction}>
                        <input type="hidden" name="portfolio_id" value={item.id} />
                        <button
                          type="submit"
                          className="min-h-[38px] px-3 rounded-lg bg-danger-bg text-danger text-xs font-bold hover:bg-danger/20"
                        >
                          Hapus
                        </button>
                      </form>
                    </div>
                  </article>
                ))}
              </div>
            )}
          </div>
        </section>
      )}

      {tab === "review" && (
        <section>
          <h1 className="font-display font-bold text-2xl">Review Klien</h1>
          <p className="text-sm text-ink-2 mt-1">
            Ulasan yang disetujui akan tampil di bagian Ulasan Klien pada Landing Page.
          </p>

          <div className="mt-4 rounded-2xl bg-white p-5 sm:p-6">
            <h2 className="font-display font-bold text-lg">Daftar Review Masuk ({reviews.length})</h2>
            {reviews.length === 0 ? (
              <div className="mt-3">
                <EmptyState
                  title="Belum ada review klien"
                  hint="Klien dapat menuliskan ulasan begitu proyek mereka mencapai Tahap 5 (Serah Terima & Garansi)."
                />
              </div>
            ) : (
              <ul className="mt-4 space-y-3">
                {reviews.map((rev) => (
                  <li key={rev.id} className="rounded-2xl bg-soft p-4 sm:p-5">
                    <div className="flex flex-wrap items-center justify-between gap-2">
                      <div>
                        <div className="flex items-center gap-2">
                          <StarRatingDisplay rating={rev.rating} />
                          <span className="text-xs font-semibold text-ink-2 tabular-nums">
                            ({rev.rating}/5)
                          </span>
                        </div>
                        <p className="text-sm font-bold text-ink mt-1">
                          {rev.profiles?.full_name}
                          {rev.profiles?.company ? ` - ${rev.profiles.company}` : ""}
                        </p>
                        <p className="text-xs text-ink-2">Proyek: {rev.projects?.title}</p>
                      </div>

                      <span
                        className={`px-2.5 py-1 rounded-lg text-xs font-bold ${
                          rev.is_published ? "bg-ok-bg text-brand" : "bg-gold/20 text-ink"
                        }`}
                      >
                        {rev.is_published ? "Tayang di Landing Page" : "Perlu Persetujuan"}
                      </span>
                    </div>

                    <p className="mt-3 text-sm text-ink italic leading-relaxed">
                      &ldquo;{rev.feedback}&rdquo;
                    </p>

                    <div className="mt-4 pt-3 flex items-center justify-between gap-2">
                      <form action={toggleReviewPublishAction}>
                        <input type="hidden" name="review_id" value={rev.id} />
                        <input type="hidden" name="is_published" value={String(rev.is_published)} />
                        <button
                          type="submit"
                          className={`min-h-[40px] px-4 rounded-xl text-xs font-bold transition-colors ${
                            rev.is_published
                              ? "bg-white text-ink-2 hover:bg-line"
                              : "bg-brand text-white hover:bg-brand-hover"
                          }`}
                        >
                          {rev.is_published ? "Sembunyikan dari Publik" : "Setujui & Tampilkan di Landing Page"}
                        </button>
                      </form>

                      <form action={deleteReviewAction}>
                        <input type="hidden" name="review_id" value={rev.id} />
                        <button
                          type="submit"
                          className="min-h-[40px] px-3.5 rounded-xl bg-danger-bg text-danger text-xs font-bold hover:bg-danger/20"
                        >
                          Hapus Review
                        </button>
                      </form>
                    </div>
                  </li>
                ))}
              </ul>
            )}
          </div>
        </section>
      )}

      {tab === "klien" && (
        <section>
          <h1 className="font-display font-bold text-2xl">Klien</h1>
          <div className="mt-4 rounded-2xl bg-white p-5 sm:p-6">
            <h2 className="font-display font-bold text-lg">Buat akun klien baru</h2>
            <p className="text-sm text-ink-2 mt-1 mb-4">Kirim email dan kata sandi sementara ke klien lewat WhatsApp.</p>
            <CreateClientForm />
          </div>
          <div className="mt-3 rounded-2xl bg-white p-5 sm:p-6">
            <h2 className="font-display font-bold text-lg">Daftar klien</h2>
            {profiles.length === 0 ? (
              <div className="mt-3"><EmptyState title="Belum ada klien" hint="Gunakan form di atas untuk membuat akun pertama." /></div>
            ) : (
              <ul className="mt-3 space-y-2">
                {profiles.map((c) => (
                  <li key={c.id} className="rounded-xl bg-soft px-4 py-3 text-sm">
                    <span className="font-semibold">{c.full_name}</span>
                    {c.company ? <span className="text-ink-2">, {c.company}</span> : null}
                  </li>
                ))}
              </ul>
            )}
          </div>
        </section>
      )}
    </DashboardShell>
  );
}

