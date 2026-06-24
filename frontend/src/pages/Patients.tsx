import PatientItem from "../components/PatientItem";
import FilterBox from "../components/FilterBox";
import { Plus } from "lucide-react";

interface PatientsProps {}

export default function Patients({}: PatientsProps) {
  return (
    <div>
      <div className="mt-6 flex flex-col items-start gap-6 lg:flex-row">
        <div className="flex w-full min-w-0 flex-1 flex-col gap-4">
          <div className="flex flex-col gap-2">
            <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
              <h1 className="text-3xl font-semibold wrap-break-words text-foreground sm:text-4xl sm:break-normal">
                All your patients
              </h1>
              <div className="shrink-0">
                <span className="flex w-fit cursor-pointer gap-2 rounded-3xl bg-primary px-4 py-2 whitespace-nowrap text-background transition-all duration-300 hover:translate-y-0.75 hover:bg-primary-dark">
                  <Plus />
                  New Patient
                </span>
              </div>
            </div>
            <p className="max-w-2xl text-sm text-slate-500">
              Lorem ipsum, dolor sit amet consectetur adipisicing elit. Quae
              dolore dolorem aperiam aspernatur nobis nulla alias obcaecati sint
              ad atque.
            </p>
          </div>

          <div className="mt-2 grid w-full grid-cols-1 items-start gap-4 xl:grid-cols-3">
            <PatientItem />
            <PatientItem />
          </div>
        </div>
        <FilterBox />
      </div>
    </div>
  );
}
