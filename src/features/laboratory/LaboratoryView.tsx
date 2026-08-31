import React, { useState } from 'react';
import {
  FlaskConical,
  Barcode,
  Search,
  CheckCircle2,
  AlertTriangle,
  FileCheck2,
  Clock,
  User,
} from 'lucide-react';
import { LabOrder } from '../../types';

export const LaboratoryView: React.FC = () => {
  const [labOrders, setLabOrders] = useState<LabOrder[]>([
    {
      id: 'lab-001',
      order_number: 'LAB-2026-009101',
      patient_id: 'pat-001',
      patient_name: 'Eleanor Vance',
      doctor_id: 'doc-001',
      doctor_name: 'Dr. Sarah Chen, MD',
      order_type: 'Routine',
      sample_type: 'Venous Whole Blood & Serum',
      sample_barcode: 'BAR-LAB-99201',
      clinical_indication: 'Follow-up monitoring for statin therapy and type 2 diabetes.',
      status: 'Verified',
      ordered_at: '2026-08-27T08:30:00Z',
      reported_at: '2026-08-28T14:15:00Z',
      technician_name: 'David Kim, MLS',
      tests: [
        {
          test_code: 'LIPID-LDL',
          test_name: 'Lipid Panel',
          parameter_name: 'LDL Cholesterol',
          measured_value: '94',
          unit: 'mg/dL',
          reference_range_min: 0,
          reference_range_max: 100,
          is_abnormal: false,
          is_critical: false,
          flag: 'Normal',
        },
        {
          test_code: 'GLUC-A1C',
          test_name: 'Glycated Hemoglobin',
          parameter_name: 'Hemoglobin A1c',
          measured_value: '6.8',
          unit: '%',
          reference_range_min: 4.0,
          reference_range_max: 5.6,
          is_abnormal: true,
          is_critical: false,
          flag: 'High (Diabetic)',
        },
        {
          test_code: 'RENAL-GFR',
          test_name: 'Comprehensive Metabolic Panel',
          parameter_name: 'Estimated GFR (eGFR)',
          measured_value: '92',
          unit: 'mL/min/1.73m²',
          reference_range_min: 60,
          reference_range_max: 120,
          is_abnormal: false,
          is_critical: false,
          flag: 'Normal',
        },
      ],
    },
  ]);

  const [selectedOrder, setSelectedOrder] = useState<LabOrder>(labOrders[0]);

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <div className="flex items-center gap-2">
            <h1 className="text-2xl font-black text-white">Laboratory Diagnostics Workbench</h1>
            <span className="px-2.5 py-0.5 rounded-full bg-teal-500/10 text-teal-400 text-xs font-bold border border-teal-500/20">
              Pathology & Molecular
            </span>
          </div>
          <p className="text-xs text-slate-400 mt-1">
            Sample tracking, automated analyzer integration, reference range checks, and critical alerting.
          </p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Lab Orders Queue */}
        <div className="bg-slate-900 border border-slate-800 rounded-2xl p-5 shadow-lg space-y-4">
          <div className="flex items-center justify-between pb-2 border-b border-slate-800">
            <h3 className="font-extrabold text-sm text-white">Active Lab Orders</h3>
            <span className="text-xs font-mono text-slate-400">{labOrders.length} orders</span>
          </div>

          <div className="space-y-3">
            {labOrders.map((order) => (
              <div
                key={order.id}
                onClick={() => setSelectedOrder(order)}
                className={`p-4 rounded-xl border transition cursor-pointer ${
                  selectedOrder.id === order.id
                    ? 'bg-slate-800 border-teal-500/50 shadow-md'
                    : 'bg-slate-900/80 border-slate-800 hover:border-slate-700'
                }`}
              >
                <div className="flex items-center justify-between">
                  <span className="font-mono text-xs font-bold text-teal-400">
                    {order.order_number}
                  </span>
                  <span className="text-[10px] font-extrabold px-2 py-0.5 rounded-full bg-emerald-500/20 text-emerald-300 border border-emerald-500/30">
                    {order.status}
                  </span>
                </div>
                <div className="font-bold text-sm text-white mt-1">{order.patient_name}</div>
                <div className="text-xs text-slate-400 mt-0.5">
                  Ordered by {order.doctor_name} • Sample: {order.sample_type}
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Test Results & Verification Panel */}
        <div className="lg:col-span-2 bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-xl space-y-5">
          <div className="flex items-start justify-between pb-4 border-b border-slate-800">
            <div>
              <div className="flex items-center gap-2">
                <h2 className="text-lg font-black text-white">{selectedOrder.patient_name}</h2>
                <span className="font-mono text-xs text-teal-400 bg-slate-950 px-2 py-0.5 rounded border border-slate-700">
                  {selectedOrder.sample_barcode}
                </span>
              </div>
              <div className="text-xs text-slate-400 mt-1">
                Clinical Indication: {selectedOrder.clinical_indication}
              </div>
            </div>
            <div className="text-right">
              <div className="text-xs font-semibold text-slate-300">
                Tech: {selectedOrder.technician_name}
              </div>
              <div className="text-[10px] text-slate-500">
                Reported: {selectedOrder.reported_at}
              </div>
            </div>
          </div>

          {/* Test Parameters Table */}
          <div className="border border-slate-800 rounded-xl overflow-hidden">
            <table className="w-full text-left text-xs">
              <thead className="bg-slate-800/80 text-slate-400 font-bold uppercase tracking-wider text-[10px]">
                <tr>
                  <th className="px-4 py-3">Test & Parameter</th>
                  <th className="px-4 py-3">Measured Result</th>
                  <th className="px-4 py-3">Unit</th>
                  <th className="px-4 py-3">Reference Interval</th>
                  <th className="px-4 py-3">Flag</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800 text-slate-300">
                {selectedOrder.tests.map((test, idx) => (
                  <tr key={idx} className="hover:bg-slate-800/40 transition">
                    <td className="px-4 py-3">
                      <div className="font-bold text-white">{test.parameter_name}</div>
                      <div className="text-[10px] text-slate-400">{test.test_name}</div>
                    </td>
                    <td className="px-4 py-3 font-mono font-bold text-sm text-white">
                      {test.measured_value}
                    </td>
                    <td className="px-4 py-3 font-mono text-slate-400">{test.unit}</td>
                    <td className="px-4 py-3 font-mono text-slate-400">
                      {test.reference_range_min} - {test.reference_range_max}
                    </td>
                    <td className="px-4 py-3">
                      {test.is_abnormal ? (
                        <span className="px-2 py-0.5 rounded-full text-[10px] font-extrabold bg-amber-500/20 text-amber-300 border border-amber-500/30">
                          {test.flag}
                        </span>
                      ) : (
                        <span className="px-2 py-0.5 rounded-full text-[10px] font-extrabold bg-emerald-500/20 text-emerald-300 border border-emerald-500/30">
                          Normal
                        </span>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  );
};
