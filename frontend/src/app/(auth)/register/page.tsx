import Link from "next/link";

export default function RegisterPage() {
  return (
    <main className="flex min-h-screen items-center justify-center p-4">
      <div className="w-full max-w-sm space-y-6">
        <div className="text-center">
          <h1 className="text-2xl font-bold">Create account</h1>
          <p className="mt-1 text-sm text-gray-600">
            Already have an account?{" "}
            <Link href="/login" className="text-blue-600 hover:underline">
              Sign in
            </Link>
          </p>
        </div>
        <p className="text-center text-sm text-gray-500">
          Registration form — wire up to <code>/users</code> via <code>@/lib/generated</code>.
        </p>
      </div>
    </main>
  );
}
