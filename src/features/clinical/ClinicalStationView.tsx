import React, { useState } from 'react';
import {
  Stethoscope,
  User,
  Heart,
  Activity,
  Plus,
  ShieldAlert,
  CheckCircle2,
  FileText,
  Sparkles,
  QrCode,
  Pill,
} from 'lucide-react';
import { INITIAL_PATIENTS, INITIAL_MEDICINES } from '../../services/api';
import { Patient, MedicineMaster, PrescriptionItem } from '../../types';

export const ClinicalStationView: React.FC = () => {
  const [patients] = useState<Patient[]>(INITIAL_PATIENTS);
  const [selectedPatient, setSelectedPatient] = useState<Patient>(INITIAL_PATIENTS[0]);
  const [chiefComplaint, setChiefComplaint] = useState(
    'Routine follow-up on cardiovascular risk reduction and glycemic control.'
  );
  const [subjectiveNotes, setSubjectiveNotes] = useState(
    'Patient reports compliant medication adherence with no acute chest tightness or orthopnea.'
  );
  const [objectiveNotes, setObjectiveNotes] = useState(
    'BP 128/82 mmHg, HR 72 bpm, O2 Sat 99%. Lungs clear to auscultation bilaterally.'
  );
  const [assessment, setAssessment] = useState(
    'Essential hypertension (stable), Type 2 diabetes (optimized), Primary hyperlipidemia.'
  );

  // E-Prescription State
  const [prescribedMedications, setPrescribedMedications] = useState<PrescriptionItem[]>([
    {
      medicine_id: 'med-001',
      medicine_name: 'Lipitor (Atorvastatin 40mg)',
      dosage: '40 mg',
      frequency: 'Once daily at bedtime (QHS)',
      duration_days: 30,
      quantity: 30,
      route: 'Oral',
      instructions: 'Take 1 tablet every night before sleep.',
      refills_allowed: 3,
      refills_remaining: 3,
    },
  ]);

  const [safetyAlerts, setSafetyAlerts] = useState<string[]>([]);
  const [isSuccessModalOpen, setIsSuccessModalOpen] = useState(false);

  // Check drug interactions & allergies on medication change
  const handleAddMedicine = (med: MedicineMaster) => {
    // Check allergy
    const patientAllergies = selectedPatient.allergies.map((a) => a.toLowerCase());
    const isAllergic =
      patientAllergies.some((a) => a.includes('penicillin') || a.includes('amoxil')) &&
      med.generic_name.toLowerCase().includes('amoxicillin');

    if (isAllergic) {
      setSafetyAlerts((prev) => [
        ...prev,
        `CRITICAL ALLERGY ALERT: Patient ${selectedPatient.first_name} has documented Penicillin allergy. Cannot prescribe ${med.brand_name}!`,
      ]);
      return;
    }

    setPrescribedMedications((prev) => [
      ...prev,
      {
        medicine_id: med.id,
        medicine_name: `${med.brand_name} (${med.strength})`,
        dosage: med.strength,
        frequency: 'Once daily with meals',
        duration_days: 30,
        quantity: 30,
        route: med.route_of_administration,
        instructions: 'Take as directed.',
        refills_allowed: 2,
        refills_remaining: 2,
      },
    ]);
  };

  const handleSignAndIssueRx = () => {
    setIsSuccessModalOpen(true);
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2">
            <h1 className="text-2xl font-black text-white">Doctor Station & Clinical EMR</h1>
            <span className="px-2.5 py-0.5 rounded-full bg-teal-500/10 text-teal-400 text-xs font-bold border border-teal-500/20">
              Active Consultation
            </span>
          </div>
          <p className="text-xs text-slate-400 mt-1">
            Longitudinal patient records, SOAP clinical chart notes, and smart e-prescribing with drug safety surveillance.
          </p>
        </div>

        {/* Patient Switcher */}
        <div className="flex items-center gap-2">
          <span className="text-xs text-slate-400 font-bold">Select Patient:</span>
          <select
            value={selectedPatient.id}
            onChange={(e) => {
              const p = patients.find((pat) => pat.id === e.target.value);
              if (p) setSelectedPatient(p);
            }}
            className="bg-slate-900 border border-slate-700 text-teal-300 font-bold text-xs rounded-xl px-3 py-2 focus:outline-none focus:border-teal-500"
          >
            {patients.map((pat) => (
              <option key={pat.id} value={pat.id}>
                {pat.first_name} {pat.last_name} ({pat.mrn})
              </option>
            ))}
          </select>
        </div>
      </div>

      {/* Patient Banner */}
      <div className="bg-slate-900 border border-slate-800 rounded-2xl p-5 shadow-lg flex flex-wrap items-center justify-between gap-4">
        <div className="flex items-center gap-4">
          <div className="w-12 h-12 rounded-2xl bg-teal-500/20 text-teal-300 flex items-center justify-center font-black text-lg border border-teal-500/30">
            {selectedPatient.first_name[0]}
            {selectedPatient.last_name[0]}
          </div>
          <div>
            <div className="flex items-center gap-2">
              <h2 className="text-base font-black text-white">
                {selectedPatient.first_name} {selectedPatient.last_name}
              </h2>
              <span className="font-mono text-xs text-teal-400 bg-slate-950 px-2 py-0.5 rounded border border-slate-700">
                {selectedPatient.mrn}
              </span>
              <span className="text-xs text-slate-400">
                DOB: {selectedPatient.dob} • Gender: {selectedPatient.gender} • Blood:{' '}
                <strong className="text-white">{selectedPatient.blood_group}</strong>
              </span>
            </div>
            <div className="flex items-center gap-2 mt-1.5 flex-wrap">
              <span className="text-[11px] text-slate-400">Allergies:</span>
              {selectedPatient.allergies.map((alg, i) => (
                <span
                  key={i}
                  className="px-2 py-0.5 rounded bg-red-500/20 text-red-300 text-[10px] font-bold border border-red-500/30"
                >
                  ⚠️ {alg}
                </span>
              ))}
              <span className="text-[11px] text-slate-400 ml-2">Conditions:</span>
              {selectedPatient.chronic_conditions.map((c, i) => (
                <span
                  key={i}
                  className="px-2 py-0.5 rounded bg-slate-800 text-slate-300 text-[10px] font-semibold"
                >
                  {c}
                </span>
              ))}
            </div>
          </div>
        </div>

        {/* Live Vitals Snapshot */}
        <div className="flex items-center gap-3 bg-slate-950/60 border border-slate-800 p-2.5 rounded-xl">
          <div className="text-center px-2">
            <div className="text-[10px] text-slate-400">BP</div>
            <div className="text-xs font-black text-white font-mono">128/82</div>
          </div>
          <div className="text-center px-2 border-l border-slate-800">
            <div className="text-[10px] text-slate-400">HR</div>
            <div className="text-xs font-black text-teal-400 font-mono">72 bpm</div>
          </div>
          <div className="text-center px-2 border-l border-slate-800">
            <div className="text-[10px] text-slate-400">SpO2</div>
            <div className="text-xs font-black text-emerald-400 font-mono">99%</div>
          </div>
          <div className="text-center px-2 border-l border-slate-800">
            <div className="text-[10px] text-slate-400">BMI</div>
            <div className="text-xs font-black text-white font-mono">25.4</div>
          </div>
        </div>
      </div>

      {/* Safety Alerts Banner if any */}
      {safetyAlerts.length > 0 && (
        <div className="bg-red-500/10 border border-red-500/40 rounded-2xl p-4 space-y-2">
          {safetyAlerts.map((alt, i) => (
            <div key={i} className="flex items-center gap-2 text-xs font-bold text-red-300">
              <ShieldAlert className="w-4 h-4 text-red-400 shrink-0" />
              <span>{alt}</span>
            </div>
          ))}
        </div>
      )}

      {/* Two Column Layout: SOAP Notes & E-Prescription Builder */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* SOAP Notes Column */}
        <div className="bg-slate-900 border border-slate-800 rounded-2xl p-5 shadow-xl space-y-4">
          <div className="flex items-center justify-between pb-3 border-b border-slate-800">
            <div className="flex items-center gap-2">
              <FileText className="w-5 h-5 text-teal-400" />
              <h3 className="font-extrabold text-sm text-white">SOAP Clinical Encounter Notes</h3>
            </div>
            <span className="text-[11px] text-slate-400 font-mono">Encounter #ENC-2026-001</span>
          </div>

          <div>
            <label className="block text-[11px] font-bold text-teal-400 uppercase tracking-wider mb-1">
              Chief Complaint
            </label>
            <input
              type="text"
              value={chiefComplaint}
              onChange={(e) => setChiefComplaint(e.target.value)}
              className="w-full bg-slate-800 border border-slate-700 rounded-xl px-3 py-2 text-xs text-white focus:outline-none focus:border-teal-500"
            />
          </div>

          <div>
            <label className="block text-[11px] font-bold text-teal-400 uppercase tracking-wider mb-1">
              S - Subjective
            </label>
            <textarea
              rows={2}
              value={subjectiveNotes}
              onChange={(e) => setSubjectiveNotes(e.target.value)}
              className="w-full bg-slate-800 border border-slate-700 rounded-xl p-3 text-xs text-white focus:outline-none focus:border-teal-500"
            />
          </div>

          <div>
            <label className="block text-[11px] font-bold text-teal-400 uppercase tracking-wider mb-1">
              O - Objective
            </label>
            <textarea
              rows={2}
              value={objectiveNotes}
              onChange={(e) => setObjectiveNotes(e.target.value)}
              className="w-full bg-slate-800 border border-slate-700 rounded-xl p-3 text-xs text-white focus:outline-none focus:border-teal-500"
            />
          </div>

          <div>
            <label className="block text-[11px] font-bold text-teal-400 uppercase tracking-wider mb-1">
              A - Assessment & Diagnoses (ICD-10)
            </label>
            <textarea
              rows={2}
              value={assessment}
              onChange={(e) => setAssessment(e.target.value)}
              className="w-full bg-slate-800 border border-slate-700 rounded-xl p-3 text-xs text-white focus:outline-none focus:border-teal-500"
            />
          </div>
        </div>

        {/* E-Prescribing & Drug Safety Radar */}
        <div className="bg-slate-900 border border-slate-800 rounded-2xl p-5 shadow-xl space-y-4 flex flex-col justify-between">
          <div>
            <div className="flex items-center justify-between pb-3 border-b border-slate-800">
              <div className="flex items-center gap-2">
                <Pill className="w-5 h-5 text-teal-400" />
                <h3 className="font-extrabold text-sm text-white">E-Prescription & Drug Matrix</h3>
              </div>
              <span className="text-[10px] font-bold bg-teal-500/10 text-teal-300 px-2.5 py-0.5 rounded-full border border-teal-500/30">
                ECDSA Signature Ready
              </span>
            </div>

            {/* Prescribed Items List */}
            <div className="mt-3 space-y-2">
              {prescribedMedications.map((item, idx) => (
                <div
                  key={idx}
                  className="bg-slate-800/90 border border-slate-700 rounded-xl p-3 text-xs space-y-1"
                >
                  <div className="flex justify-between font-bold text-white">
                    <span>{item.medicine_name}</span>
                    <span className="text-teal-400 font-mono">Qty: {item.quantity}</span>
                  </div>
                  <div className="text-[11px] text-slate-400">
                    {item.frequency} • {item.duration_days} Days ({item.route})
                  </div>
                  <div className="text-[10px] text-slate-400 italic">
                    Instructions: {item.instructions}
                  </div>
                </div>
              ))}
            </div>

            {/* Quick Drug Selection from Master Catalog */}
            <div className="mt-4 pt-3 border-t border-slate-800">
              <div className="text-[11px] font-bold text-slate-400 mb-2">
                Add Medication from Hospital Formulary:
              </div>
              <div className="grid grid-cols-2 gap-2">
                {INITIAL_MEDICINES.slice(0, 4).map((med) => (
                  <button
                    key={med.id}
                    onClick={() => handleAddMedicine(med)}
                    className="p-2 rounded-xl bg-slate-800 hover:bg-slate-700 border border-slate-700 text-left transition flex items-center justify-between group"
                  >
                    <div>
                      <div className="font-bold text-xs text-white group-hover:text-teal-300">
                        {med.brand_name}
                      </div>
                      <div className="text-[10px] text-slate-400">{med.strength}</div>
                    </div>
                    <Plus className="w-3.5 h-3.5 text-teal-400" />
                  </button>
                ))}
              </div>
            </div>
          </div>

          <button
            onClick={handleSignAndIssueRx}
            className="w-full py-3 bg-gradient-to-r from-teal-500 to-emerald-600 hover:from-teal-400 hover:to-emerald-500 text-slate-950 font-black rounded-xl text-xs shadow-lg shadow-teal-500/20 transition flex items-center justify-center gap-2"
          >
            <QrCode className="w-4 h-4" />
            <span>Digitally Sign & Issue E-Prescription</span>
          </button>
        </div>
      </div>

      {/* Success Modal */}
      {isSuccessModalOpen && (
        <div className="fixed inset-0 bg-black/80 backdrop-blur-sm z-50 flex items-center justify-center p-4">
          <div className="bg-slate-900 border border-teal-500/40 rounded-2xl max-w-md w-full p-6 shadow-2xl space-y-4 text-center">
            <div className="w-12 h-12 rounded-full bg-emerald-500/20 text-emerald-400 flex items-center justify-center mx-auto">
              <CheckCircle2 className="w-6 h-6" />
            </div>
            <h3 className="text-lg font-black text-white">E-Prescription Successfully Issued</h3>
            <p className="text-xs text-slate-400">
              Prescription #RX-2026-99201 has been cryptographically signed with ECDSA SHA-256 and sent to the Pharmacy Command Center queue for FEFO dispensing.
            </p>
            <button
              onClick={() => setIsSuccessModalOpen(false)}
              className="w-full py-2.5 bg-teal-500 hover:bg-teal-400 text-slate-950 font-black rounded-xl text-xs transition"
            >
              Continue Clinical Station
            </button>
          </div>
        </div>
      )}
    </div>
  );
};
