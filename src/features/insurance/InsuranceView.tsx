import React, { useState } from 'react';
import {
  FileCheck2,
  Search,
  ShieldCheck,
  CheckCircle2,
  Clock,
  AlertCircle,
  FileText,
} from 'lucide-react';
import { InsuranceClaim } from '../../types';

export const InsuranceView: React.FC = () => {
  const [claims, setClaims] = useState<InsuranceClaim[]>([
    {
      id: 'clm-001',
      claim_number: 'CLM-2026-BCBS-88901',
      patient_id: 'pat-001',
      patient_name: 'Eleanor Vance',
      insurance_provider: 'Blue Cross Blue Shield',
      policy_number: 'POL-BCBS-889104',
      group_number: 'GRP-TECH-7701',
      claim_type: 'Outpatient & Pharmacy',
      billed_amount: 295.0,
      deductible_amount: 0.0,
      copay_amount: 35.0,
      approved_amount: 260.0,
      diagnosis_codes: ['I10', 'E11.9', 'E78.0'],
      treatment_summary: 'Comprehensive Cardiology Follow-up and Lipid Bloodwork.',
      status: 'Approved',
      adjudication_notes: 'Tier 1 preferred specialist visit. In-network coverage 100% after copay.',
      submitted_at: '2026-08-28T12:00:00Z',
      settled_at: '2026-08-29T10:30:00Z',
    },
    {
      id: 'clm-002',
      claim_number: 'CLM-2026-AETNA-44912',
      patient_id: 'pat-002',
      patient_name: 'Michael Chang',
      insurance_provider: 'Aetna Health',
      policy_number: 'POL-AETNA-449120',
      group_number: 'GRP-EDU-9921',
      claim_type: 'Telemedicine Consultation',
      billed_amount: 150.0,
      deductible_amount: 0.0,
      copay_amount: 30.0,
      approved_amount: 120.0,
      diagnosis_codes: ['J45.40'],
      treatment_summary: 'Virtual Pulmonology & Allergy Evaluation.',
      status: 'Under Review',
      adjudication_notes: 'Electronic eligibility verified. Awaiting clearinghouse batch settlement.',
      submitted_at: '2026-08-31T10:15:00Z',
    },
  ]);

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <div className="flex items-center gap-2">
            <h1 className="text-2xl font-black text-white">Insurance & Claims Adjudication</h1>
            <span className="px-2.5 py-0.5 rounded-full bg-teal-500/10 text-teal-400 text-xs font-bold border border-teal-500/20">
              Real-Time Payer Clearinghouse
            </span>
          </div>
          <p className="text-xs text-slate-400 mt-1">
            Pre-authorization workflows, electronic claims submission, deductibles, and automated co-pay settlements.
          </p>
        </div>
      </div>

      {/* Claims Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {claims.map((claim) => (
          <div
            key={claim.id}
            className="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-xl space-y-4"
          >
            <div className="flex items-center justify-between pb-3 border-b border-slate-800">
              <div>
                <span className="font-mono text-xs font-bold text-teal-400">
                  {claim.claim_number}
                </span>
                <h3 className="font-black text-base text-white mt-0.5">{claim.patient_name}</h3>
              </div>
              <span
                className={`text-[10px] font-extrabold px-3 py-1 rounded-full ${
                  claim.status === 'Approved'
                    ? 'bg-emerald-500/20 text-emerald-300 border border-emerald-500/30'
                    : 'bg-amber-500/20 text-amber-300 border border-amber-500/30'
                }`}
              >
                {claim.status.toUpperCase()}
              </span>
            </div>

            <div className="grid grid-cols-2 gap-2 text-xs">
              <div className="bg-slate-950/60 p-2.5 rounded-xl border border-slate-800">
                <span className="text-[10px] text-slate-400 block">Payer / Insurer</span>
                <span className="font-bold text-white">{claim.insurance_provider}</span>
              </div>
              <div className="bg-slate-950/60 p-2.5 rounded-xl border border-slate-800">
                <span className="text-[10px] text-slate-400 block">Policy #</span>
                <span className="font-mono font-bold text-teal-300">{claim.policy_number}</span>
              </div>
            </div>

            <div className="bg-slate-800/60 border border-slate-700/80 rounded-xl p-3 text-xs space-y-1">
              <div className="flex justify-between text-slate-400">
                <span>Total Billed Amount:</span>
                <span className="font-mono font-bold text-white">
                  ${claim.billed_amount.toFixed(2)}
                </span>
              </div>
              <div className="flex justify-between text-slate-400">
                <span>Patient Co-Pay:</span>
                <span className="font-mono text-amber-300">${claim.copay_amount.toFixed(2)}</span>
              </div>
              <div className="flex justify-between text-teal-400 font-bold pt-1 border-t border-slate-700">
                <span>Approved Reimbursement:</span>
                <span className="font-mono">${claim.approved_amount.toFixed(2)}</span>
              </div>
            </div>

            <p className="text-xs text-slate-400 italic">"{claim.adjudication_notes}"</p>
          </div>
        ))}
      </div>
    </div>
  );
};
