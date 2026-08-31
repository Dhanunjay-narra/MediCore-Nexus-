/**
 * MediCore Nexus - Comprehensive TypeScript Definitions
 * Type interfaces across all 24 healthcare & pharmacy domains
 */

export type UserRole =
  | 'Super Admin'
  | 'Hospital Admin'
  | 'Pharmacy Admin'
  | 'Doctor'
  | 'Pharmacist'
  | 'Pharmacy Technician'
  | 'Nurse'
  | 'Lab Technician'
  | 'Billing Officer'
  | 'Insurance Officer'
  | 'Receptionist'
  | 'Patient'
  | 'Supplier'
  | 'Auditor';

export interface User {
  id: string;
  email: string;
  username: string;
  full_name: string;
  phone_number?: string;
  role: UserRole;
  hospital_id?: string;
  department_id?: string;
  avatar_url?: string;
  is_active: boolean;
  is_verified: boolean;
  mfa_enabled: boolean;
  last_login_at?: string;
}

export interface Patient {
  id: string;
  mrn: string;
  first_name: string;
  last_name: string;
  dob: string;
  gender: 'Male' | 'Female' | 'Other';
  blood_group: string;
  email?: string;
  phone: string;
  address: string;
  city: string;
  state: string;
  zip_code: string;
  emergency_contact_name: string;
  emergency_contact_phone: string;
  emergency_contact_relationship: string;
  allergies: string[];
  chronic_conditions: string[];
  medical_alerts: string[];
  primary_physician_id?: string;
  insurance_policy_number?: string;
  insurance_provider?: string;
  created_at: string;
  is_active: boolean;
}

export interface Doctor {
  id: string;
  user_id: string;
  full_name: string;
  license_number: string;
  specialization: string;
  department_id: string;
  hospital_id: string;
  consultation_fee: number;
  telemedicine_fee: number;
  available_days: string[];
  work_start_time: string;
  work_end_time: string;
  room_number: string;
  biography: string;
  rating: number;
  total_reviews: number;
  is_available: boolean;
}

export interface Appointment {
  id: string;
  patient_id: string;
  patient_name: string;
  doctor_id: string;
  doctor_name: string;
  department_id: string;
  appointment_type: 'In-Person Consultation' | 'Telemedicine Video' | 'Follow-up' | 'STAT';
  scheduled_datetime: string;
  duration_minutes: number;
  reason_for_visit: string;
  token_number: number;
  priority: 'Normal' | 'Urgent' | 'Emergency';
  status: 'Scheduled' | 'Confirmed' | 'Checked-In' | 'Waiting' | 'In-Consultation' | 'Completed' | 'Cancelled' | 'No-Show';
  created_at: string;
  checked_in_at?: string;
}

export interface VitalSigns {
  temperature_c: number;
  heart_rate_bpm: number;
  blood_pressure_systolic: number;
  blood_pressure_diastolic: number;
  respiratory_rate_bpm: number;
  oxygen_saturation_pct: number;
  height_cm: number;
  weight_kg: number;
  bmi: number;
  pain_score_10: number;
}

export interface DiagnosisItem {
  icd10_code: string;
  description: string;
  is_primary: boolean;
  status: 'Active' | 'In-Remission' | 'Resolved';
}

export interface ClinicalEncounter {
  id: string;
  patient_id: string;
  doctor_id: string;
  appointment_id?: string;
  encounter_type: string;
  chief_complaint: string;
  subjective_notes: string;
  objective_findings: string;
  assessment: string;
  clinical_plan: string;
  vitals: VitalSigns;
  diagnoses: DiagnosisItem[];
  encounter_date: string;
  is_locked: boolean;
}

export interface MedicineMaster {
  id: string;
  brand_name: string;
  generic_name: string;
  sku_code: string;
  barcode: string;
  dosage_form: string;
  strength: string;
  unit_of_measure: string;
  route_of_administration: string;
  manufacturer: string;
  therapeutic_class: string;
  is_prescription_required: boolean;
  is_controlled_substance: boolean;
  controlled_schedule?: string;
  storage_condition: string;
  contraindications: string[];
  standard_unit_price: number;
  mrp: number;
  is_active: boolean;
}

export interface InventoryBatch {
  id: string;
  medicine_id: string;
  medicine_name: string;
  batch_number: string;
  lot_number: string;
  expiry_date: string;
  manufacturing_date: string;
  quantity_on_hand: number;
  quantity_reserved: number;
  reorder_level: number;
  cost_per_unit: number;
  selling_price_per_unit: number;
  warehouse_name: string;
  shelf_location: string;
  supplier_id: string;
  days_to_expiry: number;
  is_near_expiry: boolean;
  is_expired: boolean;
  is_low_stock: boolean;
}

