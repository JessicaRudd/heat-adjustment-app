class HeatIndexPaceAdjustment:
    """
    Calculates a running pace adjustment based on the heat index, taking into account whether the runner is elite or non-elite.
    """

    def __init__(self, heat_index, is_elite):
        """
        Initializes the HeatIndexPaceAdjustment object with the maximum temperature, humidity, and whether the runner is elite.

        :param humidity: Relative humidity as a percentage.
        :param is_elite: True if the runner is elite, False otherwise.
        """
        self.heat_index = heat_index
        self.is_elite = is_elite
        self.pace_adjust = None
 

    def pace_adjustment(self):
        """
        Calculates the pace adjustment based on the heat index, taking into account whether the runner is elite or non-elite.

        :return: Pace adjustment in seconds per kilometer.
        """
        HI = self.heat_index

        if HI is not None:
            if HI >= 80:
                pace_adjust = "+30 seconds per mile"
            elif HI >= 75:
                pace_adjust = "+20 seconds per mile"
            elif HI >= 70:
                pace_adjust = "+10 seconds per mile"
            elif HI <= 40:
                pace_adjust = "-30 seconds per mile"
            elif HI <= 45:
                pace_adjust = "-20 seconds per mile"
            elif HI <= 50:
                pace_adjust = "-10 seconds per mile"
            else:
                pace_adjust = "No pace adjustment needed"
            
        else:
            None

        return pace_adjust
            
if __name__ == '__main__':

     
    w = HeatIndexPaceAdjustment(80.85, False)

    pace_adjustment = w.pace_adjustment()
    print(pace_adjustment)