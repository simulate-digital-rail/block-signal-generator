from yaramo.signal import SignalKind, Signal, SignalDirection, SignalFunction, SignalState
from yaramo.topology import Topology


class BlockSignalGenerator:

    def __init__(self, topology):
        self.topology: Topology = topology

    def add_block_signals(self):
        for node_id, node in self.topology.nodes.items():
            if len(node.connected_nodes) == 1:
                # node is an end node
                other_node = node.connected_nodes[0]
                edge = self.topology.get_edge_by_nodes(node, other_node)
                # We don't want to add a signal on edges that are an end, e.g. a buffer stop.
                # These are identified by searching for a Sperrsignal that can only show Hp0/Sh0.
                has_end_signal = any(signal.kind == SignalKind.Sperrsignal and signal.supported_states == set(SignalState.hp0) for signal in edge.signals)
                if not has_end_signal:
                    # add virtual block signal as route destination for exit
                    if edge.node_a == node:
                        distance_edge = 5
                        direction = SignalDirection.GEGEN
                    else:
                        distance_edge = edge.length - 5
                        direction = SignalDirection.IN
                    signal = Signal(edge=edge, distance_edge=distance_edge, direction=direction, function=SignalFunction.Block_Signal, kind=SignalKind.Hauptsignal, name=f"BL{node.name}")
                    edge.signals.append(signal)
                    self.topology.add_signal(signal)
