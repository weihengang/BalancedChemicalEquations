The code solves chemical equations first by identifying any elements that are unique on each side, and then subsituting values for them. 
Afterwards, it solves the rest with linear equation (simultaneous equations have not been added yet).
The program may sometimes output decimal coefficients, or those which are not fully simplified.

Example chemical equation inputs (that it can solve):                                                                                                                                                            
  CO2 + H2O -> C6H12O6 + O2                                                                                                                                                            
  SiCl4 + H2O -> H4SiO4 + HCl                                                                                                                                                            
  Al + HCl -> AlCl3 + H2                                                                                                                                                            
  Na2CO3 + HCl -> NaCl + H2O + CO2                                                                                                                                                            
  C7H6O2 + O2 -> CO2 + H2O                                                                                                                                                            
  Fe2(SO4)3 + KOH -> K2SO4 + Fe(OH)3                                                                                                                                                            
  Ca3(PO4)2 + SiO2 -> P4O10 + CaSiO3                                                                                                                                                            
  KClO3 -> KClO4 + KCl                                                                                                                                                            
  Al2(SO4)3 + Ca(OH)2 -> Al(OH)3 + CaSO4                                                                                                                                                            
  H2SO4 + HI -> H2S + I2 + H2O                                                                                                                                                            
  (NH4)2Cr2O7 -> Cr2O3 + N2 + H2O                                                                                                                                                                   
  C7H16 + O2 -> CO2 + H2O                                                                                                                                                            
  Ba3N2 + H2O -> Ba(OH)2 + NH3                                                                                                                                                            
  CaCl2 + Na3PO4 -> Ca3(PO4)2 + NaCl                                                                                                                                                            
  FeS + O2 -> Fe2O3 + SO2                                                                                                                                                            
  PCl5 + H2O -> H3PO4 + HCl                                                                                                                                                            
  As + NaOH -> Na3AsO3 + H2                                                                                                                                                            
  Hg(OH)2 + H3PO4 -> Hg3(PO4)2 + H2O                                                                                                                                                            
  HClO4 + P4O10 -> H3PO4 + Cl2O7                                                                                                                                                            
  CO + H2 -> C8H18 + H2O                                                                                                                                                            
  KClO3 + P4 -> P4O10 + KCl                                                                                                                                                            
  SnO2 + H2 -> Sn + H2O                                                                                                                                                            
  KOH + H3PO4 -> K3PO4 + H2O                                                                                                                                                            
  KNO3 + H2CO3 -> K2CO3 + HNO3                                                                                                                                                            
  Na3PO4 + HCl -> NaCl + H3PO4                                                                                                                                                            
  TiCl4 + H2O -> TiO2 + HCl                                                                                                                                                            
  C2H6O + O2 -> CO2 + H2O                                                                                                                                                            
  NH3 + O2 -> NO + H2O                                                                                                                                                            
  B2Br6 + HNO3 -> B(NO3)3 + HBr
