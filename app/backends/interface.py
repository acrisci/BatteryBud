from typing import Callable, Any
from app.indicator import Status

class BackendInterface:
    '''
    Backends should inherit from this class and implement these methods. The
    backend is given to the indicator which will call its methods to get
    information about the battery and power source and subscribe to power
    change events.
    '''

    def get_status(self) -> Status:
        '''
        Get the charging status of the battery.
        '''
        raise NotImplmentedError()


    def get_percent(self) -> float:
        '''
        Get the battery charge percentage.
        '''
        raise NotImplmentedError()


    def on_status_change(self, fn: Callable[[Status], None]) -> None:
        '''
        Register a callback for when the battery changes charging status.
        '''
        raise NotImplmentedError()


    def on_percent_change(self, fn: Callable[[float], None]) -> None:
        '''
        Register a callback for when the battery changes charge percent.
        '''
        raise NotImplmentedError()
