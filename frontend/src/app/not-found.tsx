import Link from "next/link";
import { Button } from "@/components/ui/button";

export default function NotFound() {
  return (
    <div className="container-page flex min-h-[50vh] flex-col items-center justify-center py-20 text-center">
      <p className="font-mono text-sm text-muted-foreground">404</p>
      <h1 className="mt-2 font-serif text-4xl text-foreground">Page not found</h1>
      <p className="mt-3 max-w-md text-sm text-muted-foreground">
        That route does not exist. Browse the API catalog or return home.
      </p>
      <div className="mt-8 flex gap-3">
        <Link href="/">
          <Button>Home</Button>
        </Link>
        <Link href="/apis">
          <Button variant="outline">API Catalog</Button>
        </Link>
      </div>
    </div>
  );
}
