interface FilterBoxProps {
  filters: { status: string; color: string };
  onFilterChange: (key: "status" | "color", value: string) => void;
}

export default function FilterBox({ filters, onFilterChange }: FilterBoxProps) {
  function resetFilters() {
    onFilterChange("status", "");
    onFilterChange("color", "");
  }
  return (
    <div className="flex w-full shrink-0 flex-col gap-2 rounded-2xl border-3 border-primary bg-white/30 p-4 md:w-64">
      <span className="text-xs font-bold tracking-wider text-primary-dark uppercase">
        Filters
      </span>

      <div className="flex flex-col gap-1">
        <label className="group flex cursor-pointer items-center justify-between rounded-lg p-2 transition-colors hover:bg-primary/20">
          <span className="text-sm font-medium text-foreground/80">
            Last Encounter Status
          </span>
          <div className="text-primary-dark transition-transform group-hover:scale-103">
            <select
              className="cursor-pointer border-none bg-transparent pr-2 text-right text-sm font-medium text-primary-dark outline-none"
              value={filters.status}
              onChange={(e) => onFilterChange("status", e.target.value)}
            >
              <option value="" className="text-foreground">
                All Status
              </option>
              <option value="ACTIVE" className="text-foreground">
                Active
              </option>
              <option value="UNDER_VISIT" className="text-foreground">
                Under Visit
              </option>
              <option value="DISCHARGED" className="text-foreground">
                Discharged
              </option>
            </select>
          </div>
        </label>
      </div>

      <div className="flex flex-col gap-1">
        <label className="group flex cursor-pointer items-center justify-between rounded-lg p-2 transition-colors hover:bg-primary/20">
          <span className="text-sm font-medium text-foreground/80">
            Last Triage Color
          </span>
          <div className="text-primary-dark transition-transform group-hover:scale-103">
            <select
              className="cursor-pointer border-none bg-transparent pr-2 text-right text-sm font-medium text-primary-dark outline-none"
              value={filters.color}
              onChange={(e) => onFilterChange("color", e.target.value)}
            >
              <option value="" className="text-foreground">
                All Colors
              </option>
              <option value="RED" className="text-foreground">
                Red
              </option>
              <option value="YELLOW" className="text-foreground">
                Yellow
              </option>
              <option value="GREEN" className="text-foreground">
                Green
              </option>
              <option value="WHITE" className="text-foreground">
                White
              </option>
            </select>
          </div>
        </label>
      </div>
      <span
        className="bg-primary rounded-lg w-fit px-2 py-1 text-background font-bold text-sm hover:bg-primary-dark translate-colors duration-400 cursor-pointer"
        onClick={() => resetFilters()}
      >
        RESET FILTERS
      </span>
    </div>
  );
}
