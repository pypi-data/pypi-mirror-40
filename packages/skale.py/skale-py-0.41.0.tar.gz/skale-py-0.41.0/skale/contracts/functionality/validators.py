from skale.contracts import BaseContract

class Validators(BaseContract):

    def get_periods(self, account): # todo: not found at ABI
        return self.contract.functions.getPeriods().call({'from': account})
