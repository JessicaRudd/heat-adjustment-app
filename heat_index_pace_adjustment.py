class HeatIndexPaceAdjustment:
    """
    Calculates a running pace adjustment based on the heat index, taking into account whether the runner is elite or non-elite.
    """

    def __init__(self, heat_index, is_elite):
        """
        Initializes the HeatIndexPaceAdjustment object with the maximum temperature, humidity, and whether the runner is elite.

        :param max_temp: Maximum temperature in Celsius.
        :param humidity: Relative humidity as a percentage.
        :param is_elite: True if the runner is elite, False otherwise.
        """
        self.heat_index = heat_index
        self.is_elite = is_elite


    # def heat_index(self):
    #     """
    #     Calculates the heat index in Celsius using the maximum temperature and relative humidity.

    #     :return: Heat index in Celsius.
    #     """
    #     c1 = -8.78469475556
    #     c2 = 1.61139411
    #     c3 = 2.33854883889
    #     c4 = -0.14611605
    #     c5 = -0.012308094
    #     c6 = -0.0164248277778
    #     c7 = 0.002211732
    #     c8 = 0.00072546
    #     c9 = -0.000003582

    #     T = self.max_temp
    #     R = self.humidity / 100.0

    #     HI = c1 + (c2 * T) + (c3 * R) + (c4 * T * R) + (c5 * T * T) + (c6 * R * R) + (c7 * T * T * R) + (c8 * T * R * R) + (c9 * T * T * R * R)

    #     return HI

    def pace_adjustment(self):
        """
        Calculates the pace adjustment based on the heat index, taking into account whether the runner is elite or non-elite.

        :return: Pace adjustment in seconds per kilometer.
        """
        HI = self.heat_index()
        if HI is not None:
            if HI >= 80:
                pace_adjustment = "+30 seconds per mile"
            elif HI >= 75:
                pace_adjustment = "+20 seconds per mile"
            elif HI >= 70:
                pace_adjustment = "+10 seconds per mile"
            elif HI <= 40:
                pace_adjustment = "-30 seconds per mile"
            elif HI <= 45:
                pace_adjustment = "-20 seconds per mile"
            elif HI <= 50:
                pace_adjustment = "-10 seconds per mile"

        return pace_adjustment