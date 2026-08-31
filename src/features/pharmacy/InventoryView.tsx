import React, { useState } from 'react';
import {
  Layers,
  Search,
  AlertTriangle,
  Package,
  Calendar,
  Warehouse,
  CheckCircle2,
  Filter,
  ArrowUpDown,
  Plus,
} from 'lucide-react';
import { INITIAL_BATCHES } from '../../services/api';
import { InventoryBatch } from '../../types';

export const InventoryView: React.FC = () => {
  const [batches, setBatches] = useState<InventoryBatch[]>(INITIAL_BATCHES);
  const [filterMode, setFilterMode] = useState<'ALL' | 'NEAR_EXPIRY' | 'LOW_STOCK'>('ALL');
  const [searchQuery, setSearchQuery] = useState('');

  const filteredBatches = batches.filter((b) => {
    const matchesSearch =
      b.medicine_name.toLowerCase().includes(searchQuery.toLowerCase()) ||
      b.batch_number.toLowerCase().includes(searchQuery.toLowerCase()) ||
      b.shelf_location.toLowerCase().includes(searchQuery.toLowerCase());

    if (!matchesSearch) return false;
    if (filterMode === 'NEAR_EXPIRY') return b.days_to_expiry <= 90;
    if (filterMode === 'LOW_STOCK') return b.is_low_stock;
    return true;
  });

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2">
            <h1 className="text-2xl font-black text-white">Pharmacy Inventory & Batch Control</h1>
            <span className="px-2.5 py-0.5 rounded-full bg-teal-500/10 text-teal-400 text-xs font-bold border border-teal-500/20">
              Lot Tracking & Expiry Active
            </span>
          </div>
          <p className="text-xs text-slate-400 mt-1">
            Physical stock management, warehouse shelf locations, automated reorder triggers, and FEFO sorting.
          </p>
        </div>

        {/* Filter Pills */}
        <div className="flex items-center gap-2 bg-slate-900 border border-slate-800 p-1 rounded-xl">
          <button
            onClick={() => setFilterMode('ALL')}
            className={`px-3 py-1.5 rounded-lg text-xs font-bold transition ${
              filterMode === 'ALL'
                ? 'bg-teal-500 text-slate-950 shadow'
                : 'text-slate-400 hover:text-white'
            }`}
          >
            All Stock
          </button>
          <button
            onClick={() => setFilterMode('NEAR_EXPIRY')}
            className={`px-3 py-1.5 rounded-lg text-xs font-bold transition ${
              filterMode === 'NEAR_EXPIRY'
                ? 'bg-amber-500 text-slate-950 shadow'
                : 'text-slate-400 hover:text-white'
            }`}
          >
            Near Expiry (&lt;90d)
          </button>
          <button
            onClick={() => setFilterMode('LOW_STOCK')}
            className={`px-3 py-1.5 rounded-lg text-xs font-bold transition ${
              filterMode === 'LOW_STOCK'
                ? 'bg-red-500 text-white shadow'
                : 'text-slate-400 hover:text-white'
            }`}
          >
            Low Stock Alerts
          </button>
        </div>
      </div>

      {/* Search Bar */}
      <div className="bg-slate-900 border border-slate-800 rounded-2xl p-4 shadow-lg">
        <div className="relative">
          <Search className="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" />
          <input
            type="text"
            placeholder="Search inventory by medicine name, batch number, aisle or shelf..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full bg-slate-800 border border-slate-700 rounded-xl pl-10 pr-4 py-2 text-xs text-white placeholder:text-slate-400 focus:outline-none focus:border-teal-500"
          />
        </div>
      </div>

      {/* Inventory Table */}
      <div className="bg-slate-900 border border-slate-800 rounded-2xl shadow-xl overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead className="bg-slate-800/80 text-slate-400 font-bold uppercase tracking-wider text-[10px] border-b border-slate-700/80">
              <tr>
                <th className="px-5 py-3.5">Medicine Name</th>
                <th className="px-4 py-3.5">Batch / Lot #</th>
                <th className="px-4 py-3.5">Warehouse & Shelf</th>
                <th className="px-4 py-3.5">Stock Level</th>
                <th className="px-4 py-3.5">Expiry Date</th>
                <th className="px-4 py-3.5">Unit Cost / Price</th>
                <th className="px-4 py-3.5">Status</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800 text-slate-300">
              {filteredBatches.map((batch) => {
                const isNearExp = batch.days_to_expiry <= 90;
                const isCriticalExp = batch.days_to_expiry <= 30;

                return (
                  <tr key={batch.id} className="hover:bg-slate-800/50 transition">
                    <td className="px-5 py-3.5">
                      <div className="font-bold text-white text-xs">{batch.medicine_name}</div>
                      <div className="text-[10px] text-slate-400">Supplier: {batch.supplier_id}</div>
                    </td>
                    <td className="px-4 py-3.5 font-mono">
                      <div className="font-bold text-teal-300">{batch.batch_number}</div>
                      <div className="text-[10px] text-slate-400">{batch.lot_number}</div>
                    </td>
                    <td className="px-4 py-3.5">
                      <div className="text-slate-200">{batch.shelf_location}</div>
                      <div className="text-[10px] text-slate-400">{batch.warehouse_name}</div>
                    </td>
                    <td className="px-4 py-3.5">
                      <div className="flex items-center gap-1.5">
                        <span
                          className={`font-black font-mono text-xs ${
                            batch.is_low_stock ? 'text-red-400' : 'text-white'
                          }`}
                        >
                          {batch.quantity_on_hand} Units
                        </span>
                        {batch.is_low_stock && (
                          <span className="text-[9px] px-1.5 py-0.5 rounded bg-red-500/20 text-red-300 border border-red-500/30">
                            Reorder (Min: {batch.reorder_level})
                          </span>
                        )}
                      </div>
                      <div className="text-[10px] text-slate-400">
                        Reserved: {batch.quantity_reserved}
                      </div>
                    </td>
                    <td className="px-4 py-3.5">
                      <div className="font-mono text-slate-200">{batch.expiry_date}</div>
                      <div
                        className={`text-[10px] font-bold ${
                          isCriticalExp
                            ? 'text-red-400'
                            : isNearExp
                            ? 'text-amber-400'
                            : 'text-emerald-400'
                        }`}
                      >
                        {batch.days_to_expiry} days remaining
                      </div>
                    </td>
                    <td className="px-4 py-3.5 font-mono">
                      <div className="text-white">${batch.selling_price_per_unit.toFixed(2)}</div>
                      <div className="text-[10px] text-slate-400">
                        Cost: ${batch.cost_per_unit.toFixed(2)}
                      </div>
                    </td>
                    <td className="px-4 py-3.5">
                      {batch.is_low_stock ? (
                        <span className="px-2.5 py-1 rounded-full text-[10px] font-extrabold bg-red-500/20 text-red-300 border border-red-500/30">
                          Low Stock
                        </span>
                      ) : isNearExp ? (
                        <span className="px-2.5 py-1 rounded-full text-[10px] font-extrabold bg-amber-500/20 text-amber-300 border border-amber-500/30">
                          FEFO Priority
                        </span>
                      ) : (
                        <span className="px-2.5 py-1 rounded-full text-[10px] font-extrabold bg-emerald-500/20 text-emerald-300 border border-emerald-500/30">
                          Optimal
                        </span>
                      )}
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};
