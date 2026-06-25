import Link from "next/link";

export default function HomePage() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-8">
      <h1 className="text-4xl font-bold">FastAPI + Next.js</h1>
      <p className="mt-4 text-gray-600">Simple starter — one backend, one frontend.</p>
      <div className="mt-8 flex gap-4">
        <Link href="/login" className="rounded bg-blue-600 px-4 py-2 text-white hover:bg-blue-700">
          Sign in
        </Link>
        <Link
          href="/register"
          className="rounded border border-gray-300 px-4 py-2 hover:bg-gray-50"
        >
          Register
        </Link>
      </div>
    </main>
  );
}
