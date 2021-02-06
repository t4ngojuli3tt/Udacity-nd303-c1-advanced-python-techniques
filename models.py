"""Represent models for near-Earth objects and their close approaches.

The `NearEarthObject` class represents a near-Earth object. Each has a unique
primary designation, an optional unique name, an optional diameter, and a flag
for whether the object is potentially hazardous.

The `CloseApproach` class represents a close approach to Earth by an NEO. Each
has an approach datetime, a nominal approach distance, and a relative approach
velocity.

A `NearEarthObject` maintains a collection of its close approaches, and a
`CloseApproach` maintains a reference to its NEO.

The functions that construct these objects use information extracted from the
data files from NASA, so these objects should be able to handle all of the
quirks of the data set, such as missing names and unknown diameters.

You'll edit this file in Task 1.
"""
import math
from helpers import cd_to_datetime, datetime_to_str, default_if_empty, y_to_true


class NearEarthObject:
    """A near-Earth object (NEO).

    An NEO encapsulates semantic and physical parameters about the object, such
    as its primary designation (required, unique), IAU name (optional), diameter
    in kilometers (optional - sometimes unknown), and whether it's marked as
    potentially hazardous to Earth.

    A `NearEarthObject` also maintains a collection of its close approaches -
    initialized to an empty collection, but eventually populated in the
    `NEODatabase` constructor.
    """

    def __init__(self, **info):
        """Create a new `NearEarthObject`.

        :param info: A dictionary of excess keyword arguments supplied to the constructor.
        """

        self.designation = info['pdes']
        self.name = default_if_empty(info['name'], None)
        self.diameter = default_if_empty(info['diameter'], float('nan'), float)
        self.hazardous = default_if_empty(info['pha'], False, y_to_true)

        # Create an empty initial collection of linked approaches.
        self.approaches = []

    @property
    def fullname(self):
        """Return a representation of the full name of this NEO."""

        return self.designation + default_if_empty(self.name, "")

    def __str__(self):
        """Return `str(self)`."""

        diameter = f"diameter of {self.diameter:.3f}" if not math.isnan(
            self.diameter) else "unknown diameter"
        is_hazardous = 'potentially' if self.hazardous else 'not'
        return f"A NearEarthObject {self.fullname} with {diameter} is {is_hazardous} hazardous."

    def __repr__(self):
        """Return `repr(self)`, a computer-readable string representation of this object."""
        return (f"NearEarthObject(designation={self.designation!r}, name={self.name!r}, "
                f"diameter={self.diameter:.3f}, hazardous={self.hazardous!r})")

    def serialize(self):
        """
        Methods to produce a dictionary containing relevant attributes for CSV or JSON serialization.
        """
        serialize = {}
        serialize['designation'] = self.designation
        serialize['name'] = self.name
        serialize['diameter_km'] = default_if_empty(self.diameter, 'unknown')
        serialize['potentially_hazardous'] = self.hazardous

        return serialize


class CloseApproach:
    """A close approach to Earth by an NEO.

    A `CloseApproach` encapsulates information about the NEO's close approach to
    Earth, such as the date and time (in UTC) of closest approach, the nominal
    approach distance in astronomical units, and the relative approach velocity
    in kilometers per second.

    A `CloseApproach` also maintains a reference to its `NearEarthObject` -
    initally, this information (the NEO's primary designation) is saved in a
    private attribute, but the referenced NEO is eventually replaced in the
    `NEODatabase` constructor.
    """

    def __init__(self, **info):
        """Create a new `CloseApproach`.

        :param info: A dictionary of excess keyword arguments supplied to the constructor.
        """

        self._designation = info['des']
        self.time = default_if_empty(info['cd'], None, cd_to_datetime)
        self.distance = default_if_empty(info['dist'], 0.0, float)
        self.velocity = default_if_empty(info['v_rel'], 0.0, float)

        # Create an attribute for the referenced NEO, originally None.
        self.neo = None

    @property
    def time_str(self):
        """Return a formatted representation of this `CloseApproach`'s approach time.

        The value in `self.time` should be a Python `datetime` object. While a
        `datetime` object has a string representation, the default representation
        includes seconds - significant figures that don't exist in our input
        data set.

        The `datetime_to_str` method converts a `datetime` object to a
        formatted string that can be used in human-readable representations and
        in serialization to CSV and JSON files.
        """
        return datetime_to_str(self.time)

    @property
    def fullname(self):
        """Return a representation of the full name of this NEO."""

        return self._designation + default_if_empty(self.neo, "")

    def __str__(self):
        """Return `str(self)`."""

        time = f"{self.time_str}" if not self.time else "unkown date"
        return f"A CloseApproach event at {self.time_str}, of {self.fullname} approching Earth at a distance "\
            f"of {self.distance:.2f} au and a velocity of {self.velocity:.2f} km/s."

    def __repr__(self):
        """Return `repr(self)`, a computer-readable string representation of this object."""
        return (f"CloseApproach(time={self.time_str!r}, distance={self.distance:.2f}, "
                f"velocity={self.velocity:.2f}, neo={self.neo!r})")

    def serialize(self):
        """
        Methods to produce a dictionary containing relevant attributes for CSV or JSON serialization.
        """
        serialize = {}
        serialize['datetime_utc'] = self.time_str
        serialize['distance_au'] = self.distance
        serialize['velocity_km_s'] = self.velocity
        serialize['neo'] = self.neo.serialize()

        return serialize
