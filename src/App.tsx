import React, { useState } from 'react';
import { Navbar } from './components/layout/Navbar';
import { Sidebar } from './components/layout/Sidebar';
import { LoginView } from './features/auth/LoginView';
import { DashboardView } from './features/dashboard/DashboardView';
import { PharmacyCommandCenter } from './features/pharmacy/PharmacyCommandCenter';
import { POSView } from './features/pharmacy/POSView';
import { InventoryView } from './features/pharmacy/InventoryView';
import { ClinicalStationView } from './features/clinical/ClinicalStationView';
import { PatientsView } from './features/patients/PatientsView';
import { LaboratoryView } from './features/laboratory/LaboratoryView';
import { BillingView } from './features/billing/BillingView';
import { InsuranceView } from './features/insurance/InsuranceView';
import { TelemedicineView } from './features/telemedicine/TelemedicineView';
import { AIIntelligenceView } from './features/intelligence/AIIntelligenceView';
import { OrganizationView } from './features/administration/OrganizationView';
import { AuditView } from './features/administration/AuditView';
import { DEMO_USERS } from './services/api';
import { User } from './types';

export function App() {
  // Pre-configured instant access: default logged in as Super Admin for direct one-click exploration
  const [currentUser, setCurrentUser] = useState<User | null>(DEMO_USERS.superadmin.user);
  const [activeTab, setActiveTab] = useState<string>('dashboard');
  const [activeHospital] = useState<string>(
    'MediCore Central Hospital & Advanced Medical Center'
  );

  const handleLogout = () => {
    setCurrentUser(null);
  };

  const handleLoginSuccess = (user: User) => {
    setCurrentUser(user);
    setActiveTab('dashboard');
  };

  if (!currentUser) {
    return <LoginView onLoginSuccess={handleLoginSuccess} />;
  }

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col selection:bg-teal-500 selection:text-white">
      {/* Top Navigation Bar */}
      <Navbar
        currentUser={currentUser}
        onLogout={handleLogout}
        onOpenAI={() => setActiveTab('intelligence')}
        activeHospital={activeHospital}
      />

      {/* Main Workspace Layout */}
      <div className="flex flex-1">
        {/* Left Sidebar Navigation */}
        <Sidebar
          activeTab={activeTab}
          setActiveTab={setActiveTab}
          userRole={currentUser.role}
        />

        {/* Content Area */}
        <main className="flex-1 p-6 md:p-8 overflow-y-auto max-w-7xl mx-auto w-full">
          {activeTab === 'dashboard' && (
            <DashboardView
              currentUser={currentUser}
              onNavigate={(tab) => setActiveTab(tab)}
            />
          )}

          {activeTab === 'pharmacy_center' && <PharmacyCommandCenter />}

          {activeTab === 'pos' && <POSView />}

          {activeTab === 'inventory' && <InventoryView />}

          {activeTab === 'medicines' && <InventoryView />}

          {activeTab === 'procurement' && <InventoryView />}

          {activeTab === 'clinical' && <ClinicalStationView />}

          {activeTab === 'patients' && <PatientsView />}

          {activeTab === 'appointments' && <ClinicalStationView />}

          {activeTab === 'drug_safety' && <ClinicalStationView />}

          {activeTab === 'laboratory' && <LaboratoryView />}

          {activeTab === 'billing' && <BillingView />}

          {activeTab === 'insurance' && <InsuranceView />}

          {activeTab === 'telemedicine' && <TelemedicineView />}

          {activeTab === 'intelligence' && <AIIntelligenceView />}

          {activeTab === 'analytics' && <AIIntelligenceView />}

          {activeTab === 'staff' && <OrganizationView />}

          {activeTab === 'organization' && <OrganizationView />}

          {activeTab === 'audit' && <AuditView />}
        </main>
      </div>
    </div>
  );
}

export default App;
