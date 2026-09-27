"""
engine/__init__.py
Purity for Sugar — Python Thermodynamics Engine
Phase 02: Calculation Modules

All modules enforce SI units internally:
  - Mass flow  : kg/h
  - Temperature: °C  (converted to K for CoolProp: T_K = t + 273.15)
  - Pressure   : kPa absolute (converted to Pa for CoolProp: P_Pa = P_kpa * 1000)
  - DS, Purity : fractions 0–1 (NOT percentages inside engines)
  - Enthalpy   : kJ/kg
  - Cp         : kJ/(kg·K)
  - Density    : kg/m³

Source authority: Sugar's Help Book (.agents/skills/sugars-helpbook/)
Engineering rulebook: RULES_v5.md
"""

__version__ = "2.0.0"
__author__ = "Purity for Sugar — Agent 4 Developer"