export interface PrescriptionItem {
  medicine_id: string;
  medicine_name: string;
  dosage: string;
  frequency: string;
  duration_days: number;
  quantity: number;
  route: string;
  instructions: string;
  refills_allowed: number;
  refills_remaining: number;
}

export interface Prescription {
  id: string;
  rx_number: string;
  patient_id: string;
  patient_name: string;
  doctor_id: string;
  doctor_name: string;
  encounter_id?: string;
  diagnosis_summary: string;
  clinical_notes?: string;
  items: PrescriptionItem[];
  digital_signature_hash: string;
  qr_code_payload: string;
  status: 'Active' | 'Validated' | 'Dispensed' | 'Refilled' | 'Cancelled' | 'Expired';
  created_at: string;
  validated_at?: string;
  validated_by_pharmacist?: string;
}

export interface DrugInteractionAlert {
  drug_a: string;
  drug_b: string;
  severity: 'Critical' | 'High' | 'Moderate' | 'Minor';
  mechanism: string;
  clinical_recommendation: string;
}

export interface AllergyAlert {
  medicine_name: string;
  allergen_matched: string;
  severity: 'Critical' | 'High' | 'Moderate';
  clinical_recommendation: string;
}

export interface SafetyCheckResult {
  patient_id: string;
  overall_risk_level: 'Critical' | 'High' | 'Medium' | 'Normal';
  risk_score_100: number;
  is_safe_to_dispense: boolean;
  interaction_alerts: DrugInteractionAlert[];
  allergy_alerts: AllergyAlert[];
  contraindication_alerts: string[];
  duplicate_therapy_alerts: string[];
  special_population_warnings: string[];
}

export interface LabTestItem {
  test_code: string;
  test_name: string;
  parameter_name: string;
  measured_value?: string;
  unit: string;
  reference_range_min: number;
  reference_range_max: number;
  is_abnormal: boolean;
  is_critical: boolean;
  flag?: string;
}

export interface LabOrder {
  id: string;
  order_number: string;
  patient_id: string;
  patient_name: string;
  doctor_id: string;
  doctor_name: string;
  order_type: string;
  sample_type: string;
  sample_barcode: string;
  tests: LabTestItem[];
  clinical_indication: string;
  status: 'Ordered' | 'Sample Collected' | 'Processing' | 'Verified' | 'Reported';
  ordered_at: string;
  reported_at?: string;
  technician_name?: string;
}

export interface InvoiceItem {
  service_type: string;
  description: string;
  quantity: number;
  unit_price: number;
  discount: number;
  tax: number;
  net_total: number;
}

export interface Invoice {
  id: string;
  invoice_number: string;
  patient_id: string;
  patient_name: string;
  hospital_id: string;
  insurance_claim_id?: string;
  insurance_coverage_amount: number;
  patient_copay_amount: number;
  subtotal: number;
  total_tax: number;
  total_discount: number;
  gross_total: number;
  balance_due: number;
  payment_status: 'Pending' | 'Partially Paid' | 'Paid' | 'Void' | 'Refunded';
  created_at: string;
  paid_at?: string;
  items: InvoiceItem[];
}

export interface InsuranceClaim {
  id: string;
  claim_number: string;
  patient_id: string;
  patient_name: string;
  insurance_provider: string;
  policy_number: string;
  group_number: string;
  claim_type: string;
  billed_amount: number;
  deductible_amount: number;
  copay_amount: number;
  approved_amount: number;
  diagnosis_codes: string[];
  treatment_summary: string;
  status: 'Submitted' | 'Under Review' | 'Pre-Authorized' | 'Approved' | 'Settled' | 'Rejected';
  adjudication_notes?: string;
  submitted_at: string;
  settled_at?: string;
}

export interface TelemedicineSession {
  id: string;
  appointment_id: string;
  patient_id: string;
  patient_name: string;
  doctor_id: string;
  doctor_name: string;
  scheduled_start: string;
  room_token: string;
  is_video_enabled: boolean;
  is_audio_enabled: boolean;
  clinical_notes?: string;
  session_status: 'Scheduled' | 'Waiting' | 'In-Call' | 'Completed' | 'Missed';
  call_duration_seconds: number;
  created_at: string;
}

export interface NotificationItem {
  id: string;
  recipient_user_id: string;
  recipient_name: string;
  channel: 'In-App' | 'SMS' | 'Email' | 'WhatsApp' | 'Push';
  category: string;
  title: string;
  message: string;
  is_read: boolean;
  sent_at: string;
}

export interface AuditLog {
  id: string;
  event_time: string;
  actor_user_id: string;
  actor_name: string;
  actor_role: string;
  action_type: string;
  resource_type: string;
  resource_id: string;
  ip_address: string;
  details: string;
  compliance_tag: string;
}
