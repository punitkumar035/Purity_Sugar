"""
solver/stations/distributor.py
Purity for Sugar — Distributor / Stream Splitter Model

Rules:
  - Splits single inlet flow into multiple outlet streams (ports 0 to 7)
  - Split by specified percentages (use_percent=True) or specified mass flows
  - Preserves exact temperature, pressure, concentration, and enthalpy of fluid
  - If sum of specified flows exceeds inlet flow, flows are proportionally scaled with a warning (RULES_v5.md §C2)
"""

from __future__ import annotations
from typing import Dict, Any, List

from solver.stations.base import BaseStation, StationResult
from solver.stream import Stream, mix_streams


class DistributorStation(BaseStation):
    def calculate(
        self,
        inlet_streams: Dict[str, Stream],
        inlet_flow_ids: List[str],
        outlet_flow_ids: List[str],
        atmospheric_p_kpa: float = 101.325,
    ) -> StationResult:
        warnings = []
        if not inlet_flow_ids:
            in_stream = Stream(mass_flow_kgh=0.0, temperature_c=20.0, pressure_kpa=atmospheric_p_kpa)
        else:
            inlets = [inlet_streams[fid] for fid in inlet_flow_ids if fid in inlet_streams]
            in_stream = mix_streams(inlets)

        total_in_flow = in_stream.mass_flow_kgh
        n_out = len(outlet_flow_ids)
        outlet_streams = {}

        if n_out == 0:
            return StationResult(
                outlet_streams={},
                calculated_properties={"total_inlet_flow_kgh": total_in_flow},
                warnings=["Distributor has no outgoing flows."],
            )

        use_pct = self.get_bool("use_percent", True)

        # Collect configured quantities for up to 8 ports
        configured_q = []
        for i in range(n_out):
            q_val = self.get_float(f"quantity_{i}", -1.0)
            configured_q.append(q_val)

        # Allocate flow to each outlet
        out_flows = [0.0] * n_out
        if use_pct:
            # Check if percentages were entered
            pct_sum = sum(q for q in configured_q if q >= 0.0)
            if pct_sum <= 0.0:
                # Default: split equally
                equal_share = total_in_flow / n_out
                out_flows = [equal_share] * n_out
            else:
                for i in range(n_out):
                    pct = configured_q[i] if configured_q[i] >= 0.0 else 0.0
                    out_flows[i] = total_in_flow * (pct / 100.0)
                # If sum of percentages != 100, normalize or distribute remainder
                if abs(pct_sum - 100.0) > 0.01:
                    scale = 100.0 / pct_sum
                    out_flows = [f * scale for f in out_flows]
                    warnings.append(
                        f"Distributor {self.station_number}: output percentages sum to {pct_sum:.1f}%, normalized to 100%."
                    )
        else:
            # Absolute kg/h specified
            spec_sum = sum(q for q in configured_q if q >= 0.0)
            if spec_sum > total_in_flow and total_in_flow > 0:
                scale = total_in_flow / spec_sum
                out_flows = [(q if q >= 0.0 else 0.0) * scale for q in configured_q]
                warnings.append(
                    f"Distributor {self.station_number}: specified flows ({spec_sum:.1f} kg/h) exceed inlet ({total_in_flow:.1f} kg/h), scaled down proportionally."
                )
            else:
                unallocated_flow = total_in_flow - spec_sum
                unspec_indices = [i for i, q in enumerate(configured_q) if q < 0.0]
                for i in range(n_out):
                    if configured_q[i] >= 0.0:
                        out_flows[i] = configured_q[i]
                if unspec_indices:
                    share = max(0.0, unallocated_flow) / len(unspec_indices)
                    for i in unspec_indices:
                        out_flows[i] = share

        for i, ofid in enumerate(outlet_flow_ids):
            s = in_stream.copy()
            s.mass_flow_kgh = max(0.0, out_flows[i])
            outlet_streams[ofid] = s

        return StationResult(
            outlet_streams=outlet_streams,
            calculated_properties={
                "inlet_flow_kgh": total_in_flow,
                "outlet_flows_kgh": {ofid: s.mass_flow_kgh for ofid, s in outlet_streams.items()},
                "split_count": n_out,
            },
            warnings=warnings,
        )
