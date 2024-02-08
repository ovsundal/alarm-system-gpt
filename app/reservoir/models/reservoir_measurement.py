from django.db import models


class ReservoirMeasurement(models.Model):
    start_timestamp = models.DateTimeField()
    end_timestamp = models.DateTimeField()
    duration_hr = models.FloatField()
    reference_rate = models.FloatField()
    q = models.CharField(max_length=255)
    p_26hr = models.FloatField()
    t_26hr = models.FloatField()
    p_58hr = models.FloatField()
    t_58hr = models.FloatField()
    wpi = models.FloatField()
    rpi = models.FloatField()
    cpi = models.FloatField()
    is_shutin = models.BooleanField()
    is_prev_shutin = models.BooleanField()
    pressure_std = models.FloatField()
    derivative_std = models.FloatField()
    well_id = models.FloatField()

    def __str__(self):
        return (f"Measurement from {self.start_timestamp} to "
                f"{self.end_timestamp}")
