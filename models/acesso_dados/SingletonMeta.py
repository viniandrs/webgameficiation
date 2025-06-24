#models/acesso_dados/SingletonMeta.py

from abc import ABCMeta

class SingletonMeta(ABCMeta):
  """
  Metaclasse para implementar o Design Pattern Singleton, que garante a criação de 
  uma única instância de uma classe
  """

  _instancias = {}

  def __call__(cls, *args, **kwds):
    """
    Verifica se já existe uma instância e a retorna, ou cria uma nova
    """
    if cls not in cls._instancias:
      cls._instancias[cls] = super().__call__(*args, **kwds)
    return cls._instancias[cls]