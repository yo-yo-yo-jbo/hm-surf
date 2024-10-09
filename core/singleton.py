class Singleton(type):
    """
        Implements a singleton class.
    """
    
    # Saves the instance
    instance = None

    def __call__(cls, *args, **kwargs):
        """
            Implements a singleton.
        """
        
        # Implements a singleton
        if cls.instance is None:
            cls.instance = super(Singleton, cls).__call__(*args, **kwargs)
        return cls.instance

    def get_instance(cls):
        """
            Get the class instance.
        """
        
        # Return the instance
        return cls.instance

