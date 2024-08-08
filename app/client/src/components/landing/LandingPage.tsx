import Link from "next/link";
import { Mountain } from "lucide-react"; // Removed X since it's not used

export default function LandingPage() {
  return (
    <div className="flex flex-col min-h-[100dvh]">
      <header className="px-4 lg:px-6 h-14 flex items-center">
        <Link
          href="#"
          className="flex items-center justify-center"
          prefetch={false}
        >
          <Mountain className="h-6 w-6" />
          <span className="sr-only">MLpal</span>
        </Link>
        <nav className="ml-auto flex gap-4 sm:gap-6">
          <Link
            href="/api/auth/login"
            className="text-sm font-medium hover:underline underline-offset-4"
            prefetch={false}
          >
            Login
          </Link>
        </nav>
      </header>
      <main className="flex flex-col items-center justify-center">
        <section id="hero" className="w-full py-12 md:py-24 lg:py-32">
          <div className="container px-4 md:px-6">
            <div className="grid gap-6 lg:grid-cols-[1fr_400px] lg:gap-12 xl:grid-cols-[1fr_600px]">
              <div className="flex flex-col justify-center space-y-4">
                <div className="space-y-2">
                  <h1 className="text-3xl font-bold tracking-tighter sm:text-5xl xl:text-6xl">
                    MLpal: Your Personal Machine Learning Engineer
                  </h1>
                  <p className="max-w-[600px] text-muted-foreground md:text-xl">
                    In a world where AI is revolutionizing industries, Architect
                    AI stands as your gateway to harnessing this power. We are
                    not just another ML platform; we are your personal Machine
                    Learning Engineer, ready to transform your ideas into
                    reality.
                  </p>
                </div>
                <div className="flex flex-col gap-2 min-[400px]:flex-row">
                  <Link
                    href="/signin"
                    className="inline-flex h-10 items-center justify-center rounded-md bg-primary px-8 text-sm font-medium text-primary-foreground shadow transition-colors hover:bg-primary/90 focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring disabled:pointer-events-none disabled:opacity-50"
                    prefetch={false}
                  >
                    Get Started
                  </Link>
                  <Link
                    href="#learn-more"
                    className="inline-flex h-10 items-center justify-center rounded-md border border-input bg-background px-8 text-sm font-medium shadow-sm transition-colors hover:bg-accent hover:text-accent-foreground focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring disabled:pointer-events-none disabled:opacity-50"
                    prefetch={false}
                  >
                    Learn More
                  </Link>
                </div>
              </div>
              <img
                src="https://via.placeholder.com/550x550"
                width="550"
                height="550"
                alt="Hero"
                className="mx-auto aspect-video overflow-hidden rounded-xl object-cover sm:w-full lg:order-last lg:aspect-square"
              />
            </div>
          </div>
        </section>
        <section
          id="features"
          className="w-full py-12 md:py-24 lg:py-32 bg-muted"
        >
          <div className="container px-4 md:px-6">
            <div className="flex flex-col items-center justify-center space-y-4 text-center">
              <div className="space-y-2">
                <div className="inline-block rounded-lg bg-muted px-3 py-1 text-sm">
                  Key Features
                </div>
                <h2 className="text-3xl font-bold tracking-tighter sm:text-5xl">
                  Streamline Your Workflow
                </h2>
                <p className="max-w-[900px] text-muted-foreground md:text-xl/relaxed lg:text-base/relaxed xl:text-xl/relaxed">
                  MLpal is packed with powerful features to help you achieve
                  more in less time. From model selection to model training,
                  we have got you covered.
                </p>
              </div>
            </div>
            <div className="mx-auto grid max-w-5xl items-center gap-6 py-12 lg:grid-cols-2 lg:gap-12">
              <img
                src="https://via.placeholder.com/550x310"
                width="550"
                height="310"
                alt="Feature"
                className="mx-auto aspect-video overflow-hidden rounded-xl object-cover object-center sm:w-full lg:order-last"
              />
              <div className="flex flex-col justify-center space-y-4">
                <ul className="grid gap-6">
                  <li>
                    <div className="grid gap-1">
                      <h3 className="text-xl font-bold">Model Selection</h3>
                      <p className="text-muted-foreground">
                        Dumbledore, our model chooser, helps you navigate the
                        vast sea of AI models, finding the perfect fit for your
                        unique needs.
                      </p>
                    </div>
                  </li>
                  <li>
                    <div className="grid gap-1">
                      <h3 className="text-xl font-bold">Model Training</h3>
                      <p className="text-muted-foreground">
                        Yoda, our AI trainer, takes the chosen model and
                        transforms it into a powerful AI service, ready to
                        tackle your toughest challenges.
                      </p>
                    </div>
                  </li>
                  <li>
                    <div className="grid gap-1">
                      <h3 className="text-xl font-bold">Deployment</h3>
                      <p className="text-muted-foreground">
                        Deploy your AI models with a single click, and let MLpal
                        handle the infrastructure and scaling for you.
                      </p>
                    </div>
                  </li>
                </ul>
              </div>
            </div>
          </div>
        </section>
        <section id="testimonials" className="w-full py-12 md:py-24 lg:py-32">
          <div className="container px-4 md:px-6">
            <div className="flex flex-col items-center justify-center space-y-4 text-center">
              <div className="space-y-2">
                <div className="inline-block rounded-lg bg-muted px-3 py-1 text-sm">
                  Testimonials
                </div>
                <h2 className="text-3xl font-bold tracking-tighter sm:text-5xl">
                  What Our Users Say
                </h2>
                <p className="max-w-[900px] text-muted-foreground md:text-xl/relaxed lg:text-base/relaxed xl:text-xl/relaxed">
                  Discover how MLpal has made a difference for our users.
                </p>
              </div>
            </div>
            <div className="w-full mt-8">
              <div className="flex flex-col lg:flex-row lg:justify-between lg:gap-8">
                <div className="flex-1">
                  <blockquote className="relative space-y-4 rounded-md border border-muted bg-muted px-6 py-8 text-lg font-medium">
                    <p>
                      &quot;MLpal has transformed the way we approach machine
                      learning. The ease of use and the power of the platform
                      have made a huge difference for our team.&quot;
                    </p>
                    <footer className="text-sm font-semibold">
                      Jane Doe, Data Scientist
                    </footer>
                  </blockquote>
                </div>
                <div className="flex-1 mt-8 lg:mt-0">
                  <blockquote className="relative space-y-4 rounded-md border border-muted bg-muted px-6 py-8 text-lg font-medium">
                    <p>
                      &quot;The intuitive design and powerful features of Architect
                      AI have significantly boosted our productivity. Highly
                      recommended!&quot;
                    </p>
                    <footer className="text-sm font-semibold">
                      John Smith, ML Engineer
                    </footer>
                  </blockquote>
                </div>
              </div>
            </div>
          </div>
        </section>
        <section
          id="download"
          className="w-full py-12 md:py-24 lg:py-32 bg-muted"
        >
          <div className="container px-4 md:px-6">
            <div className="flex flex-col items-center justify-center space-y-4 text-center">
              <h2 className="text-3xl font-bold tracking-tighter sm:text-5xl">
                Ready to Get Started?
              </h2>
              <p className="max-w-[900px] text-muted-foreground md:text-xl/relaxed lg:text-base/relaxed xl:text-xl/relaxed">
                Sign up today to start building your AI-powered solutions with
                MLpal.
              </p>
              <div className="flex flex-col gap-2 min-[400px]:flex-row">
                <Link
                  href="/signin"
                  className="inline-flex h-10 items-center justify-center rounded-md bg-primary px-8 text-sm font-medium text-primary-foreground shadow transition-colors hover:bg-primary/90 focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring disabled:pointer-events-none disabled:opacity-50"
                  prefetch={false}
                >
                  Get Started
                </Link>
                <Link
                  href="#learn-more"
                  className="inline-flex h-10 items-center justify-center rounded-md border border-input bg-background px-8 text-sm font-medium shadow-sm transition-colors hover:bg-accent hover:text-accent-foreground focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring disabled:pointer-events-none disabled:opacity-50"
                  prefetch={false}
                >
                  Learn More
                </Link>
              </div>
            </div>
          </div>
        </section>
      </main>
      <footer className="bg-muted py-4">
        <div className="container px-4 md:px-6">
          <div className="flex flex-col items-center text-center">
            <div className="text-sm text-muted-foreground">
              © 2024 MLpal. All rights reserved.
            </div>
            <div className="mt-2 text-sm">
              <Link href="#terms" className="hover:underline" prefetch={false}>
                Terms of Service
              </Link>{" "}
              |{" "}
              <Link
                href="#privacy"
                className="hover:underline"
                prefetch={false}
              >
                Privacy Policy
              </Link>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
}
