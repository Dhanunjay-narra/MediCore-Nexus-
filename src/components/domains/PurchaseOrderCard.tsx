import React from 'react';
import { Activity, ShieldCheck, Clock, FileText, CheckCircle2, ChevronRight } from 'lucide-react';

export interface PurchaseOrderCardProps {
  id: string;
  name: string;
  code?: string;
  status: string;
  description?: string;
  timestamp?: string;
  onActionClick?: (id: string) => void;
}

export const PurchaseOrderCard: React.FC<PurchaseOrderCardProps> = ({
  id,
  name,
  code,
  status,
  description,
  timestamp,
  onActionClick,
}) => {
  const isOptimal = status === 'Active' || status === 'Completed' || status === 'Verified' || status === 'Paid';

  return (
    <div className="bg-slate-900/90 border border-slate-800 hover:border-teal-500/40 rounded-2xl p-5 shadow-lg backdrop-blur transition group space-y-3">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2.5">
          <div className="w-8 h-8 rounded-xl bg-teal-500/10 text-teal-400 flex items-center justify-center font-black text-xs border border-teal-500/20">
            PO
          </div>
          <div>
            <h4 className="font-extrabold text-sm text-white group-hover:text-teal-300 transition leading-snug">
              {name}
            </h4>
            {code && <span className="font-mono text-[10px] text-slate-400">{code}</span>}
          </div>
        </div>

        <span
          className={`px-2.5 py-0.5 rounded-full text-[10px] font-extrabold border ${
            isOptimal
              ? 'bg-emerald-500/10 text-emerald-300 border-emerald-500/30'
              : 'bg-amber-500/10 text-amber-300 border-amber-500/30'
          }`}
        >
          {status}
        </span>
      </div>

      {description && (
        <p className="text-xs text-slate-400 line-clamp-2 leading-relaxed">
          {description}
        </p>
      )}

      <div className="flex items-center justify-between pt-2 border-t border-slate-800/80 text-[11px] text-slate-500">
        <span className="font-mono">{timestamp || new Date().toLocaleDateString()}</span>
        <button
          onClick={() => onActionClick && onActionClick(id)}
          className="text-teal-400 font-bold hover:underline flex items-center gap-1 group-hover:translate-x-0.5 transition"
        >
          <span>View Details</span>
          <ChevronRight className="w-3.5 h-3.5" />
        </button>
      </div>
    </div>
  );
};
