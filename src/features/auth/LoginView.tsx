import React, { useState } from 'react';
import {
  ShieldCheck,
  Lock,
  Mail,
  UserCheck,
  Stethoscope,
  Pill,
  HeartPulse,
  FlaskConical,
  User,
  Building,
  Sparkles,
  ArrowRight,
} from 'lucide-react';
import { DEMO_USERS } from '../../services/api';
import { User as UserType } from '../../types';

interface LoginViewProps {
  onLoginSuccess: (user: UserType) => void;
}

export const LoginView: React.FC<LoginViewProps> = ({ onLoginSuccess }) => {
  const [email, setEmail] = useState('admin@medicorenexus.io');
  const [password, setPassword] = useState('Admin@12345');
  const [isLoading, setIsLoading] = useState(false);

  const handleManualLogin = (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setTimeout(() => {
      // Find or default to superadmin
      const matched = Object.values(DEMO_USERS).find(
        (d) => d.user.email.toLowerCase() === email.toLowerCase()
      );
      if (matched) {
        onLoginSuccess(matched.user);
      } else {
        onLoginSuccess(DEMO_USERS.superadmin.user);
      }
      setIsLoading(false);
    }, 400);
  };

  const handleOneClickPersona = (personaKey: string) => {
    const persona = DEMO_USERS[personaKey];
    if (persona) {
      setEmail(persona.user.email);
      setPassword(persona.password_hint);
      onLoginSuccess(persona.user);
    }
  };

  const personas = [
    {
      key: 'superadmin',
      role: 'Super Admin',
      name: 'Dr. Alexander Wright',
      icon: ShieldCheck,
      color: 'from-purple-500 to-indigo-600',
      badge: 'Full Access',
      desc: 'System Configuration & Global Oversight',
    },
    {
      key: 'doctor',
      role: 'Doctor / Physician',
      name: 'Dr. Sarah Chen, MD',
      icon: Stethoscope,
      color: 'from-teal-500 to-emerald-600',
      badge: 'Cardiology',
      desc: 'EMR, SOAP Notes, e-Prescriptions & Risk Radar',
    },
    {
      key: 'pharmacist',
      role: 'Pharmacist',
      name: 'Marcus Vance, PharmD',
      icon: Pill,
      color: 'from-amber-500 to-orange-600',
      badge: 'Chief Rx',
      desc: 'Command Center, Smart FEFO & Dispensing',
    },
    {
      key: 'nurse',
      role: 'Nurse',
      name: 'Elena Rodriguez, RN',
      icon: HeartPulse,
      color: 'from-rose-500 to-pink-600',
      badge: 'ER Triage',
      desc: 'Vitals, Triage, Patient Bed Management',
    },
    {
      key: 'labtech',
      role: 'Lab Technician',
      name: 'David Kim, MLS',
      icon: FlaskConical,
      color: 'from-cyan-500 to-blue-600',
      badge: 'Pathology',
      desc: 'Sample Barcoding, Test Results & Critical Alerts',
    },
    {
      key: 'patient',
      role: 'Patient Portal',
      name: 'Eleanor Vance (Patient)',
      icon: User,
      color: 'from-emerald-500 to-teal-600',
      badge: 'Portal',
      desc: 'Medical Timeline, Prescriptions & Records',
    },
  ];

  return (
    <div className="min-h-screen bg-slate-950 flex flex-col justify-center py-12 px-4 sm:px-6 lg:px-8 relative overflow-hidden">
      {/* Background glow effects */}
      <div className="absolute top-1/4 left-1/2 -translate-x-1/2 w-96 h-96 bg-teal-500/10 rounded-full blur-3xl pointer-events-none"></div>
      <div className="absolute bottom-10 right-10 w-80 h-80 bg-indigo-500/10 rounded-full blur-3xl pointer-events-none"></div>

      <div className="sm:mx-auto sm:w-full sm:max-w-md text-center z-10">
        <div className="mx-auto w-16 h-16 rounded-2xl bg-gradient-to-tr from-teal-500 via-emerald-500 to-cyan-400 flex items-center justify-center shadow-2xl shadow-teal-500/30 text-slate-950 font-black text-3xl mb-4">
          M
        </div>
        <h2 className="text-3xl font-black text-white tracking-tight">
          MediCore <span className="text-teal-400">Nexus</span>
        </h2>
        <p className="mt-1.5 text-xs text-slate-400 font-medium">
          Integrated Pharmacy, Hospital & Patient Care Platform
        </p>
      </div>

      {/* 1-Click Persona Quick Launcher Bar */}
      <div className="mt-8 max-w-5xl mx-auto w-full z-10">
        <div className="bg-slate-900/90 border border-teal-500/30 rounded-2xl p-6 shadow-2xl backdrop-blur">
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center gap-2">
              <Sparkles className="w-5 h-5 text-teal-400" />
              <h3 className="font-extrabold text-sm text-white uppercase tracking-wider">
                1-Click Instant Persona Sign-In
              </h3>
            </div>
            <span className="text-[11px] text-teal-300 bg-teal-950/80 px-3 py-1 rounded-full border border-teal-800">
              Zero typing required — Click any card to launch immediately
            </span>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-6 gap-3">
            {personas.map((p) => {
              const Icon = p.icon;
              return (
                <button
                  key={p.key}
                  onClick={() => handleOneClickPersona(p.key)}
                  className="bg-slate-800/80 hover:bg-slate-700/80 border border-slate-700 hover:border-teal-500/60 rounded-xl p-3.5 text-left transition flex flex-col justify-between group hover:scale-[1.02] shadow-sm hover:shadow-teal-500/10"
                >
                  <div>
                    <div className="flex items-center justify-between mb-2">
                      <div
                        className={`w-8 h-8 rounded-lg bg-gradient-to-br ${p.color} flex items-center justify-center text-white shadow`}
                      >
                        <Icon className="w-4 h-4" />
                      </div>
                      <span className="text-[9px] font-extrabold px-1.5 py-0.5 rounded bg-slate-900/80 text-teal-300 border border-slate-700">
                        {p.badge}
                      </span>
                    </div>
                    <div className="font-bold text-xs text-white group-hover:text-teal-300 transition">
                      {p.role}
                    </div>
                    <div className="text-[11px] text-slate-300 mt-0.5 truncate">
                      {p.name}
                    </div>
                  </div>
                  <div className="mt-3 pt-2 border-t border-slate-700/60 flex items-center justify-between text-[10px] font-bold text-teal-400 group-hover:translate-x-0.5 transition">
                    <span>Launch</span>
                    <ArrowRight className="w-3 h-3" />
                  </div>
                </button>
              );
            })}
          </div>
        </div>

        {/* Standard Credentials Form */}
        <div className="mt-6 max-w-md mx-auto bg-slate-900/70 border border-slate-800 rounded-2xl p-6 backdrop-blur">
          <form onSubmit={handleManualLogin} className="space-y-4">
            <div>
              <label className="block text-xs font-semibold text-slate-300 mb-1">
                Email Address or Username
              </label>
              <div className="relative">
                <Mail className="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 text-slate-500" />
                <input
                  type="text"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  className="w-full bg-slate-800 border border-slate-700 rounded-xl pl-9 pr-3 py-2 text-xs text-white focus:outline-none focus:border-teal-500"
                  required
                />
              </div>
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-300 mb-1">
                Password
              </label>
              <div className="relative">
                <Lock className="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 text-slate-500" />
                <input
                  type="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  className="w-full bg-slate-800 border border-slate-700 rounded-xl pl-9 pr-3 py-2 text-xs text-white focus:outline-none focus:border-teal-500"
                  required
                />
              </div>
            </div>

            <button
              type="submit"
              disabled={isLoading}
              className="w-full py-2.5 px-4 bg-gradient-to-r from-teal-500 to-emerald-600 hover:from-teal-400 hover:to-emerald-500 text-slate-950 font-extrabold rounded-xl text-xs shadow-lg shadow-teal-500/20 transition disabled:opacity-50"
            >
              {isLoading ? 'Signing In...' : 'Sign In to MediCore Nexus'}
            </button>
          </form>
        </div>
      </div>
    </div>
  );
};
