#!/usr/bin/env python
"""Interfaces implemented by serializable objects."""



# Using lowercase function naming to match the JavaScript names.
# pylint: disable-msg=g-bad-name


class Encodable(object):
  """An interface implemented by objects that can serialize themselves."""

  def encode(self, encoder):
    """Encodes the object in a format compatible with Serializer.

    Args:
      encoder: A function that can be called to encode the components of
          an object.

    Returns:
      The encoded form of the object.
    """
    raise NotImplementedError('Encodable classes must implement encode().')



class EncodableFunction(object):
  """An interface implemented by functions that can serialize themselves."""

  def encode_invocation(self, encoder):
    """Encodes the function in a format compatible with Serializer.

    Args:
      encoder: A function that can be called to encode the components of
          an object.

    Returns:
      The encoded form of the function.
    """
    raise NotImplementedError(
        'EncodableFunction classes must implement encode_invocation().')

