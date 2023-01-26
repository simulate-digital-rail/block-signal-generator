from orm_importer.importer import ORMImporter
from planproexporter import Generator
from railwayroutegenerator.routegenerator import RouteGenerator
from yaramo.signal import SignalKind, Signal, SignalDirection, SignalFunction
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
                has_main_signal = False
                has_minor_signal = False
                for signal in edge.signals:
                    if signal.kind in [SignalKind.Hauptsignal, SignalKind.Mehrabschnittssignal, SignalKind.Hauptsperrsignal]:
                        has_main_signal = True
                    if signal.kind == SignalKind.Sperrsignal:
                        has_minor_signal = True
                if not has_minor_signal:
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
