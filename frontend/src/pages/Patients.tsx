import PatientItem from "../components/PatientItem";
import FilterBox from "../components/FilterBox";
import { Plus } from "lucide-react";
import { useEffect, useState } from "react";
import Loading from "./Loading";
import Modal from "../components/Modal";

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

interface FilterState {
  status: string;
  color: string;
}

export default function Patients({}: PatientsProps) {
  const [patients, setPatients] = useState<Patient[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [formData, setFormData] = useState({
    first_name: "",
    last_name: "",
    fiscal_code: "",
    birth_date: "",
    blood_type: "",
  });
  const [filters, setFilters] = useState<FilterState>({
    status: "",
    color: "",
  });

  function getPatients(filters: { status: string; color: string }) {
    const token = localStorage.getItem("token")?.trim();
    if (!token) {
      console.error("Nessun token trovato.");
      throw new Error("Utente non autenticato");
    }

    const params = new URLSearchParams();
    if (filters.status) params.append("status", filters.status);
    if (filters.color) params.append("color", filters.color);

    const url = `http://127.0.0.1:8000/api/patients/?${params.toString()}`;

    return fetch(url, {
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

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const loadPatients = () => {
    getPatients(filters).then((data) => setPatients(data));
  };

  const handleSubmit = async (e: React.SubmitEvent) => {
    e.preventDefault();
    const token = localStorage.getItem("token")?.trim();
    if (!token) {
      console.error("Nessun token trovato.");
      throw new Error("Utente non autenticato");
    }

    fetch("http://127.0.0.1:8000/api/patients/", {
      method: "POST",
      headers: {
        Authorization: `Token ${token}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify(formData),
    })
      .then((response) => {
        if (!response.ok) {
          return response.json().then((err) => {
            throw new Error(err.detail || "Errore");
          });
        }
        return response.json();
      })
      .then((data) => {
        console.log("Paziente aggiunto con successo:", data);
        setIsModalOpen(false);
        loadPatients();
      });
  };

  useEffect(() => {
    getPatients(filters)
      .then((data) => {
        setPatients(data);
        setLoading(false);
      })
      .catch((err) => {
        setError(err.message);
        setLoading(false);
      });
  }, [filters]);

  if (loading) return <Loading />;
  if (error) return <div>Errore: {error}</div>;

  const handleFilterChange = (key: keyof FilterState, value: string) => {
    setFilters((prev) => ({ ...prev, [key]: value }));
  };

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
                <div
                  className="flex w-fit cursor-pointer gap-2 rounded-3xl bg-primary px-4 py-2 whitespace-nowrap text-background transition-all duration-300 hover:translate-y-0.75 hover:bg-primary-dark"
                  onClick={() => setIsModalOpen(true)}
                >
                  <Plus />
                  New Patient
                </div>
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
                    patient_id={patient.id}
                    first_name={patient.first_name}
                    last_name={patient.last_name}
                    fiscal_code={patient.fiscal_code}
                    birth_date={patient.birth_date}
                  />
                ))
              : "Nessun paziente trovato."}
          </div>
        </div>
        <FilterBox filters={filters} onFilterChange={handleFilterChange} />
      </div>
      <Modal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        title="New Patient"
      >
        <form className="gap-y-4" onSubmit={handleSubmit}>
          <div>
            <label className="block text-sm font-medium text-slate-700">
              First Name
            </label>
            <input
              name="first_name"
              type="text"
              maxLength={120}
              className="mt-1 w-full rounded-md border border-slate-300 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-primary"
              value={formData.first_name}
              onChange={handleChange}
              required
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-slate-700">
              Last Name
            </label>
            <input
              name="last_name"
              type="text"
              maxLength={120}
              className="mt-1 w-full rounded-md border border-slate-300 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-primary"
              value={formData.last_name}
              onChange={handleChange}
              required
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-slate-700">
              Fiscal Code
            </label>
            <input
              name="fiscal_code"
              type="text"
              maxLength={16}
              className="mt-1 w-full rounded-md border border-slate-300 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-primary"
              value={formData.fiscal_code}
              onChange={handleChange}
              required
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-slate-700">
              Birth Date
            </label>
            <input
              type="date"
              name="birth_date"
              value={formData.birth_date}
              onChange={handleChange}
              className="mt-1 block w-full rounded-md border border-slate-300 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-primary"
              max={new Date().toISOString().split("T")[0]}
              required
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-slate-700">
              Blood Type
            </label>
            <input
              name="blood_type"
              type="text"
              maxLength={3}
              className="mt-1 w-full rounded-md border border-slate-300 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-primary"
              value={formData.blood_type}
              onChange={handleChange}
            />
          </div>
          <input
            type="submit"
            value="Submit"
            className="mt-4 flex w-fit cursor-pointer gap-2 rounded-3xl bg-primary px-4 py-2 whitespace-nowrap text-background transition-all duration-300 hover:translate-y-0.75 hover:bg-primary-dark"
          />
        </form>
      </Modal>
    </div>
  );
}
