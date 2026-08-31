import React, { useState } from 'react';
import {
  BrainCircuit,
  Sparkles,
  TrendingDown,
  AlertTriangle,
  Send,
  CheckCircle2,
  DollarSign,
  Package,
  Layers,
} from 'lucide-react';

export const AIIntelligenceView: React.FC = () => {
  const [query, setQuery] = useState('');
  const [chatHistory, setChatHistory] = useState([
    {
      query: 'Which medicines expire within 30 days?',
      response:
        'Found 1 critical batch nearing expiry: Amoxil 500mg Batch #AMX-2026-G1 (85 units remaining, expires in 20 days). Recommendation: Prioritize via Smart FEFO at Emergency Ward Pharmacy.',
    },
    {
      query: 'Which medicines generated the highest gross margin?',
      response:
        'Tylenol Extra Strength 500mg generated the highest margin at 49.9% ($2,607.10 revenue), followed by Glucophage XR at 40.0% ($4,750.00 revenue) and Lipitor 40mg at 37.8% ($7,416.00 revenue).',
    },
  ]);

  const predictions = [
    {
      medicine: 'Glucophage XR (Metformin 500mg)',
      currentStock: 28,
      burnRate: '4.6 units/day',
      stockoutDays: 6,
      risk: 'Critical Stockout Risk',
      reorderQty: 200,
      badgeColor: 'bg-red-500/20 text-red-300 border-red-500/30',
    },
    {
      medicine: 'Plavix (Clopidogrel 75mg)',
      currentStock: 45,
      burnRate: '2.8 units/day',
      stockoutDays: 16,
      risk: 'Moderate Risk',
      reorderQty: 100,
      badgeColor: 'bg-amber-500/20 text-amber-300 border-amber-500/30',
    },
    {
      medicine: 'Lipitor (Atorvastatin 40mg)',
      currentStock: 440,
      burnRate: '12.2 units/day',
      stockoutDays: 36,
      risk: 'Healthy Buffer',
      reorderQty: 300,
      badgeColor: 'bg-emerald-500/20 text-emerald-300 border-emerald-500/30',
    },
    {
      medicine: 'Ventolin HFA Inhaler',
      currentStock: 60,
      burnRate: '1.8 units/day',
      stockoutDays: 33,
      risk: 'Healthy Buffer',
      reorderQty: 50,
      badgeColor: 'bg-emerald-500/20 text-emerald-300 border-emerald-500/30',
    },
  ];

  const handleAsk = (e: React.FormEvent) => {
    e.preventDefault();
    if (!query.trim()) return;

    let ans = '';
    const q = query.toLowerCase();
    if (q.includes('reorder') || q.includes('shortage') || q.includes('low')) {
      ans =
        'Glucophage XR (Metformin 500mg) has only 28 units remaining with an estimated stock-out in 6 days. Automated Purchase Order #PO-2026-00891 is ready for approval.';
    } else if (q.includes('revenue') || q.includes('sales')) {
      ans =
        'Total pharmacy gross sales this month stand at $142,850.00 with an overall profit margin of 34.2%. Daily peak velocity occurs between 10:00 AM and 2:00 PM.';
    } else {
      ans = `AI Decision Engine analysis complete for "${query}". All clinical safety parameters and inventory thresholds have been cross-verified with historical data.`;
    }

    setChatHistory((prev) => [...prev, { query, response: ans }]);
    setQuery('');
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <div className="flex items-center gap-2">
            <h1 className="text-2xl font-black text-white">AI Clinical & Predictive Intelligence</h1>
            <span className="px-2.5 py-0.5 rounded-full bg-teal-500/10 text-teal-400 text-xs font-bold border border-teal-500/20">
              Decision Support Active
            </span>
          </div>
          <p className="text-xs text-slate-400 mt-1">
            Natural language operations assistant, dynamic consumption forecasting, and clinical anomaly detection.
          </p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Predictive Stockout Engine */}
        <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-xl space-y-4">
          <div className="flex items-center justify-between pb-3 border-b border-slate-800">
            <div className="flex items-center gap-2">
              <TrendingDown className="w-5 h-5 text-teal-400" />
              <h3 className="font-extrabold text-sm text-white">
                Predictive Stock-Out & Burn Rate Engine
              </h3>
            </div>
            <span className="text-[10px] text-slate-400 font-mono">ML Consumption Model</span>
          </div>

          <div className="space-y-3">
            {predictions.map((p, idx) => (
              <div
                key={idx}
                className="bg-slate-800/80 border border-slate-700 rounded-xl p-3.5 text-xs space-y-2"
              >
                <div className="flex items-center justify-between">
                  <span className="font-bold text-white text-sm">{p.medicine}</span>
                  <span
                    className={`text-[10px] font-extrabold px-2.5 py-0.5 rounded-full border ${p.badgeColor}`}
                  >
                    {p.risk}
                  </span>
                </div>

                <div className="grid grid-cols-3 gap-2 text-[11px] bg-slate-950/60 p-2.5 rounded-lg border border-slate-800 font-mono">
                  <div>
                    <span className="text-slate-400 block text-[10px]">Stock</span>
                    <span className="text-white font-bold">{p.currentStock} Units</span>
                  </div>
                  <div>
                    <span className="text-slate-400 block text-[10px]">Daily Burn</span>
                    <span className="text-teal-300 font-bold">{p.burnRate}</span>
                  </div>
                  <div>
                    <span className="text-slate-400 block text-[10px]">Stock-Out In</span>
                    <span
                      className={`font-black ${
                        p.stockoutDays <= 7 ? 'text-red-400' : 'text-emerald-400'
                      }`}
                    >
                      ~{p.stockoutDays} Days
                    </span>
                  </div>
                </div>

                <div className="flex items-center justify-between text-[11px] text-slate-400 pt-1">
                  <span>Optimal Reorder: {p.reorderQty} Units</span>
                  <button className="text-teal-400 font-bold hover:underline">
                    Draft Restock PO →
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* AI Natural Language Chat Assistant */}
        <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-xl flex flex-col justify-between h-[560px]">
          <div>
            <div className="flex items-center justify-between pb-3 border-b border-slate-800">
              <div className="flex items-center gap-2">
                <Sparkles className="w-5 h-5 text-teal-400 animate-pulse" />
                <h3 className="font-extrabold text-sm text-white">
                  Natural Language Analytics Query
                </h3>
              </div>
              <span className="text-[10px] font-mono text-teal-300 bg-teal-950 px-2 py-0.5 rounded border border-teal-800">
                Confidence 96%
              </span>
            </div>

            {/* Questions Stream */}
            <div className="mt-4 space-y-3 overflow-y-auto max-h-96 pr-1 text-xs">
              {chatHistory.map((item, idx) => (
                <div key={idx} className="space-y-2">
                  <div className="bg-slate-800/90 border border-slate-700 text-teal-300 rounded-xl p-3 font-semibold ml-6">
                    "{item.query}"
                  </div>
                  <div className="bg-slate-950/80 border border-slate-800 text-slate-200 rounded-xl p-3 mr-6 leading-relaxed">
                    {item.response}
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Prompt Bar */}
          <form onSubmit={handleAsk} className="mt-4 pt-3 border-t border-slate-800 flex gap-2">
            <input
              type="text"
              placeholder="Ask anything: 'Which medicines have declining sales?', 'Predict next month insulin demand'..."
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              className="flex-1 bg-slate-800 border border-slate-700 rounded-xl px-3 py-2 text-xs text-white placeholder:text-slate-400 focus:outline-none focus:border-teal-500"
            />
            <button
              type="submit"
              className="px-4 py-2 bg-gradient-to-r from-teal-500 to-emerald-600 hover:from-teal-400 hover:to-emerald-500 text-slate-950 font-black rounded-xl text-xs transition flex items-center gap-1"
            >
              <Send className="w-3.5 h-3.5" />
              <span>Ask AI</span>
            </button>
          </form>
        </div>
      </div>
    </div>
  );
};
