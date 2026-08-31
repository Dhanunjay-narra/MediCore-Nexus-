import React from 'react';
import {
  Activity,
  Bell,
  Shield,
  Search,
  Sparkles,
  LogOut,
  ChevronDown,
  Building2,
} from 'lucide-react';
import { User } from '../../types';

interface NavbarProps {
  currentUser: User | null;
  onLogout: () => void;
  onOpenAI: () => void;
  activeHospital: string;
}

export const Navbar: React.FC<NavbarProps> = ({
  currentUser,
  onLogout,
  onOpenAI,
  activeHospital,
}) => {
  return (
    <header className="h-16 bg-slate-900/90 backdrop-blur border-b border-slate-800 sticky top-0 z-30 px-6 flex items-center justify-between">
      {/* Brand & Hospital Selection */}
      <div className="flex items-center gap-4">
        <div className="flex items-center gap-2.5">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-teal-500 via-emerald-500 to-cyan-400 flex items-center justify-center shadow-lg shadow-teal-500/20 text-slate-950 font-black text-xl">
            M
          </div>
          <div>
            <div className="flex items-center gap-1.5">
              <span className="font-extrabold text-lg text-white tracking-tight">
                MediCore <span className="text-teal-400">Nexus</span>
              </span>
              <span className="text-[10px] uppercase font-bold bg-teal-950 text-teal-300 px-2 py-0.5 rounded-full border border-teal-800/60">
                v1.0 Enterprise
              </span>
            </div>
            <div className="flex items-center gap-1 text-xs text-slate-400">
              <Building2 className="w-3 h-3 text-teal-400" />
              <span>{activeHospital}</span>
            </div>
          </div>
        </div>
      </div>

      {/* Global Quick Search & AI Assistant Launcher */}
      <div className="hidden md:flex items-center gap-3 max-w-md w-full mx-6">
        <div className="relative w-full">
          <Search className="w-4 h-4 absolute left-3.5 top-1/2 -translate-y-1/2 text-slate-400" />
          <input
            type="text"
            placeholder="Search patients by MRN, drugs, prescriptions, batches, ICD-10..."
            className="w-full bg-slate-800/80 border border-slate-700/80 rounded-xl pl-10 pr-4 py-2 text-xs text-slate-200 placeholder:text-slate-400 focus:outline-none focus:border-teal-500 focus:ring-1 focus:ring-teal-500/30 transition"
          />
        </div>
        <button
          onClick={onOpenAI}
          className="flex items-center gap-1.5 px-3 py-2 bg-gradient-to-r from-teal-600 to-emerald-600 hover:from-teal-500 hover:to-emerald-500 text-white rounded-xl text-xs font-bold transition shadow-sm whitespace-nowrap"
        >
          <Sparkles className="w-3.5 h-3.5 text-teal-200 animate-pulse" />
          <span>AI Assistant</span>
        </button>
      </div>

      {/* User Persona & Role Badge */}
      <div className="flex items-center gap-4">
        {/* Notification Bell */}
        <button className="relative p-2 text-slate-400 hover:text-slate-200 hover:bg-slate-800 rounded-xl transition">
          <Bell className="w-5 h-5" />
          <span className="absolute top-1.5 right-1.5 w-2 h-2 rounded-full bg-teal-400 animate-ping"></span>
          <span className="absolute top-1.5 right-1.5 w-2 h-2 rounded-full bg-teal-500"></span>
        </button>

        {currentUser && (
          <div className="flex items-center gap-3 pl-3 border-l border-slate-800">
            <img
              src={currentUser.avatar_url || 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=150'}
              alt={currentUser.full_name}
              className="w-9 h-9 rounded-xl object-cover ring-2 ring-teal-500/40"
            />
            <div className="hidden lg:block text-left">
              <div className="text-xs font-bold text-white leading-tight">
                {currentUser.full_name}
              </div>
              <div className="text-[11px] font-semibold text-teal-400">
                {currentUser.role}
              </div>
            </div>
            <button
              onClick={onLogout}
              title="Sign Out"
              className="p-2 text-slate-400 hover:text-red-400 hover:bg-red-500/10 rounded-xl transition"
            >
              <LogOut className="w-4 h-4" />
            </button>
          </div>
        )}
      </div>
    </header>
  );
};
