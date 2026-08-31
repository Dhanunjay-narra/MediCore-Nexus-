import React from 'react';
import {
  LayoutDashboard,
  Users,
  Stethoscope,
  Calendar,
  FileText,
  Pill,
  Package,
  Layers,
  Truck,
  ShoppingCart,
  ShieldAlert,
  FlaskConical,
  CreditCard,
  FileCheck2,
  Video,
  Bell,
  BarChart3,
  BrainCircuit,
  Building,
  Lock,
  Archive,
  UserCheck,
} from 'lucide-react';
import { UserRole } from '../../types';

interface SidebarProps {
  activeTab: string;
  setActiveTab: (tab: string) => void;
  userRole?: UserRole;
}

export const Sidebar: React.FC<SidebarProps> = ({
  activeTab,
  setActiveTab,
  userRole = 'Super Admin',
}) => {
  const navSections = [
    {
      title: 'CORE PLATFORM',
      items: [
        { id: 'dashboard', label: 'Command Cockpit', icon: LayoutDashboard },
        { id: 'patients', label: 'Patient Master (MPI)', icon: Users },
        { id: 'clinical', label: 'Doctor Station & EMR', icon: Stethoscope },
        { id: 'appointments', label: 'Appointments & Queue', icon: Calendar },
      ],
    },
    {
      title: 'PHARMACY & COMMERCE',
      items: [
        { id: 'pharmacy_center', label: 'Pharmacy Command Center', icon: ActivityIcon },
        { id: 'pos', label: 'Point-of-Sale (POS)', icon: ShoppingCart },
        { id: 'inventory', label: 'Inventory & Smart FEFO', icon: Layers },
        { id: 'medicines', label: 'Medicine Catalog Master', icon: Pill },
        { id: 'procurement', label: 'Suppliers & Procurement', icon: Truck },
      ],
    },
    {
      title: 'CLINICAL ENGINES & DIAGNOSTICS',
      items: [
        { id: 'drug_safety', label: 'Drug Safety & Risk Radar', icon: ShieldAlert },
        { id: 'laboratory', label: 'Laboratory Diagnostics', icon: FlaskConical },
        { id: 'telemedicine', label: 'Telemedicine Suite', icon: Video },
      ],
    },
    {
      title: 'FINANCE & REVENUE',
      items: [
        { id: 'billing', label: 'Billing & Invoices', icon: CreditCard },
        { id: 'insurance', label: 'Insurance & Claims', icon: FileCheck2 },
      ],
    },
    {
      title: 'INTELLIGENCE & OPERATIONS',
      items: [
        { id: 'intelligence', label: 'AI Decision & Predictions', icon: BrainCircuit },
        { id: 'analytics', label: 'Healthcare & Sales BI', icon: BarChart3 },
        { id: 'staff', label: 'Staff Rosters & Shifts', icon: UserCheck },
        { id: 'organization', label: 'Hospitals & Beds', icon: Building },
        { id: 'audit', label: 'Audit & Compliance Logs', icon: Lock },
      ],
    },
  ];

  return (
    <aside className="w-64 bg-slate-900 border-r border-slate-800 flex flex-col h-[calc(100vh-4rem)] sticky top-16 select-none">
      <div className="flex-1 overflow-y-auto py-4 px-3 space-y-6">
        {navSections.map((section, idx) => (
          <div key={idx} className="space-y-1">
            <div className="px-3 text-[10px] font-extrabold tracking-wider text-slate-500 uppercase">
              {section.title}
            </div>
            <div className="space-y-0.5 mt-1">
              {section.items.map((item) => {
                const Icon = item.icon;
                const isActive = activeTab === item.id;
                return (
                  <button
                    key={item.id}
                    onClick={() => setActiveTab(item.id)}
                    className={`w-full flex items-center gap-3 px-3 py-2 rounded-xl text-xs font-semibold transition group text-left ${
                      isActive
                        ? 'bg-gradient-to-r from-teal-500/20 to-emerald-500/10 text-teal-400 border border-teal-500/30'
                        : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/60'
                    }`}
                  >
                    <Icon
                      className={`w-4 h-4 transition ${
                        isActive ? 'text-teal-400' : 'text-slate-500 group-hover:text-slate-300'
                      }`}
                    />
                    <span className="truncate">{item.label}</span>
                  </button>
                );
              })}
            </div>
          </div>
        ))}
      </div>

      {/* Role Indicator Footer */}
      <div className="p-3 border-t border-slate-800 bg-slate-950/40">
        <div className="flex items-center justify-between text-[11px] text-slate-400">
          <span>Active Role</span>
          <span className="font-bold text-teal-400">{userRole}</span>
        </div>
      </div>
    </aside>
  );
};

function ActivityIcon(props: React.SVGProps<SVGSVGElement>) {
  return (
    <svg
      {...props}
      xmlns="http://www.w3.org/2000/svg"
      width="24"
      height="24"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
    >
      <path d="M22 12h-4l-3 9L9 3l-3 9H2" />
    </svg>
  );
}
