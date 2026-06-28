import PatientItem from "../components/PatientItem";
import FilterBox from "../components/FilterBox";
import { Plus } from "lucide-react";
import { useEffect, useState } from "react";
import Loading from "./Loading";

interface PatientsProps {}

interface Patient {
  id: number;
  first_name: string;
  last_name: string;
  fiscal_code: string;
  birth_date: string;
  blood_type: string;
  created_at: string;
}

function getPatients() {
  const token = localStorage.getItem("token")?.trim();
  if (!token) {
    console.error("Nessun token trovato.");
    throw new Error("Utente non autenticato");
  }

  return fetch("http://127.0.0.1:8000/api/patients/", {
    method: "GET",
    headers: {
      Authorization: `Token ${token}`,
      "Content-Type": "application/json",
    },
  })
    .then((response) => {
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      return response.json();
    })
    .catch((error) => {
      console.error(error);
    });
}

export default function Patients({}: PatientsProps) {
  const [patients, setPatients] = useState<Patient[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  useEffect(() => {
    getPatients()
      .then((data) => {
        setPatients(data);
        setLoading(false);
      })
      .catch((err) => {
        setError(err.message);
        setLoading(false);
      });
  }, []);

  if (loading) return <Loading />;
  if (error) return <div>Errore: {error}</div>;

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
            {patients.length >= 1
              ? patients.map((patient) => (
                  <PatientItem
                    key={patient.id}
                    first_name={patient.first_name}
                    last_name={patient.last_name}
                    fiscal_code={patient.fiscal_code}
                    birth_date={patient.birth_date}
                    last_encounter_status="ACTIVE"
                  /> /* TODO: LAST_ENCOUNTER_STATUS*/
                ))
              : "Nessun paziente trovato."}
          </div>
        </div>
        <FilterBox />
      </div>
    </div>
  );
}
