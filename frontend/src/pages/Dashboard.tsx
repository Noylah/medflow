interface DashboardProps {}

export default function Dashboard({}: DashboardProps) {
  return (
    <div className="mt-6 flex flex-col items-start gap-6 lg:flex-row">
      <div className="w-full h-fit bg-foreground text-background p-4 rounded-lg">
        <span className="text-2xl font-black">Welcome Back Dr. Rossi!</span>
      </div>
    </div>
  );
}
