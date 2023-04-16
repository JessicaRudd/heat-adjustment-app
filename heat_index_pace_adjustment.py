import math

class HeatIndexPaceAdjustment:
    """
    Calculates a running pace adjustment based on the heat index, taking into account whether the runner is elite or non-elite.
    """

    def __init__(self, temp, dew_point, pace_minutes, is_elite):
        """
        Initializes the HeatIndexPaceAdjustment object with the maximum temperature, humidity, and whether the runner is elite.

        :param humidity: Relative humidity as a percentage.
        :param is_elite: True if the runner is elite, False otherwise.
        """
        self.temp = temp
        self.dew_point = dew_point
        self.is_elite = is_elite
        self.pace_minutes = pace_minutes
        self.adjustment = None
 
    def _pace_calc(self, adjust):
        adjust_decimal = adjust / 100
        pace_add = self.pace_minutes * adjust_decimal
        new_pace = math.modf(self.pace_minutes + pace_add)
        minutes = int(new_pace[1])
        seconds = int(new_pace[0]*60)
        return minutes, seconds

    def pace_adjustment(self):
        """
        Calculates the pace adjustment based on the heat index, taking into account whether the runner is elite or non-elite.

        :return: Pace adjustment in seconds per kilometer.
        """

        adjust_metic = int(self.temp) + int(self.dew_point)
        # print(adjust_metic)

        if adjust_metic is not None:
            if adjust_metic <= 100:
                pace_adjustment = "No pace adjustment needed"
            elif 100 < adjust_metic <= 110:
                self.adjustment = 0.5
            elif 110 < adjust_metic <= 120:
                self.adjustment = 1.0
            elif 120 < adjust_metic <= 130:
                self.adjustment = 1.5
            elif 130 < adjust_metic <= 140:
                self.adjustment = 2.5
            elif 140 < adjust_metic <= 150:
                self.adjustment = 4.0
            elif 150 < adjust_metic <= 160:
                self.adjustment = 5.5
            elif 160 < adjust_metic <= 170:
                self.adjustment = 7.0
            elif 170 < adjust_metic <= 180:
                self.adjustment = 9.0
            elif adjust_metic > 180:
                pace_adjustment = "Hard running not recommended"

            if self.adjustment is not None:
                minutes, seconds = self._pace_calc(self.adjustment)
                pace_adjustment = f"{minutes}:{seconds} minutes/miles"
      
        else:
            pace_adjustment = "Unable to calculate pace adjustment"

        return pace_adjustment
            
if __name__ == '__main__':

     
    w = HeatIndexPaceAdjustment(95, 90, 9.5, False)
    pace = w.pace_adjustment()
    print(pace)
