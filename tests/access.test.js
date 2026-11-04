import test from "node:test";
import assert from "node:assert/strict";
import { resolveRole, guardPath, homePathFor } from "../src/lib/access.js";
import { normalizeStage, stageState, formatDate } from "../src/lib/stages.js";

test("resolveRole membaca peran dari app_metadata saja", () => {
  assert.equal(resolveRole(null), "anonymous");
  assert.equal(resolveRole({ app_metadata: { role: "admin" } }), "admin");
  assert.equal(resolveRole({ app_metadata: {}, user_metadata: { role: "admin" } }), "client");
  assert.equal(resolveRole({ id: "u1" }), "client");
});

test("guardPath mengalihkan sesuai peran", () => {
  assert.equal(guardPath("/admin", "admin"), null);
  assert.equal(guardPath("/admin", "client"), "/klien");
  assert.equal(guardPath("/admin/x", "anonymous"), "/masuk");
  assert.equal(guardPath("/klien", "client"), null);
  assert.equal(guardPath("/klien", "admin"), "/admin");
  assert.equal(guardPath("/klien", "anonymous"), "/masuk");
  assert.equal(guardPath("/masuk", "client"), "/klien");
  assert.equal(guardPath("/masuk", "anonymous"), null);
  assert.equal(guardPath("/", "anonymous"), null);
  assert.equal(homePathFor("admin"), "/admin");
});

test("aturan tahap proyek", () => {
  assert.equal(normalizeStage("9"), 5);
  assert.equal(normalizeStage("0"), 1);
  assert.equal(normalizeStage("abc"), 1);
  assert.equal(stageState(1, 3), "done");
  assert.equal(stageState(3, 3), "active");
  assert.equal(stageState(5, 3), "pending");
  assert.equal(formatDate(null), "Belum ditentukan");
});

