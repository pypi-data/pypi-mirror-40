from skale.contracts import BaseContract
from skale.utils.helper import sign_and_send


class ValidatorsData(BaseContract):

    def get_reward_period(self):
        constants = self.skale.get_contract_by_name('constants')
        return constants.contract.functions.rewardPeriod().call()

    def get_delta_period(self):
        constants = self.skale.get_contract_by_name('constants')
        return constants.contract.functions.deltaPeriod().call()

    def get_validated_array(self, node_id, account):
        return self.contract.functions.getValidatedArray(node_id).call({'from': account})
