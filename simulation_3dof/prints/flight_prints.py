class flight_prints_3dof():
    """
    
    This class holds the printing methods
    of the flight class

    Attributes
    ----------
    flight_prints_3dof.flight : flight_3dof
        Instance of flight_3dof, with which the prints are 
        obtained.
    """
    def __init__(self, flight) -> None:
        """
        Parameters
        ---------
        flight : flight_3dof
            Instance of flight_3dof, that will be used to 
            obtain the prints
        """
        self.flight = flight
    

    def apogee_conditions(self) -> None:
        """
        Prints the most relevatn information form the flight
        """
        print("\nApogee conditions: ")
        print(f"Apogee Height ASL: {self.flight.apogee_z}")
        print(f"Apogee X: {self.flight.apogee_u[0]}")
        print(f"Apogee Y: {self.flight.apogee_u[1]}")
        print(f"Apogee time: {self.flight.apogee_t}")

    def impact_conditions(self) -> None:
        print("\nImpact conditions: ")
        print(f"Downrange impact: {self.flight.landing_downrange}")
        print(f"Impact time: {self.flight.landing_t}")

    def all(self) -> None:
        """
        prints all the methods in the flight_prints_3dof class
        """
        self.apogee_conditions()
        self.impact_conditions()