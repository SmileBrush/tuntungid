"use client";

import { useActionState } from "react";
import { loginAction } from "../actions.js";

export function LoginForm() {
  const [state, formAction, pending] = useActionState(loginAction, null);

  return (
    <form action={formAction} className="mt-6 space-y-4" noValidate>
      <div>
        <label htmlFor="email" className="block text-sm font-semibold mb-1.5">Email</label>
        <input
          id="email"
          name="email"
          type="email"
          autoComplete="email"
          required
          className="w-full min-h-[48px] rounded-xl bg-soft px-4 text-base"
        />
      </div>
      <div>
        <label htmlFor="password" className="block text-sm font-semibold mb-1.5">Kata sandi</label>
        <input
          id="password"
          name="password"
          type="password"
          autoComplete="current-password"
          required
          className="w-full min-h-[48px] rounded-xl bg-soft px-4 text-base"
        />
      </div>
      {state?.error && (
        <p role="alert" className="rounded-xl bg-danger-bg p-3 text-sm font-medium text-danger">
          {state.error}
        </p>
      )}
      <button
        type="submit"
        disabled={pending}
        className="w-full min-h-[48px] rounded-xl bg-brand text-white font-semibold hover:bg-brand-hover"
      >
        {pending ? "Memeriksa akun..." : "Masuk"}
      </button>
    </form>
  );
}

