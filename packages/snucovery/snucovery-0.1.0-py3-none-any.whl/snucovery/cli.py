import argparse


class Arguments:
    def __init__(self):
        """Aws Asset Discovery

        Discovery command line arguments.
        """
        self.parser = argparse.ArgumentParser(
            description="Aws Asset Discovery",
        )
        self.command_line_arguments()
        self.args = self.get_args()

    def command_line_arguments(self):
        """Command line arguments setter

        Note:
            Returns nothing since it only modifies the argparse object
        """
        self.parser.add_argument('-p', '--profile', help='Aws Profile Name')
        self.parser.add_argument('-w', '--workbook-name', help='Name of the Excel Workbook that will be created')

    def get_args(self):
        """Get arguments passed from command line execution

        Returns:
            Arguments passed from command line
        """
        return self.parser.parse_args()
