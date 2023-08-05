'''Contains the StructuredTransaction class.'''
from typing import (Any, Mapping, MutableMapping, Optional, Tuple)
from ntier.policy_result import PolicyResult
from ntier.transaction_base import TransactionBase
from ntier.transaction_result import TransactionResult
from ntier.validation_result import ValidationResult

InputData = Mapping[str, Any]
State = MutableMapping[str, Any]

class APITransactionBase(TransactionBase):
  '''Allows child classes to define parts of a standard API request life-cycle:
    - initialize
    - authenticate
    - find
    - authorize
    - validate
    - perform
  '''
  async def execute(self, data: InputData) -> TransactionResult:
    '''Calls and response properly to overridden methods to run a standard API request.'''
    state = await self.initialize({'input_data': data})

    (is_authenticated, state) = await self.authenticate(state)
    if not is_authenticated:
      return TransactionResult.not_authenticated()

    (missing_entity_name, state) = await self.find(state)
    if missing_entity_name:
      return TransactionResult.not_found(missing_entity_name)

    (policy_result, state) = await self.authorize(state)
    if not policy_result.is_valid:
      return TransactionResult.not_authorized(policy_result)

    (validation_result, state) = await self.validate(state)
    if not validation_result.is_valid:
      return TransactionResult.not_valid(validation_result)

    result = await self.perform(state)
    return result

  async def initialize(self, state: State) -> State:
    return state

  async def authenticate(self, state: State) -> Tuple[bool, State]:
    return (True, state)

  async def find(self, state: State) -> Tuple[Optional[str], State]:
    return (None, state)

  async def authorize(self, state: State) -> Tuple[PolicyResult, State]:
    return (PolicyResult.success(), state)

  async def validate(self, state: State) -> Tuple[ValidationResult, State]:
    return (ValidationResult.success(), state)

  async def perform(self, state: State) -> TransactionResult:
    return TransactionResult.success()
