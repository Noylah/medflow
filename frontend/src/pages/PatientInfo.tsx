import { ArrowLeft } from "lucide-react";
import { useNavigate, useParams } from "react-router-dom";

interface PatientInfoProps {}

export default function PatientInfo({}: PatientInfoProps) {
  const { id } = useParams();
  const navigator = useNavigate();
  return (
    <div>
      <div className="mt-6 flex flex-col items-start gap-6 lg:flex-row">
        <div className="flex w-full min-w-0 flex-1 flex-col gap-4">
          <div className="flex flex-col gap-2">
            <div className="flex flex-col gap-4 sm:flex-row sm:items-center">
              <ArrowLeft
                className="cursor-pointer"
                onClick={() => navigator("/patients")}
              />
              <h1 className="text-3xl font-semibold wrap-break-words text-foreground sm:text-4xl sm:break-normal">
                All your patients
              </h1>
            </div>
            <p className="max-w-2xl text-sm text-slate-500">
              Lorem ipsum, dolor sit amet consectetur adipisicing elit. Quae
              dolore dolorem aperiam aspernatur nobis nulla alias obcaecati sint
              ad atque.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
