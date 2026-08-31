import React, { useState } from 'react';
import {
  Lock,
  Search,
  ShieldCheck,
  CheckCircle2,
  Clock,
  UserCheck,
  FileText,
} from 'lucide-react';
import { AuditLog } from '../../types';

export const AuditView: React.FC = () => {
  const [logs] = useState<AuditLog[]>([
    {
      id: 'aud-001',
      event_time: '2026-08-31T14:48:00Z',
      actor_user_id: 'usr-pharm-01',
      actor_name: 'Marcus Vance, PharmD',
      actor_role: 'Pharmacist',
      action_type: 'DISPENSE',
      resource_type: 'PRESCRIPTION',
      resource_id: 'rx-001',
      ip_address: '192.168.1.104',
      details: 'Validated and dispensed 30 tabs Atorvastatin 40mg under Smart FEFO protocol.',
      compliance_tag: 'HIPAA_AUDITABLE',
    },
    {
      id: 'aud-002',
      event_time: '2026-08-31T14:15:00Z',
      actor_user_id: 'usr-doc-01',
      actor_name: 'Dr. Sarah Chen, MD',
      actor_role: 'Doctor',
      action_type: 'CREATE',
      resource_type: 'PRESCRIPTION',
      resource_id: 'rx-001',
      ip_address: '192.168.1.52',
      details: 'Signed electronic prescription with ECDSA hash SIG-ECDSA-SHA256-CHEN-99210.',
      compliance_tag: 'HIPAA_AUDITABLE',
    },
    {
      id: 'aud-003',
      event_time: '2026-08-31T12:30:00Z',
      actor_user_id: 'usr-admin-01',
      actor_name: 'Dr. Alexander Wright, MD',
      actor_role: 'Super Admin',
      action_type: 'UPDATE',
      resource_type: 'SECURITY_POLICY',
      resource_id: 'sec-pol-01',
      ip_address: '10.0.4.1',
      details: 'Enforced mandatory MFA policy across all pharmacy and hospital administrator accounts.',
      compliance_tag: 'SOC2_AUDITABLE',
    },
  ]);

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <div className="flex items-center gap-2">
            <h1 className="text-2xl font-black text-white">Security & HIPAA Audit Trail</h1>
            <span className="px-2.5 py-0.5 rounded-full bg-teal-500/10 text-teal-400 text-xs font-bold border border-teal-500/20">
              Immutable Ledger
            </span>
          </div>
          <p className="text-xs text-slate-400 mt-1">
            Complete audit logging of all patient record views, prescription modifications, dispensing events, and security overrides.
          </p>
        </div>
      </div>

      {/* Audit Log Entries Table */}
      <div className="bg-slate-900 border border-slate-800 rounded-2xl shadow-xl overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead className="bg-slate-800/80 text-slate-400 font-bold uppercase tracking-wider text-[10px]">
              <tr>
                <th className="px-5 py-3.5">Timestamp</th>
                <th className="px-4 py-3.5">Actor & Role</th>
                <th className="px-4 py-3.5">Action Type</th>
                <th className="px-4 py-3.5">Resource</th>
                <th className="px-4 py-3.5">IP Address</th>
                <th className="px-4 py-3.5">Audit Trail Details</th>
                <th className="px-4 py-3.5">Compliance</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800 text-slate-300">
              {logs.map((log) => (
                <tr key={log.id} className="hover:bg-slate-800/40 transition">
                  <td className="px-5 py-3.5 font-mono text-slate-400">
                    {new Date(log.event_time).toLocaleTimeString()}
                    <div className="text-[10px] text-slate-500">
                      {new Date(log.event_time).toLocaleDateString()}
                    </div>
                  </td>
                  <td className="px-4 py-3.5">
                    <div className="font-bold text-white">{log.actor_name}</div>
                    <div className="text-[10px] text-teal-400 font-semibold">{log.actor_role}</div>
                  </td>
                  <td className="px-4 py-3.5 font-mono font-bold">
                    <span className="px-2 py-0.5 rounded bg-slate-800 text-teal-300 border border-slate-700 text-[10px]">
                      {log.action_type}
                    </span>
                  </td>
                  <td className="px-4 py-3.5 font-mono text-xs text-white">
                    {log.resource_type}
                    <div className="text-[10px] text-slate-500">{log.resource_id}</div>
                  </td>
                  <td className="px-4 py-3.5 font-mono text-slate-400">{log.ip_address}</td>
                  <td className="px-4 py-3.5 text-slate-300 max-w-xs truncate">{log.details}</td>
                  <td className="px-4 py-3.5">
                    <span className="px-2 py-0.5 rounded-full text-[10px] font-extrabold bg-emerald-500/20 text-emerald-300 border border-emerald-500/30">
                      {log.compliance_tag}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};
