"""
Code for menu class, to be used a few times but probably only a few times. Bit clumsy round the rim tbh but it'll do
for now I think.
"""
from typing import List, Tuple, Callable
from support_funcs import unpack_list_to_hyphened_string


class Menu:
    """Class containing all the code needed for the menus structure in the system.
    """
    def __init__(self) -> None:
        self._run_sys = True

    @property
    def run_sys(self) -> bool:
        """Get the _run_sys attr from self.

        Returns
        -------
        bool
            The value of the boolean class attribute _run_sys.
        """
        return self._run_sys

    @run_sys.setter
    def run_sys(
        self,
        val: bool,
    ) -> None:
        """Setter for the _run_sys attr from self.

        Parameters
        ----------
        val : A boolean value indicating whether or not to run the system.
        """
        self._run_sys = val

    def run_menu(
        self,
        options: List[Tuple[str, Callable]],
        check_portfolios: bool=True,
        message: str='',
        ) -> None:
        """Runs the main menu until it doesn't anymore, at which point, it stops (if you can believe it :O).

        Notes
        -----
        Also prints a little opening schpeel.

        Parameters
        ----------
        options : List of tuples containing the description of the method and the unexecuted function.
        check_portfolios : passed to get_menu, used there to determine whether to query the existance of portfolios in
        the database.
        message : Message to print on start up.
        """
        print(message)

        while self.run_sys:
            self.get_menu(options=options, check_portfolios=check_portfolios)

    def get_menu(
        self,
        options: Tuple[Tuple[str, Callable]],
        check_portfolios: bool=True,
        ) -> bool:
        """Generates the main menu, to be ran in run_menu

        Parameters
        ----------
        options : Tuple of tuples containing the description of the method and the unexecuted function.
        check_portfolios : passed to get_menu, used there to determine whether to query the existance of portfolios in
        the database.

        Returns
        -------
        bool
            Returns False if the user wishes to leave the menu, else returns True
        """
        if check_portfolios:
            self.check_for_portfolios()

        choose = input("what would you like to do?:"
                       f"{unpack_list_to_hyphened_string(list(enumerate([option[0] for option in options])))}\n"
                       "type '<' to return to previous menu\n")
        menu = dict(enumerate([option[1] for option in options]))

        if choose in [str(key) for key in menu.keys()]:
            menu[int(choose)]()
        elif choose == '<':
            self.run_sys = False
        else:
            print('invalid selection!\n')

    def check_for_portfolios(self) -> None:
        pass  # to be overwritten by children
