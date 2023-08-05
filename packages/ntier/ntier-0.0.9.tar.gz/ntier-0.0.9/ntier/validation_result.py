'''Contains the ValidationResult data structure.'''
from typing import (Any, Optional)
from .messages import (MessageData, Messages)

class ValidationResult:
  '''Contains information about whether a validation passes or fails.'''
  def __init__(self, messages: Optional[Messages]) -> None:
    self._messages: Optional[Messages] = messages
    self.output: Any

  def __bool__(self) -> bool:
    return self.is_valid

  @property
  def is_valid(self):
    return not bool(self.messages)

  @property
  def messages(self) -> MessageData:
    if self._messages is None:
      return {}
    return self._messages.messages

  def set_output(self, output: Any) -> 'ValidationResult':
    self.output = output
    return self

  def add_message(self, subject: str, message: str) -> 'ValidationResult':
    if self._messages is None:
      self._messages = Messages()
    self._messages.add_message(subject, message)
    return self

  def add_general_message(self, message: str) -> 'ValidationResult':
    if self._messages is None:
      self._messages = Messages()
    self._messages.add_general_message(message)
    return self

  @classmethod
  def success(cls) -> 'ValidationResult':
    return ValidationResult(None)

  @classmethod
  def failed(cls, messages: Messages) -> 'ValidationResult':
    return ValidationResult(messages)

  @classmethod
  def builder(cls) -> 'ValidationResult':
    return ValidationResult(Messages())
