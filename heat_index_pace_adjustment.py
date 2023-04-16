class HeatIndexPaceAdjustment:
    """
    Calculates a running pace adjustment based on the heat index, taking into account whether the runner is elite or non-elite.
    """

    def __init__(self, temp, dew_point, is_elite):
        """
        Initializes the HeatIndexPaceAdjustment object with the maximum temperature, humidity, and whether the runner is elite.

        :param humidity: Relative humidity as a percentage.
        :param is_elite: True if the runner is elite, False otherwise.
        """
        self.temp = temp
        self.dew_point = dew_point
        self.is_elite = is_elite
        self.pace_adjust = None
 
    def _pace_calc():
        pass

    def pace_adjustment(self):
        """
        Calculates the pace adjustment based on the heat index, taking into account whether the runner is elite or non-elite.

        :return: Pace adjustment in seconds per kilometer.
        """

        adjust_metic = self.temp + self.dew_point
        print(adjust_metic)

        if adjust_metic is not None:
            if adjust_metic <= 100:
                pace_adjustment = "No pace adjustment needed"
            elif 100 < adjust_metic <= 110:
                pace_adjustment = "0.5%"
            elif 110 < adjust_metic <= 120:
                pace_adjustment = "1.0%"
            elif 120 < adjust_metic <= 130:
                pace_adjustment = "1.5%"
            elif 130 < adjust_metic <= 140:
                pace_adjustment = "2.5%"
            elif 140 < adjust_metic <= 150:
                pace_adjustment = "4.0%"
            elif 150 < adjust_metic <= 160:
                pace_adjustment = "5.5%"
            elif 160 < adjust_metic <= 170:
                pace_adjustment = "7.0%"
            elif 170 < adjust_metic <= 180:
                pace_adjustment = "9.0%"
            elif adjust_metic > 180:
                pace_adjustment = "Hard running not recommended"
        else:
            None

        return pace_adjustment

        # HI = self.heat_index

        # if HI is not None:
        #     if HI >= 80:
        #         pace_adjust = "+30 seconds per mile"
        #     elif HI >= 75:
        #         pace_adjust = "+20 seconds per mile"
        #     elif HI >= 70:
        #         pace_adjust = "+10 seconds per mile"
        #     elif HI <= 40:
        #         pace_adjust = "-30 seconds per mile"
        #     elif HI <= 45:
        #         pace_adjust = "-20 seconds per mile"
        #     elif HI <= 50:
        #         pace_adjust = "-10 seconds per mile"
        #     else:
        #         pace_adjust = "No pace adjustment needed"
            
        # else:
        #     None

        return pace_adjust
            
if __name__ == '__main__':

     
    w = HeatIndexPaceAdjustment(80.85, False)

    pace_adjustment = w.pace_adjustment()
    print(pace_adjustment)