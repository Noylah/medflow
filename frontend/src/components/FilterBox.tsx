interface FilterBoxProps {}

export default function FilterBox({}: FilterBoxProps) {
  return (
    <div className="flex w-full shrink-0 flex-col gap-2 rounded-2xl border-3 border-primary bg-white/30 p-4 md:w-64">
      <span className="text-xs font-bold tracking-wider text-primary-dark uppercase">
        Filters
      </span>

      <div className="flex flex-col gap-1">
        <label className="group flex cursor-pointer items-center justify-between rounded-lg p-2 transition-colors hover:bg-primary/20">
          <span className="text-sm font-medium text-foreground/80">
            Active Encounter
          </span>
          <div className="text-primary-dark transition-transform group-hover:scale-105">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              width="18"
              height="18"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
              stroke-linecap="round"
              stroke-linejoin="round"
              className="lucide lucide-square"
            >
              <rect width="18" height="18" x="3" y="3" rx="2" />
            </svg>
          </div>
        </label>
      </div>

      <div className="flex flex-col gap-1">
        <label className="group flex cursor-pointer items-center justify-between rounded-lg p-2 transition-colors hover:bg-primary/20">
          <span className="text-sm font-medium text-foreground/80">
            Select Filter
          </span>
          <div className="text-primary-dark transition-transform group-hover:scale-103">
            <select className="cursor-pointer border-none bg-transparent pr-2 text-right text-sm font-medium text-primary-dark outline-none">
              <option value="" className="text-foreground">
                All Roles
              </option>
              <option value="doctor" className="text-foreground">
                Doctor
              </option>
              <option value="nurse" className="text-foreground">
                Nurse
              </option>
              <option value="receptionist" className="text-foreground">
                Receptionist
              </option>
            </select>
          </div>
        </label>
      </div>
    </div>
  );
}
