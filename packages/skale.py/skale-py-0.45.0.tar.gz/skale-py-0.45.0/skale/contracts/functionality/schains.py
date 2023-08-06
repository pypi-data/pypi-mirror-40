from skale.contracts import BaseContract
from skale.utils.helper import ip_from_bytes


class SChains(BaseContract):

    def __get_schain_nodes_raw(self, schain_name):
        return self.contract.functions.getSchainNodes(schain_name).call()

    def get_schain_nodes(self, schain_name):
        nodes = []
        raw_nodes = self.__get_schain_nodes_raw(schain_name)

        for i, node in enumerate(raw_nodes):
            node_id_bytes = node[0:10]
            node_id = int.from_bytes(node_id_bytes, byteorder='big')

            ip_bytes = node[10:14]
            ip = ip_from_bytes(ip_bytes)

            port_bytes = node[14:16]
            port = int.from_bytes(port_bytes, byteorder='big')

            nodes.append({
                'schainIndex': i,
                'nodeID': node_id,
                'ip': ip,
                'basePort': port
            })
        return nodes

    def get_schain_by_index(self, index):  # todo: not found at ABI
        return self.contract.functions.getSchainByIndex(index).call()

    def get_schain_price(self, indexOfType, lifetime):
        return self.contract.functions.getSchainPrice(indexOfType, lifetime).call()
