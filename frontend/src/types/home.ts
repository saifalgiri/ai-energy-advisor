export type HeatingType = 'gas' | 'electric' | 'heat_pump' | 'oil'  | 'solar';
export type InsulationLevel = 'minimal' | 'moderate' | 'good' | 'excellent';
export type WindowsType = 'single' | 'double' | 'triple';
export type RoofType = 'flat' | 'pitched' | 'metal' | 'tile';

export interface HomeProfile {
  id?: string;
  size_sqft: number;
  year_built: number;
  heating_type: HeatingType;
  insulation_level: InsulationLevel;
  windows_type: WindowsType;
  roof_type: RoofType;
  monthly_energy_bill: number;
  num_occupants: number;
  location?: string;
}


export interface EnergyAdvice {
  id: string;
  home_id: string;
  recommendations: Recommendation[];
  estimated_savings: number;
  priority_score: number;
  generated_at: string;
}

export interface Recommendation {
  id?: string;
  title: string;
  description: string;
  estimated_cost: string;
  estimated_savings: string;
  priority: 'high' | 'medium' | 'low';
  category: 'heating' | 'insulation' | 'windows' | 'appliances' | 'habits' | 'renewable';
}

export interface SSEMessage {
  type: 'connected' | 'recommendation' | 'complete' | 'error';
  recommendation?: Recommendation;
  home_id?: string;
  error?: string;
}
