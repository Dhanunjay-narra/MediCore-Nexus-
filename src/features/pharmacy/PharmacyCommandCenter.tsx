import React, { useState } from 'react';
import {
  Activity,
  AlertTriangle,
  Pill,
  Clock,
  ShieldAlert,
  CheckCircle2,
  Package,
  Layers,
  ArrowRight,
  TrendingUp,
  Sparkles,
} from 'lucide-react';
import { INITIAL_PRESCRIPTIONS, INITIAL_BATCHES } from '../../services/api';

export const PharmacyCommandCenter: React.FC = () => {
  const [prescriptions, setPrescriptions] = useState(INITIAL_PRESCRIPTIONS);
  const [batches] = useState(INITIAL_BATCHES);

  const handleValidateRx = (rxId: string) => {
    setPrescriptions((prev) =>
      prev.map((r) =>
        r.id === rxId
          ? {
              ...r,
              status: 'Validated',
              validated_at: new Date().toISOString(),
              validated_by_pharmacist: 'Marcus Vance, PharmD',
            }
          : r
      )
    );
  };

  const handleDispenseRx = (rxId: string) => {
    setPrescriptions((prev) =>
      prev.map((r) =>
        r.id === rxId ? { ...r, status: 'Dispensed' } : r
      )
    );
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2">
            <h1 className="text-2xl font-black text-white">Pharmacy Command Center</h1>
            <span className="px-2.5 py-0.5 rounded-full bg-teal-500/10 text-teal-400 text-xs font-bold border border-teal-500/20">
              Live Operations
            </span>
          </div>
          <p className="text-xs text-slate-400 mt-1">
            Real-time dispensing engine, Smart FEFO prioritization, and automated pharmacist clinical reviews.
          </p>
        </div>
      </div>

      {/* Command Center Quick Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="bg-slate-900 border border-slate-800 rounded-2xl p-4 shadow-lg">
          <div className="flex items-center justify-between text-slate-400 text-xs font-bold">
            <span>Today's Rx Volume</span>
            <Pill className="w-4 h-4 text-teal-400" />
          </div>
          <div className="text-2xl font-black text-white mt-2">42 Dispensed</div>
          <div className="text-[11px] text-teal-400 font-semibold mt-1">98.4% FEFO Compliant</div>
        </div>

        <div className="bg-slate-900 border border-slate-800 rounded-2xl p-4 shadow-lg">
          <div className="flex items-center justify-between text-slate-400 text-xs font-bold">
            <span>Pending Validation</span>
            <Clock className="w-4 h-4 text-amber-400" />
          </div>
          <div className="text-2xl font-black text-white mt-2">
            {prescriptions.filter((p) => p.status === 'Active').length} Prescriptions
          </div>
          <div className="text-[11px] text-amber-400 font-semibold mt-1">Avg Wait: 4.2 mins</div>
        </div>

        <div className="bg-slate-900 border border-slate-800 rounded-2xl p-4 shadow-lg">
          <div className="flex items-center justify-between text-slate-400 text-xs font-bold">
            <span>Expiring Batches (30d)</span>
            <AlertTriangle className="w-4 h-4 text-red-400" />
          </div>
          <div className="text-2xl font-black text-white mt-2">
            {batches.filter((b) => b.days_to_expiry <= 30).length} Batches
          </div>
          <div className="text-[11px] text-red-400 font-semibold mt-1">Priority Dispense Triggered</div>
        </div>

        <div className="bg-slate-900 border border-slate-800 rounded-2xl p-4 shadow-lg">
          <div className="flex items-center justify-between text-slate-400 text-xs font-bold">
            <span>Low Stock Reorders</span>
            <Package className="w-4 h-4 text-cyan-400" />
          </div>
          <div className="text-2xl font-black text-white mt-2">
            {batches.filter((b) => b.is_low_stock).length} Items
          </div>
          <div className="text-[11px] text-cyan-400 font-semibold mt-1">PO-2026-00891 In Progress</div>
        </div>
      </div>

      {/* Main Prescriptions Dispensing Queue */}
      <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-xl">
        <div className="flex items-center justify-between mb-4">
          <div>
            <h2 className="font-extrabold text-base text-white">
              Prescription Validation & Dispensing Queue
            </h2>
            <p className="text-xs text-slate-400 mt-0.5">
              Review digital signatures, check patient allergy history, and assign Smart FEFO batches.
            </p>
          </div>
        </div>

        <div className="space-y-4">
          {prescriptions.map((rx) => {
            const isValidated = rx.status === 'Validated';
            const isDispensed = rx.status === 'Dispensed';

            return (
              <div
                key={rx.id}
                className={`rounded-2xl p-5 border transition ${
                  isDispensed
                    ? 'bg-slate-900/60 border-slate-800 opacity-80'
                    : isValidated
                    ? 'bg-slate-800/60 border-teal-500/40 shadow-lg shadow-teal-500/5'
                    : 'bg-slate-800/80 border-amber-500/40 shadow-lg shadow-amber-500/5'
                }`}
              >
                <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-4">
                  <div>
                    <div className="flex items-center gap-2.5">
                      <span className="font-mono font-bold text-xs text-teal-400 bg-slate-950 px-2 py-0.5 rounded border border-slate-700">
                        {rx.rx_number}
                      </span>
                      <span className="font-extrabold text-sm text-white">{rx.patient_name}</span>
                      <span
                        className={`text-[10px] font-extrabold px-2.5 py-0.5 rounded-full ${
                          isDispensed
                            ? 'bg-slate-700 text-slate-300'
                            : isValidated
                            ? 'bg-teal-500/20 text-teal-300 border border-teal-500/30'
                            : 'bg-amber-500/20 text-amber-300 border border-amber-500/30'
                        }`}
                      >
                        {rx.status.toUpperCase()}
                      </span>
                    </div>

                    <div className="text-xs text-slate-400 mt-1">
                      Prescribed by <span className="text-slate-200 font-semibold">{rx.doctor_name}</span> • Diagnosis:{' '}
                      <span className="text-slate-300">{rx.diagnosis_summary}</span>
                    </div>

                    {/* Prescription Line Items */}
                    <div className="mt-3 grid grid-cols-1 md:grid-cols-2 gap-2">
                      {rx.items.map((it, idx) => (
                        <div
                          key={idx}
                          className="bg-slate-950/60 border border-slate-800 rounded-xl p-2.5 text-xs"
                        >
                          <div className="font-bold text-white flex items-center justify-between">
                            <span>{it.medicine_name}</span>
                            <span className="text-teal-400 font-mono">Qty: {it.quantity}</span>
                          </div>
                          <div className="text-slate-400 text-[11px] mt-0.5">
                            {it.dosage} • {it.frequency} • {it.duration_days} Days
                          </div>
                          <div className="text-slate-400 text-[10px] mt-0.5 italic">
                            "{it.instructions}"
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>

                  {/* Actions Column */}
                  <div className="flex flex-row lg:flex-col items-end justify-between gap-2 shrink-0">
                    <div className="text-right">
                      <div className="text-[10px] text-slate-400">Digital Signature Hash</div>
                      <div className="text-[10px] font-mono text-slate-400 truncate max-w-[180px]">
                        {rx.digital_signature_hash}
                      </div>
                    </div>

                    <div className="flex items-center gap-2 mt-2">
                      {!isValidated && !isDispensed && (
                        <button
                          onClick={() => handleValidateRx(rx.id)}
                          className="px-4 py-2 bg-gradient-to-r from-teal-500 to-emerald-600 hover:from-teal-400 hover:to-emerald-500 text-slate-950 font-black text-xs rounded-xl shadow-md transition flex items-center gap-1"
                        >
                          <CheckCircle2 className="w-3.5 h-3.5" />
                          <span>Validate Rx</span>
                        </button>
                      )}

                      {isValidated && !isDispensed && (
                        <button
                          onClick={() => handleDispenseRx(rx.id)}
                          className="px-4 py-2 bg-gradient-to-r from-emerald-500 to-teal-600 hover:from-emerald-400 hover:to-teal-500 text-slate-950 font-black text-xs rounded-xl shadow-md transition flex items-center gap-1"
                        >
                          <Package className="w-3.5 h-3.5" />
                          <span>Dispense (FEFO)</span>
                        </button>
                      )}

                      {isDispensed && (
                        <span className="px-3 py-1.5 rounded-xl bg-slate-800 text-slate-400 text-xs font-bold flex items-center gap-1">
                          <CheckCircle2 className="w-3.5 h-3.5 text-teal-400" />
                          <span>Dispensed</span>
                        </span>
                      )}
                    </div>
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
};
