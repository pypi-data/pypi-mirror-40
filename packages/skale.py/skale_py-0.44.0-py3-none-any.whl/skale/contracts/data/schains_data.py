from skale.contracts import BaseContract
from skale.utils.helper import format, ip_from_bytes
from skale.utils.helper import sign_and_send

FIELDS = [
    'name',
    'owner',
    'indexInOwnerList',
    'lifetime',
    'startDate',
    'numberOfNodes',
    'deposit',
    'groupIndex'
]


class SChainsData(BaseContract):
    def __get_raw(self, name):
        return self.contract.functions.schains(name).call()

    @format(FIELDS)
    def get(self, id):
        return self.__get_raw(id)

    @format(FIELDS)
    def get_by_name(self, name):
        id = self.get_id_by_name(name)
        return self.__get_raw(id)

    def get_schain_list_size(self, account):
        return self.contract.functions.getSchainListSize().call({'from': account})

    def get_schain_by_index(self, index):
        return self.contract.functions.getSchainByIndex(index).call()

    def get_id_by_name(self, name):
        return self.contract.functions.getSchainIdBySchainName(name).call()

    def get_schain_ids_for_node(self, node_id):
        # return self.contract.functions.schainsForNodes(int(node_id)).call() # todo: new function - problem with bytes32 map
        return self.contract.functions.getSchainIdsForNode(node_id).call()  # todo: function will be removed

    def get_schains_for_node(self, node_id):
        schains = []
        #schain_contract = self.skale.get_contract_by_name('schains_data')
        schain_ids = self.get_schain_ids_for_node(node_id)
        for schain_id in schain_ids:
            # name = self.get_schain_name_by_schain_id(schain_id)
            schain = self.get(schain_id)
            schains.append(schain)
        return schains

    def get_schain_price(self, indexOfType):
        return self.contract.functions.getSchainPrice(indexOfType).call()
