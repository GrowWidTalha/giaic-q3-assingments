class Logger:
    """
    A simple Logger class that demonstrates constructor and destructor usage.
    The constructor (__init__) is called when an object is created,
    and the destructor (__del__) is called when the object is about to be destroyed.
    """
    
    def __init__(self, name: str):
        """
        Constructor method that initializes the Logger object.
        
        Args:
            name (str): The name of the logger instance
        """
        self.name = name
        print(f"🔨 Logger '{self.name}' has been created!")
    
    def log(self, message: str) -> None:
        """
        Log a message with the logger's name.
        
        Args:
            message (str): The message to log
        """
        print(f"[{self.name}] {message}")
    
    def __del__(self):
        """
        Destructor method that is called when the object is about to be destroyed.
        This happens when:
        1. The object goes out of scope
        2. The program ends
        3. The object is explicitly deleted using 'del'
        """
        print(f"🗑️ Logger '{self.name}' is being destroyed!")


def main():
    # Create a logger instance
    logger = Logger("MainLogger")
    
    # Use the logger
    logger.log("This is a test message")
    
    # Create another logger
    temp_logger = Logger("TempLogger")
    temp_logger.log("This is a temporary logger")
    
    # The temp_logger will be destroyed when it goes out of scope
    print("\nEnd of main function - temp_logger will be destroyed")
    
    # The main logger will be destroyed when the program ends
    print("Program ending - main logger will be destroyed")


if __name__ == "__main__":
    main() 