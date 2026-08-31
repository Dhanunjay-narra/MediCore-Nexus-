import React, { useState } from 'react';
import {
  CreditCard,
  Search,
  DollarSign,
  Receipt,
  FileCheck2,
  CheckCircle2,
  Clock,
  ArrowUpRight,
} from 'lucide-react';
import { Invoice } from '../../types';

export const BillingView: React.FC = () => {
  const [invoices, setInvoices] = useState<Invoice[]>([
    {
      id: 'inv-001',
      invoice_number: 'INV-2026-003891',
      patient_id: 'pat-001',
      patient_name: 'Eleanor Vance',
      hospital_id: 'hosp-001',
      insurance_claim_id: 'clm-001',
      insurance_coverage_amount: 260.0,
      patient_copay_amount: 35.0,
      subtotal: 295.0,
      total_tax: 0.0,
      total_discount: 0.0,
      gross_total: 295.0,
      balance_due: 0.0,
      payment_status: 'Paid',
      created_at: '2026-08-28T12:00:00Z',
      paid_at: '2026-08-28T12:15:00Z',
      items: [
        {
          service_type: 'Consultation',
          description: 'Comprehensive Cardiac Consultation with Dr. Sarah Chen',
          quantity: 1,
          unit_price: 220.0,
          discount: 0.0,
          tax: 0.0,
          net_total: 220.0,
        },
        {
          service_type: 'Laboratory',
          description: 'Lipid Panel & Metabolic Test Panel',
          quantity: 1,
          unit_price: 75.0,
          discount: 0.0,
          tax: 0.0,
          net_total: 75.0,
        },
      ],
    },
    {
      id: 'inv-002',
      invoice_number: 'INV-2026-003892',
      patient_id: 'pat-002',
      patient_name: 'Michael Chang',
      hospital_id: 'hosp-001',
      insurance_coverage_amount: 120.0,
      patient_copay_amount: 30.0,
      subtotal: 150.0,
      total_tax: 0.0,
      total_discount: 0.0,
      gross_total: 150.0,
      balance_due: 30.0,
      payment_status: 'Pending',
      created_at: '2026-08-31T10:00:00Z',
      items: [
        {
          service_type: 'Telemedicine',
          description: 'Virtual Pulmonology & Allergy Consultation',
          quantity: 1,
          unit_price: 150.0,
          discount: 0.0,
          tax: 0.0,
          net_total: 150.0,
        },
      ],
    },
  ]);

  const [selectedInvoice, setSelectedInvoice] = useState<Invoice>(invoices[0]);

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <div className="flex items-center gap-2">
            <h1 className="text-2xl font-black text-white">Billing & Revenue Ledger</h1>
            <span className="px-2.5 py-0.5 rounded-full bg-teal-500/10 text-teal-400 text-xs font-bold border border-teal-500/20">
              Automated Co-Pay
            </span>
          </div>
          <p className="text-xs text-slate-400 mt-1">
            Consolidated invoicing across outpatient consultations, inpatient stays, pharmacy dispensing, and lab services.
          </p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Invoices List */}
        <div className="bg-slate-900 border border-slate-800 rounded-2xl p-5 shadow-lg space-y-3">
          <div className="flex items-center justify-between pb-2 border-b border-slate-800">
            <h3 className="font-extrabold text-sm text-white">Recent Invoices</h3>
            <span className="text-xs font-mono text-slate-400">{invoices.length} entries</span>
          </div>

          <div className="space-y-2">
            {invoices.map((inv) => (
              <div
                key={inv.id}
                onClick={() => setSelectedInvoice(inv)}
                className={`p-3.5 rounded-xl border transition cursor-pointer ${
                  selectedInvoice.id === inv.id
                    ? 'bg-slate-800 border-teal-500/50 shadow-md'
                    : 'bg-slate-900/80 border-slate-800 hover:border-slate-700'
                }`}
              >
                <div className="flex items-center justify-between">
                  <span className="font-mono text-xs font-bold text-teal-400">
                    {inv.invoice_number}
                  </span>
                  <span
                    className={`text-[10px] font-extrabold px-2 py-0.5 rounded-full ${
                      inv.payment_status === 'Paid'
                        ? 'bg-emerald-500/20 text-emerald-300 border border-emerald-500/30'
                        : 'bg-amber-500/20 text-amber-300 border border-amber-500/30'
                    }`}
                  >
                    {inv.payment_status}
                  </span>
                </div>
                <div className="font-bold text-sm text-white mt-1">{inv.patient_name}</div>
                <div className="flex justify-between items-center text-xs text-slate-400 mt-1">
                  <span>Total: ${inv.gross_total.toFixed(2)}</span>
                  <span className="font-bold text-teal-300">
                    Balance: ${inv.balance_due.toFixed(2)}
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Invoice Itemized Details */}
        <div className="lg:col-span-2 bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-xl space-y-5">
          <div className="flex items-start justify-between pb-4 border-b border-slate-800">
            <div>
              <div className="font-mono text-xs font-bold text-teal-400">
                {selectedInvoice.invoice_number}
              </div>
              <h2 className="text-xl font-black text-white mt-0.5">
                {selectedInvoice.patient_name}
              </h2>
              <div className="text-xs text-slate-400 mt-0.5">
                Billed on {new Date(selectedInvoice.created_at).toLocaleString()}
              </div>
            </div>

            <div className="text-right">
              <div className="text-2xl font-black text-white font-mono">
                ${selectedInvoice.gross_total.toFixed(2)}
              </div>
              <div className="text-xs text-teal-400 font-semibold">
                Insurance Covered: ${selectedInvoice.insurance_coverage_amount.toFixed(2)}
              </div>
            </div>
          </div>

          {/* Line Items Table */}
          <div className="border border-slate-800 rounded-xl overflow-hidden">
            <table className="w-full text-left text-xs">
              <thead className="bg-slate-800/80 text-slate-400 font-bold uppercase tracking-wider text-[10px]">
                <tr>
                  <th className="px-4 py-3">Service / Description</th>
                  <th className="px-4 py-3">Type</th>
                  <th className="px-4 py-3 font-mono">Qty</th>
                  <th className="px-4 py-3 font-mono">Unit Price</th>
                  <th className="px-4 py-3 font-mono text-right">Net Amount</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800 text-slate-300">
                {selectedInvoice.items.map((item, idx) => (
                  <tr key={idx}>
                    <td className="px-4 py-3 font-bold text-white">{item.description}</td>
                    <td className="px-4 py-3">
                      <span className="px-2 py-0.5 rounded bg-slate-800 text-slate-400 text-[10px]">
                        {item.service_type}
                      </span>
                    </td>
                    <td className="px-4 py-3 font-mono">{item.quantity}</td>
                    <td className="px-4 py-3 font-mono">${item.unit_price.toFixed(2)}</td>
                    <td className="px-4 py-3 font-mono font-bold text-teal-300 text-right">
                      ${item.net_total.toFixed(2)}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          <div className="flex justify-between items-center pt-2">
            <span className="text-xs text-slate-400">
              Payment Status:{' '}
              <strong className="text-teal-400">{selectedInvoice.payment_status}</strong>
            </span>
            <button className="px-4 py-2 bg-gradient-to-r from-teal-500 to-emerald-600 hover:from-teal-400 hover:to-emerald-500 text-slate-950 font-black rounded-xl text-xs shadow-md transition">
              Process Payment / Settle Balance
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};
