import React, { useState } from 'react';
import {
  Building2,
  Bed,
  Layers,
  MapPin,
  CheckCircle2,
  AlertCircle,
  Phone,
  Mail,
} from 'lucide-react';

export const OrganizationView: React.FC = () => {
  const [hospitals] = useState([
    {
      id: 'hosp-001',
      name: 'MediCore Central Hospital & Advanced Medical Center',
      code: 'MCH-01',
      license: 'MED-LIC-884920',
      address: '742 Evergreen Healthcare Blvd, Boston, MA 02115',
      phone: '+1 (555) 019-2000',
      totalBeds: 350,
      occupiedBeds: 295,
      departments: [
        { name: 'Cardiology & Vascular Institute', code: 'CARD', floor: 3, head: 'Dr. Sarah Chen, MD' },
        { name: 'Central Pharmacy Operations', code: 'PHARM', floor: 1, head: 'Marcus Vance, PharmD' },
        { name: 'Emergency & Trauma Medicine', code: 'ER', floor: 1, head: 'Dr. Robert Reynolds, MD' },
        { name: 'Clinical Pathology & Molecular Lab', code: 'LAB', floor: 2, head: 'David Kim, MLS' },
      ],
    },
  ]);

  const beds = [
    { room: 'ICU-301', bed: 'A', dept: 'Cardiology', type: 'ICU', patient: 'Eleanor Vance', status: 'Occupied' },
    { room: 'ICU-301', bed: 'B', dept: 'Cardiology', type: 'ICU', patient: null, status: 'Available' },
    { room: 'BAY-104', bed: 'Bay 1', dept: 'Emergency', type: 'Emergency', patient: 'Michael Chang', status: 'Occupied' },
    { room: 'MED-202', bed: 'Bed 1', dept: 'Internal Med', type: 'Standard Inpatient', patient: null, status: 'Available' },
    { room: 'MED-202', bed: 'Bed 2', dept: 'Internal Med', type: 'Standard Inpatient', patient: null, status: 'Available' },
  ];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <div className="flex items-center gap-2">
            <h1 className="text-2xl font-black text-white">Hospital & Ward Structure</h1>
            <span className="px-2.5 py-0.5 rounded-full bg-teal-500/10 text-teal-400 text-xs font-bold border border-teal-500/20">
              Multi-Facility Management
            </span>
          </div>
          <p className="text-xs text-slate-400 mt-1">
            Hierarchy of organizations, hospital branches, clinical departments, inpatient wards, and real-time bed allocation.
          </p>
        </div>
      </div>

      {/* Hospital Overview Card */}
      <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-xl space-y-4">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 pb-4 border-b border-slate-800">
          <div>
            <div className="flex items-center gap-2">
              <Building2 className="w-6 h-6 text-teal-400" />
              <h2 className="text-lg font-black text-white">{hospitals[0].name}</h2>
            </div>
            <div className="text-xs text-slate-400 mt-1 flex items-center gap-1">
              <MapPin className="w-3.5 h-3.5 text-teal-400" />
              <span>{hospitals[0].address}</span>
            </div>
          </div>
          <div className="text-right font-mono">
            <div className="text-2xl font-black text-white">
              {hospitals[0].occupiedBeds} / {hospitals[0].totalBeds}
            </div>
            <div className="text-xs text-teal-400 font-bold">Inpatient Beds Occupied (84.2%)</div>
          </div>
        </div>

        {/* Departments Grid */}
        <div>
          <h3 className="font-extrabold text-xs text-slate-400 uppercase tracking-wider mb-3">
            Clinical Departments
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-3">
            {hospitals[0].departments.map((dept, i) => (
              <div
                key={i}
                className="bg-slate-800/80 border border-slate-700 rounded-xl p-3 text-xs space-y-1"
              >
                <div className="font-bold text-white text-sm">{dept.name}</div>
                <div className="text-teal-300 font-mono text-[11px]">
                  Floor {dept.floor} • Code: {dept.code}
                </div>
                <div className="text-[10px] text-slate-400">Head: {dept.head}</div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Real-Time Inpatient Bed Matrix */}
      <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-xl space-y-4">
        <div className="flex items-center justify-between pb-3 border-b border-slate-800">
          <div className="flex items-center gap-2">
            <Bed className="w-5 h-5 text-teal-400" />
            <h3 className="font-extrabold text-sm text-white">Real-Time Inpatient Bed Status Map</h3>
          </div>
          <span className="text-xs text-slate-400 font-mono">5 Sample Bays Monitored</span>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-3">
          {beds.map((b, idx) => (
            <div
              key={idx}
              className={`rounded-xl p-3.5 border text-xs space-y-1.5 transition ${
                b.status === 'Occupied'
                  ? 'bg-slate-800/90 border-teal-500/40'
                  : 'bg-slate-950/60 border-slate-800'
              }`}
            >
              <div className="flex items-center justify-between">
                <span className="font-black text-white font-mono">{b.room}</span>
                <span
                  className={`text-[9px] font-extrabold px-2 py-0.5 rounded-full ${
                    b.status === 'Occupied'
                      ? 'bg-teal-500/20 text-teal-300 border border-teal-500/30'
                      : 'bg-emerald-500/20 text-emerald-300 border border-emerald-500/30'
                  }`}
                >
                  {b.status}
                </span>
              </div>
              <div className="text-[11px] text-slate-400">
                {b.dept} • Bed {b.bed}
              </div>
              {b.patient ? (
                <div className="text-xs font-bold text-teal-300 truncate">👤 {b.patient}</div>
              ) : (
                <div className="text-xs text-slate-500 italic">Available for Admission</div>
              )}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
