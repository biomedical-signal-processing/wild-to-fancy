import os
import numpy as np

class _Defaults:
    """
    Stores and potentially updates default values for sleep stages etc.
    """
    # Global RNG seed
    GLOBAL_SEED = None

    @classmethod
    def set_global_seed(cls, seed):
        import numpy as np
        import random
        cls.GLOBAL_SEED = int(seed)
        print("Seeding numpy and random modules with seed: {}".format(cls.GLOBAL_SEED))
        np.random.seed(cls.GLOBAL_SEED)
        random.seed(cls.GLOBAL_SEED)

class _Defaults_hypnograms:
    """
    Stores and potentially updates default values for sleep stages etc.
    """
    # Standardized string representation for 5 typical sleep stages
    AWAKE = ["W", 0]
    NON_REM_STAGE_1 = ["N1", 1]
    NON_REM_STAGE_2 = ["N2", 2]
    NON_REM_STAGE_3 = ["N3", 3]
    REM = ["REM", 4]
    UNKNOWN = ["UNKNOWN", 5]
    OUT_OF_BOUNDS = ["OUT_OF_BOUNDS", 6]

    # Visualization defaults
    STAGE_COLORS = ["darkblue", "darkred",
                    "darkgreen", "darkcyan",
                    "darkorange", "black"]

    # Default segmentation length in seconds
    PERIOD_LENGTH_SEC = 30

    @classmethod
    def get_stage_lists(cls):
        return [cls.AWAKE, cls.NON_REM_STAGE_1, cls.NON_REM_STAGE_2,
                cls.NON_REM_STAGE_3, cls.REM, cls.UNKNOWN]

    @classmethod
    def get_stage_string_to_class_int(cls):
        # Dictionary mapping from the standardized string rep to integer
        # representation
        return {s[0]: s[1] for s in cls.get_stage_lists()}
