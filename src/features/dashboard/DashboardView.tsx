import React from 'react';
import {
  Activity,
  DollarSign,
  Pill,
  Users,
  Calendar,
  AlertTriangle,
  ShieldAlert,
  ArrowUpRight,
  TrendingUp,
  Clock,
  Sparkles,
  CheckCircle2,
  Package,
} from 'lucide-react';
import { User } from '../../types';

interface DashboardViewProps {
  currentUser: User | null;
  onNavigate: (tab: string) => void;
}

export const DashboardView: React.FC<DashboardViewProps> = ({
  currentUser,
  onNavigate,
}) => {
  const stats = [
    {
      title: "Today's Pharmacy Sales",
      value: '$3,480.50',
      change: '+14.2% vs yesterday',
      icon: DollarSign,
      color: 'text-emerald-400',
      bg: 'bg-emerald-500/10',
      border: 'border-emerald-500/30',
      actionTab: 'pos',
    },
    {
      title: 'Prescriptions Dispensed',
      value: '42 / 47',
      change: '5 pending validation',
      icon: Pill,
      color: 'text-teal-400',
      bg: 'bg-teal-500/10',
      border: 'border-teal-500/30',
      actionTab: 'pharmacy_center',
    },
    {
      title: 'Inpatient Bed Occupancy',
      value: '84.2%',
      change: '295 / 350 beds occupied',
      icon: Users,
      color: 'text-blue-400',
      bg: 'bg-blue-500/10',
      border: 'border-blue-500/30',
      actionTab: 'organization',
    },
    {
      title: 'FEFO Expiry Alerts',
      value: '2 Batches',
      change: 'Expires within 30 days',
      icon: AlertTriangle,
      color: 'text-amber-400',
      bg: 'bg-amber-500/10',
      border: 'border-amber-500/30',
      actionTab: 'inventory',
    },
  ];

  return (
    <div className="space-y-6">
      {/* Welcome Banner */}
      <div className="bg-gradient-to-r from-slate-900 via-slate-800 to-slate-900 border border-slate-800 rounded-2xl p-6 shadow-xl relative overflow-hidden">
        <div className="absolute right-0 top-0 bottom-0 w-1/3 bg-gradient-to-l from-teal-500/10 to-transparent pointer-events-none"></div>
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 relative z-10">
          <div>
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-teal-500/10 border border-teal-500/30 text-teal-300 text-xs font-bold mb-2">
              <Sparkles className="w-3.5 h-3.5 text-teal-400 animate-pulse" />
              <span>Smart Hospital & Pharmacy Clinical Engine</span>
            </div>
            <h1 className="text-2xl font-black text-white">
              Welcome back, {currentUser?.full_name || 'Healthcare Specialist'}
            </h1>
            <p className="text-xs text-slate-400 mt-1 max-w-2xl">
              All 24 domain subsystems are synchronized. Drug interaction matrix active, Smart FEFO dispensing online, and emergency triage operational.
            </p>
          </div>

          {/* Quick Launch Buttons */}
          <div className="flex items-center gap-2.5 flex-wrap">
            <button
              onClick={() => onNavigate('pos')}
              className="px-4 py-2 bg-gradient-to-r from-teal-500 to-emerald-600 hover:from-teal-400 hover:to-emerald-500 text-slate-950 text-xs font-black rounded-xl shadow-lg shadow-teal-500/20 transition flex items-center gap-1.5"
            >
              <span>Scan POS Barcode</span>
              <ArrowUpRight className="w-3.5 h-3.5" />
            </button>
            <button
              onClick={() => onNavigate('clinical')}
              className="px-4 py-2 bg-slate-800 hover:bg-slate-700 text-white text-xs font-bold rounded-xl border border-slate-700 transition flex items-center gap-1.5"
            >
              <span>Doctor Station</span>
            </button>
            <button
              onClick={() => onNavigate('pharmacy_center')}
              className="px-4 py-2 bg-slate-800 hover:bg-slate-700 text-teal-300 text-xs font-bold rounded-xl border border-slate-700 transition flex items-center gap-1.5"
            >
              <span>Command Center</span>
            </button>
          </div>
        </div>
      </div>

      {/* KPI Cards Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {stats.map((st, i) => {
          const Icon = st.icon;
          return (
            <div
              key={i}
              onClick={() => onNavigate(st.actionTab)}
              className={`bg-slate-900/90 border ${st.border} rounded-2xl p-5 shadow-lg backdrop-blur hover:scale-[1.01] transition cursor-pointer group`}
            >
              <div className="flex items-center justify-between">
                <span className="text-xs font-bold text-slate-400">{st.title}</span>
                <div className={`w-9 h-9 rounded-xl ${st.bg} flex items-center justify-center ${st.color}`}>
                  <Icon className="w-5 h-5" />
                </div>
              </div>
              <div className="text-2xl font-black text-white mt-3">{st.value}</div>
              <div className="flex items-center gap-1 text-[11px] font-semibold text-slate-400 mt-1">
                <span>{st.change}</span>
              </div>
            </div>
          );
        })}
      </div>

      {/* Two Column Section: Real-time Pharmacy Flow & Clinical Risk Radar */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Active Pharmacy Queue */}
        <div className="lg:col-span-2 bg-slate-900 border border-slate-800 rounded-2xl p-5 shadow-lg">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h3 className="font-extrabold text-sm text-white">
                Active Prescription & Dispensing Queue
              </h3>
              <p className="text-xs text-slate-400 mt-0.5">
                Real-time FEFO validation and pharmacist safety reviews
              </p>
            </div>
            <button
              onClick={() => onNavigate('pharmacy_center')}
              className="text-xs text-teal-400 font-bold hover:underline"
            >
              View Command Center →
            </button>
          </div>

          <div className="divide-y divide-slate-800">
            <div className="py-3 flex items-center justify-between">
              <div className="flex items-center gap-3">
                <div className="w-8 h-8 rounded-lg bg-teal-500/10 text-teal-400 flex items-center justify-center font-bold text-xs border border-teal-500/20">
                  Rx1
                </div>
                <div>
                  <div className="font-bold text-xs text-white">Eleanor Vance (MRN-2026-004128)</div>
                  <div className="text-[11px] text-slate-400">Lipitor 40mg (30 Tabs), Glucophage XR 500mg (60 Tabs)</div>
                </div>
              </div>
              <div className="text-right">
                <span className="px-2.5 py-1 rounded-full text-[10px] font-extrabold bg-emerald-500/10 text-emerald-400 border border-emerald-500/30">
                  Ready to Dispense
                </span>
                <div className="text-[10px] text-slate-500 mt-0.5">FEFO Batch #ATV-2026-B1</div>
              </div>
            </div>

            <div className="py-3 flex items-center justify-between">
              <div className="flex items-center gap-3">
                <div className="w-8 h-8 rounded-lg bg-amber-500/10 text-amber-400 flex items-center justify-center font-bold text-xs border border-amber-500/20">
                  Rx2
                </div>
                <div>
                  <div className="font-bold text-xs text-white">Michael Chang (MRN-2026-004129)</div>
                  <div className="text-[11px] text-slate-400">Ventolin HFA Inhaler 100mcg (1 Canister)</div>
                </div>
              </div>
              <div className="text-right">
                <span className="px-2.5 py-1 rounded-full text-[10px] font-extrabold bg-amber-500/10 text-amber-400 border border-amber-500/30">
                  Pending Validation
                </span>
                <div className="text-[10px] text-slate-500 mt-0.5">AERD Allergy Warning Checked</div>
              </div>
            </div>
          </div>
        </div>

        {/* Medicine Risk Radar Widget */}
        <div className="bg-slate-900 border border-slate-800 rounded-2xl p-5 shadow-lg flex flex-col justify-between">
          <div>
            <div className="flex items-center gap-2 mb-2">
              <ShieldAlert className="w-5 h-5 text-teal-400" />
              <h3 className="font-extrabold text-sm text-white">Medicine Risk Radar</h3>
            </div>
            <p className="text-xs text-slate-400">
              Live automated clinical surveillance of drug-drug interactions, allergies, and contraindications.
            </p>

            <div className="mt-4 space-y-2.5">
              <div className="flex items-center justify-between p-2.5 rounded-xl bg-slate-800/80 border border-slate-700">
                <div className="flex items-center gap-2">
                  <span className="w-3 h-3 rounded-full bg-red-500 animate-pulse"></span>
                  <span className="text-xs font-bold text-white">Critical Risk Alerts</span>
                </div>
                <span className="text-xs font-black text-red-400">0 Active</span>
              </div>

              <div className="flex items-center justify-between p-2.5 rounded-xl bg-slate-800/80 border border-slate-700">
                <div className="flex items-center gap-2">
                  <span className="w-3 h-3 rounded-full bg-amber-500"></span>
                  <span className="text-xs font-bold text-white">Moderate Intercepts</span>
                </div>
                <span className="text-xs font-black text-amber-400">3 Logged</span>
              </div>

              <div className="flex items-center justify-between p-2.5 rounded-xl bg-slate-800/80 border border-slate-700">
                <div className="flex items-center gap-2">
                  <span className="w-3 h-3 rounded-full bg-emerald-500"></span>
                  <span className="text-xs font-bold text-white">Safe Verifications</span>
                </div>
                <span className="text-xs font-black text-emerald-400">142 Today</span>
              </div>
            </div>
          </div>

          <button
            onClick={() => onNavigate('drug_safety')}
            className="w-full mt-4 py-2 bg-slate-800 hover:bg-slate-700 border border-slate-700 rounded-xl text-xs font-bold text-teal-300 transition"
          >
            Launch Safety Matrix →
          </button>
        </div>
      </div>
    </div>
  );
};
