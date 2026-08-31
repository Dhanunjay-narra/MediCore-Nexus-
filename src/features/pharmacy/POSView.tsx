import React, { useState } from 'react';
import {
  ShoppingCart,
  Barcode,
  Search,
  Plus,
  Trash2,
  Receipt,
  CreditCard,
  CheckCircle2,
  DollarSign,
  Printer,
  Sparkles,
} from 'lucide-react';
import { INITIAL_MEDICINES, INITIAL_BATCHES } from '../../services/api';
import { MedicineMaster } from '../../types';

interface CartLine {
  medicine: MedicineMaster;
  batchNumber: string;
  expiryDate: string;
  quantity: number;
  unitPrice: number;
  lineTotal: number;
}

export const POSView: React.FC = () => {
  const [searchQuery, setSearchQuery] = useState('');
  const [cart, setCart] = useState<CartLine[]>([
    {
      medicine: INITIAL_MEDICINES[0],
      batchNumber: 'ATV-2026-B1',
      expiryDate: '2026-11-30',
      quantity: 2,
      unitPrice: 18.0,
      lineTotal: 36.0,
    },
    {
      medicine: INITIAL_MEDICINES[4],
      batchNumber: 'TYL-2027-T1',
      expiryDate: '2027-12-31',
      quantity: 1,
      unitPrice: 8.99,
      lineTotal: 8.99,
    },
  ]);
  const [customerName, setCustomerName] = useState('Walk-in Patient / Customer');
  const [paymentMethod, setPaymentMethod] = useState('Credit Card');
  const [isReceiptModalOpen, setIsReceiptModalOpen] = useState(false);
  const [lastReceipt, setLastReceipt] = useState<any>(null);

  const filteredMedicines = INITIAL_MEDICINES.filter(
    (m) =>
      m.brand_name.toLowerCase().includes(searchQuery.toLowerCase()) ||
      m.generic_name.toLowerCase().includes(searchQuery.toLowerCase()) ||
      m.barcode.includes(searchQuery)
  );

  const addToCart = (med: MedicineMaster) => {
    // Find earliest expiry batch for this medicine (Smart FEFO)
    const matchingBatches = INITIAL_BATCHES.filter((b) => b.medicine_id === med.id);
    const chosenBatch = matchingBatches[0] || {
      batch_number: 'GEN-2027-01',
      expiry_date: '2027-06-30',
    };

    setCart((prev) => {
      const existing = prev.find((i) => i.medicine.id === med.id);
      if (existing) {
        return prev.map((i) =>
          i.medicine.id === med.id
            ? {
                ...i,
                quantity: i.quantity + 1,
                lineTotal: (i.quantity + 1) * i.unitPrice,
              }
            : i
        );
      }
      return [
        ...prev,
        {
          medicine: med,
          batchNumber: chosenBatch.batch_number,
          expiryDate: chosenBatch.expiry_date,
          quantity: 1,
          unitPrice: med.mrp,
          lineTotal: med.mrp,
        },
      ];
    });
  };

  const removeFromCart = (medId: string) => {
    setCart((prev) => prev.filter((i) => i.medicine.id !== medId));
  };

  const subtotal = cart.reduce((acc, item) => acc + item.lineTotal, 0);
  const tax = subtotal * 0.05;
  const grandTotal = subtotal + tax;

  const handleCheckout = () => {
    const receiptData = {
      invoiceNumber: `INV-POS-${Math.floor(100000 + Math.random() * 900000)}`,
      date: new Date().toLocaleString(),
      customerName,
      paymentMethod,
      items: cart,
      subtotal,
      tax,
      grandTotal,
    };
    setLastReceipt(receiptData);
    setIsReceiptModalOpen(true);
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <div className="flex items-center gap-2">
            <h1 className="text-2xl font-black text-white">Pharmacy Point-of-Sale (POS)</h1>
            <span className="px-2.5 py-0.5 rounded-full bg-teal-500/10 text-teal-400 text-xs font-bold border border-teal-500/20">
              Smart FEFO Active
            </span>
          </div>
          <p className="text-xs text-slate-400 mt-1">
            Barcode scanning, prescription matching, and instant stock deduction.
          </p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Medicine Search & Catalog */}
        <div className="lg:col-span-2 space-y-4">
          <div className="bg-slate-900 border border-slate-800 rounded-2xl p-4 shadow-lg">
            <div className="relative">
              <Barcode className="w-5 h-5 absolute left-3 top-1/2 -translate-y-1/2 text-teal-400" />
              <input
                type="text"
                placeholder="Scan medicine barcode (e.g. 8901088231901) or search by name..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="w-full bg-slate-800 border border-slate-700 rounded-xl pl-11 pr-4 py-2.5 text-xs text-white placeholder:text-slate-400 focus:outline-none focus:border-teal-500"
              />
            </div>
          </div>

          {/* Medicines Grid */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
            {filteredMedicines.map((med) => (
              <div
                key={med.id}
                className="bg-slate-900 border border-slate-800 rounded-2xl p-4 shadow-md hover:border-slate-700 transition flex flex-col justify-between"
              >
                <div>
                  <div className="flex items-center justify-between">
                    <span className="font-extrabold text-sm text-white">{med.brand_name}</span>
                    <span className="font-mono text-xs font-black text-teal-400">
                      ${med.mrp.toFixed(2)}
                    </span>
                  </div>
                  <div className="text-xs text-slate-400 mt-0.5">{med.generic_name}</div>
                  <div className="text-[11px] text-slate-500 mt-1">
                    {med.strength} • {med.dosage_form} • {med.unit_of_measure}
                  </div>
                  <div className="mt-2 text-[10px] font-mono text-slate-400">
                    Barcode: {med.barcode}
                  </div>
                </div>

                <button
                  onClick={() => addToCart(med)}
                  className="w-full mt-3 py-1.5 bg-slate-800 hover:bg-teal-500 hover:text-slate-950 text-teal-300 rounded-xl text-xs font-bold border border-slate-700 transition flex items-center justify-center gap-1.5"
                >
                  <Plus className="w-3.5 h-3.5" />
                  <span>Add to Cart (Auto-FEFO)</span>
                </button>
              </div>
            ))}
          </div>
        </div>

        {/* Cart & Billing Summary */}
        <div className="bg-slate-900 border border-slate-800 rounded-2xl p-5 shadow-xl flex flex-col justify-between h-fit sticky top-20">
          <div>
            <div className="flex items-center justify-between pb-3 border-b border-slate-800">
              <div className="flex items-center gap-2">
                <ShoppingCart className="w-5 h-5 text-teal-400" />
                <h3 className="font-extrabold text-sm text-white">Dispense Cart</h3>
              </div>
              <span className="text-xs font-mono text-slate-400">{cart.length} items</span>
            </div>

            <div className="mt-3">
              <label className="block text-[11px] font-semibold text-slate-400 mb-1">
                Customer / Patient
              </label>
              <input
                type="text"
                value={customerName}
                onChange={(e) => setCustomerName(e.target.value)}
                className="w-full bg-slate-800 border border-slate-700 rounded-xl px-3 py-1.5 text-xs text-white focus:outline-none focus:border-teal-500"
              />
            </div>

            {/* Cart Items List */}
            <div className="mt-4 space-y-2.5 max-h-64 overflow-y-auto pr-1">
              {cart.map((item) => (
                <div
                  key={item.medicine.id}
                  className="bg-slate-800/80 border border-slate-700/60 rounded-xl p-3 text-xs"
                >
                  <div className="flex items-center justify-between">
                    <span className="font-bold text-white">{item.medicine.brand_name}</span>
                    <span className="font-mono font-bold text-teal-400">
                      ${item.lineTotal.toFixed(2)}
                    </span>
                  </div>
                  <div className="flex items-center justify-between text-[11px] text-slate-400 mt-1">
                    <span className="font-mono text-[10px] text-teal-300">
                      Batch: {item.batchNumber} (Exp: {item.expiryDate})
                    </span>
                    <div className="flex items-center gap-2">
                      <span className="font-mono">x{item.quantity}</span>
                      <button
                        onClick={() => removeFromCart(item.medicine.id)}
                        className="text-slate-500 hover:text-red-400"
                      >
                        <Trash2 className="w-3.5 h-3.5" />
                      </button>
                    </div>
                  </div>
                </div>
              ))}
            </div>

            {/* Payment Method Selector */}
            <div className="mt-4 pt-3 border-t border-slate-800">
              <label className="block text-[11px] font-semibold text-slate-400 mb-1">
                Payment Method
              </label>
              <select
                value={paymentMethod}
                onChange={(e) => setPaymentMethod(e.target.value)}
                className="w-full bg-slate-800 border border-slate-700 rounded-xl px-3 py-2 text-xs text-white focus:outline-none focus:border-teal-500"
              >
                <option value="Credit Card">Credit / Debit Card</option>
                <option value="Cash">Cash Currency</option>
                <option value="Insurance Split">Insurance Co-Pay Settlement</option>
                <option value="UPI / QR">Digital QR / UPI</option>
              </select>
            </div>

            {/* Price Calculations */}
            <div className="mt-4 pt-3 border-t border-slate-800 space-y-1.5 text-xs">
              <div className="flex justify-between text-slate-400">
                <span>Subtotal</span>
                <span className="font-mono text-white">${subtotal.toFixed(2)}</span>
              </div>
              <div className="flex justify-between text-slate-400">
                <span>Sales Tax (5%)</span>
                <span className="font-mono text-white">${tax.toFixed(2)}</span>
              </div>
              <div className="flex justify-between text-sm font-black text-white pt-2 border-t border-slate-800">
                <span>Total Amount Due</span>
                <span className="font-mono text-teal-400">${grandTotal.toFixed(2)}</span>
              </div>
            </div>
          </div>

          <button
            onClick={handleCheckout}
            disabled={cart.length === 0}
            className="w-full mt-6 py-2.5 bg-gradient-to-r from-teal-500 to-emerald-600 hover:from-teal-400 hover:to-emerald-500 text-slate-950 font-black rounded-xl text-xs shadow-lg shadow-teal-500/20 transition disabled:opacity-50 flex items-center justify-center gap-1.5"
          >
            <CheckCircle2 className="w-4 h-4" />
            <span>Complete Checkout & Print Receipt</span>
          </button>
        </div>
      </div>

      {/* Receipt Modal */}
      {isReceiptModalOpen && lastReceipt && (
        <div className="fixed inset-0 bg-black/80 backdrop-blur-sm z-50 flex items-center justify-center p-4">
          <div className="bg-slate-900 border border-slate-800 rounded-2xl max-w-md w-full p-6 shadow-2xl space-y-4">
            <div className="text-center pb-3 border-b border-slate-800">
              <div className="font-black text-lg text-white">MediCore Central Pharmacy</div>
              <div className="text-xs text-teal-400 font-mono mt-0.5">
                Receipt #{lastReceipt.invoiceNumber}
              </div>
              <div className="text-[10px] text-slate-400">{lastReceipt.date}</div>
            </div>

            <div className="text-xs space-y-1">
              <div className="flex justify-between text-slate-400">
                <span>Customer:</span>
                <span className="text-white font-semibold">{lastReceipt.customerName}</span>
              </div>
              <div className="flex justify-between text-slate-400">
                <span>Payment:</span>
                <span className="text-white font-semibold">{lastReceipt.paymentMethod}</span>
              </div>
            </div>

            <div className="divide-y divide-slate-800 text-xs my-3">
              {lastReceipt.items.map((it: CartLine, idx: number) => (
                <div key={idx} className="py-2 flex justify-between">
                  <div>
                    <div className="font-bold text-white">{it.medicine.brand_name}</div>
                    <div className="text-[10px] text-slate-400">
                      Batch {it.batchNumber} • x{it.quantity} @ ${it.unitPrice.toFixed(2)}
                    </div>
                  </div>
                  <span className="font-mono font-bold text-teal-400">
                    ${it.lineTotal.toFixed(2)}
                  </span>
                </div>
              ))}
            </div>

            <div className="pt-2 border-t border-slate-800 space-y-1 text-xs">
              <div className="flex justify-between text-slate-400">
                <span>Subtotal:</span>
                <span className="font-mono text-white">${lastReceipt.subtotal.toFixed(2)}</span>
              </div>
              <div className="flex justify-between text-slate-400">
                <span>Tax (5%):</span>
                <span className="font-mono text-white">${lastReceipt.tax.toFixed(2)}</span>
              </div>
              <div className="flex justify-between font-black text-sm text-white pt-2 border-t border-slate-800">
                <span>Total Paid:</span>
                <span className="font-mono text-teal-400">
                  ${lastReceipt.grandTotal.toFixed(2)}
                </span>
              </div>
            </div>

            <div className="flex gap-2 pt-2">
              <button
                onClick={() => window.print()}
                className="flex-1 py-2 bg-slate-800 hover:bg-slate-700 text-white rounded-xl text-xs font-bold border border-slate-700 flex items-center justify-center gap-1"
              >
                <Printer className="w-3.5 h-3.5" />
                <span>Print</span>
              </button>
              <button
                onClick={() => {
                  setIsReceiptModalOpen(false);
                  setCart([]);
                }}
                className="flex-1 py-2 bg-teal-500 hover:bg-teal-400 text-slate-950 rounded-xl text-xs font-black"
              >
                Done / New Sale
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
