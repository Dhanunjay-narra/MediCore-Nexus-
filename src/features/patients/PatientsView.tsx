import React, { useState } from 'react';
import {
  Users,
  Search,
  Plus,
  Phone,
  Mail,
  MapPin,
  Calendar,
  AlertTriangle,
  HeartPulse,
  Clock,
  FileText,
} from 'lucide-react';
import { INITIAL_PATIENTS } from '../../services/api';
import { Patient } from '../../types';

export const PatientsView: React.FC = () => {
  const [patients] = useState<Patient[]>(INITIAL_PATIENTS);
  const [searchQuery, setSearchQuery] = useState('');
  const [activePatient, setActivePatient] = useState<Patient>(INITIAL_PATIENTS[0]);

  const filteredPatients = patients.filter(
    (p) =>
      p.first_name.toLowerCase().includes(searchQuery.toLowerCase()) ||
      p.last_name.toLowerCase().includes(searchQuery.toLowerCase()) ||
      p.mrn.toLowerCase().includes(searchQuery.toLowerCase()) ||
      p.phone.includes(searchQuery)
  );

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2">
            <h1 className="text-2xl font-black text-white">Master Patient Index (MPI)</h1>
            <span className="px-2.5 py-0.5 rounded-full bg-teal-500/10 text-teal-400 text-xs font-bold border border-teal-500/20">
              Enterprise MPI
            </span>
          </div>
          <p className="text-xs text-slate-400 mt-1">
            Centralized demographic registry, longitudinal medical timeline, and allergy risk indicators.
          </p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Patients Registry List */}
        <div className="space-y-3">
          <div className="bg-slate-900 border border-slate-800 rounded-2xl p-3 shadow-lg">
            <div className="relative">
              <Search className="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" />
              <input
                type="text"
                placeholder="Search MRN, patient name, phone..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="w-full bg-slate-800 border border-slate-700 rounded-xl pl-9 pr-3 py-2 text-xs text-white placeholder:text-slate-400 focus:outline-none focus:border-teal-500"
              />
            </div>
          </div>

          <div className="space-y-2 max-h-[calc(100vh-16rem)] overflow-y-auto pr-1">
            {filteredPatients.map((p) => {
              const isSelected = activePatient.id === p.id;
              return (
                <div
                  key={p.id}
                  onClick={() => setActivePatient(p)}
                  className={`p-4 rounded-2xl border transition cursor-pointer ${
                    isSelected
                      ? 'bg-slate-800 border-teal-500/50 shadow-lg shadow-teal-500/10'
                      : 'bg-slate-900/90 border-slate-800 hover:border-slate-700'
                  }`}
                >
                  <div className="flex items-center justify-between">
                    <span className="font-extrabold text-sm text-white">
                      {p.first_name} {p.last_name}
                    </span>
                    <span className="font-mono text-[10px] text-teal-400 bg-slate-950 px-2 py-0.5 rounded border border-slate-700">
                      {p.mrn}
                    </span>
                  </div>
                  <div className="text-xs text-slate-400 mt-1">
                    DOB: {p.dob} • Gender: {p.gender} • Blood: <strong>{p.blood_group}</strong>
                  </div>
                  <div className="text-[11px] text-slate-500 mt-1 flex items-center gap-1">
                    <Phone className="w-3 h-3" />
                    <span>{p.phone}</span>
                  </div>
                </div>
              );
            })}
          </div>
        </div>

        {/* Selected Patient Comprehensive Chart */}
        <div className="lg:col-span-2 space-y-4">
          <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-xl space-y-5">
            {/* Demographic Profile */}
            <div className="flex items-start justify-between pb-4 border-b border-slate-800">
              <div className="flex items-center gap-4">
                <div className="w-14 h-14 rounded-2xl bg-teal-500/20 text-teal-300 flex items-center justify-center font-black text-xl border border-teal-500/30">
                  {activePatient.first_name[0]}
                  {activePatient.last_name[0]}
                </div>
                <div>
                  <h2 className="text-lg font-black text-white">
                    {activePatient.first_name} {activePatient.last_name}
                  </h2>
                  <div className="text-xs text-slate-400 mt-0.5">
                    MRN: <span className="font-mono text-teal-400 font-bold">{activePatient.mrn}</span>{' '}
                    • Registered: {new Date(activePatient.created_at).toLocaleDateString()}
                  </div>
                  <div className="text-xs text-slate-400 mt-0.5 flex items-center gap-1">
                    <MapPin className="w-3.5 h-3.5 text-teal-400" />
                    <span>
                      {activePatient.address}, {activePatient.city}, {activePatient.state}{' '}
                      {activePatient.zip_code}
                    </span>
                  </div>
                </div>
              </div>

              <div className="text-right">
                <span className="text-[10px] font-extrabold px-3 py-1 rounded-full bg-emerald-500/20 text-emerald-300 border border-emerald-500/30">
                  ACTIVE PATIENT
                </span>
                <div className="text-xs text-slate-400 mt-1 font-semibold">
                  {activePatient.insurance_provider}
                </div>
              </div>
            </div>

            {/* Medical Alerts & Allergies */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="bg-red-500/10 border border-red-500/30 rounded-xl p-3.5">
                <div className="flex items-center gap-2 text-xs font-black text-red-400 uppercase tracking-wider mb-2">
                  <AlertTriangle className="w-4 h-4" />
                  <span>Documented Allergies</span>
                </div>
                <div className="flex flex-wrap gap-1.5">
                  {activePatient.allergies.map((a, i) => (
                    <span
                      key={i}
                      className="px-2 py-1 rounded-md bg-red-500/20 text-red-300 text-xs font-bold border border-red-500/30"
                    >
                      {a}
                    </span>
                  ))}
                </div>
              </div>

              <div className="bg-slate-800/80 border border-slate-700 rounded-xl p-3.5">
                <div className="flex items-center gap-2 text-xs font-black text-teal-400 uppercase tracking-wider mb-2">
                  <HeartPulse className="w-4 h-4" />
                  <span>Chronic Conditions</span>
                </div>
                <div className="flex flex-wrap gap-1.5">
                  {activePatient.chronic_conditions.map((c, i) => (
                    <span
                      key={i}
                      className="px-2 py-1 rounded-md bg-slate-900 text-slate-300 text-xs font-semibold border border-slate-700"
                    >
                      {c}
                    </span>
                  ))}
                </div>
              </div>
            </div>

            {/* Longitudinal Medical Timeline */}
            <div className="pt-3 border-t border-slate-800">
              <h3 className="font-extrabold text-sm text-white mb-3">Longitudinal Patient Timeline</h3>
              <div className="space-y-3 relative before:absolute before:left-3.5 before:top-2 before:bottom-2 before:w-0.5 before:bg-slate-800 pl-8">
                <div className="relative">
                  <span className="absolute -left-8 top-1 w-3.5 h-3.5 rounded-full bg-teal-400 ring-4 ring-slate-900"></span>
                  <div className="bg-slate-800/80 border border-slate-700/80 rounded-xl p-3 text-xs">
                    <div className="flex items-center justify-between font-bold text-white">
                      <span>Comprehensive Cardiac Follow-up Consultation</span>
                      <span className="text-[10px] text-slate-400 font-mono">2026-08-28</span>
                    </div>
                    <p className="text-slate-300 text-[11px] mt-1">
                      Dr. Sarah Chen, MD — Blood pressure controlled. Adjusted Atorvastatin to 40mg.
                    </p>
                  </div>
                </div>

                <div className="relative">
                  <span className="absolute -left-8 top-1 w-3.5 h-3.5 rounded-full bg-emerald-400 ring-4 ring-slate-900"></span>
                  <div className="bg-slate-800/80 border border-slate-700/80 rounded-xl p-3 text-xs">
                    <div className="flex items-center justify-between font-bold text-white">
                      <span>E-Prescription Dispensed (FEFO Batch #ATV-2026-B1)</span>
                      <span className="text-[10px] text-slate-400 font-mono">2026-08-28</span>
                    </div>
                    <p className="text-slate-300 text-[11px] mt-1">
                      Marcus Vance, PharmD — Dispensed Lipitor 40mg (30 Tabs), Glucophage XR 500mg (60 Tabs).
                    </p>
                  </div>
                </div>

                <div className="relative">
                  <span className="absolute -left-8 top-1 w-3.5 h-3.5 rounded-full bg-blue-400 ring-4 ring-slate-900"></span>
                  <div className="bg-slate-800/80 border border-slate-700/80 rounded-xl p-3 text-xs">
                    <div className="flex items-center justify-between font-bold text-white">
                      <span>Lab Test Results Verified: Lipid & Metabolic Panel</span>
                      <span className="text-[10px] text-slate-400 font-mono">2026-08-25</span>
                    </div>
                    <p className="text-slate-300 text-[11px] mt-1">
                      David Kim, MLS — HbA1c: 6.8%, LDL: 94 mg/dL, eGFR: 92 mL/min/1.73m².
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
