"""
Database connection utilities for MongoDB
"""
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
import logging
from payroll_system.config import MONGODB_URI, MONGODB_HOST, MONGODB_PORT, MONGODB_DB_NAME

logger = logging.getLogger(__name__)

class Database:
    """Singleton database connection manager"""
    _instance = None
    _client = None
    _db = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
        return cls._instance
    
    def connect(self):
        """Establish connection to MongoDB"""
        try:
            if self._client is None:
                if MONGODB_URI:
                    # Atlas / SRV / authenticated connection
                    self._client = MongoClient(
                        MONGODB_URI,
                        serverSelectionTimeoutMS=5000,
                    )
                else:
                    # Local/host-port connection
                    self._client = MongoClient(
                        host=MONGODB_HOST,
                        port=MONGODB_PORT,
                        serverSelectionTimeoutMS=5000
                    )
                # Test connection
                self._client.admin.command('ping')
                self._db = self._client[MONGODB_DB_NAME]
                if MONGODB_URI:
                    logger.info("Connected to MongoDB via MONGODB_URI")
                else:
                    logger.info(f"Connected to MongoDB at {MONGODB_HOST}:{MONGODB_PORT}")
                self._create_indexes()
            return self._db
        except ConnectionFailure as e:
            logger.error(f"Failed to connect to MongoDB: {e}")
            raise
    
    def _create_indexes(self):
        """Create necessary indexes for better query performance"""
        try:
            # Employee indexes
            self._db.employees.create_index("employee_id", unique=True)
            self._db.employees.create_index("email", unique=True)
            
            # Attendance indexes
            self._db.attendance.create_index([("employee_id", 1), ("date", 1)], unique=True)
            
            # Payroll indexes
            self._db.payrolls.create_index([("employee_id", 1), ("month", 1), ("year", 1)], unique=True)
            
            logger.info("Database indexes created successfully")
        except Exception as e:
            logger.warning(f"Error creating indexes: {e}")
    
    def get_db(self):
        """Get database instance"""
        if self._db is None:
            self.connect()
        return self._db
    
    def disconnect(self):
        """Close database connection"""
        if self._client:
            self._client.close()
            self._client = None
            self._db = None
            logger.info("Disconnected from MongoDB")

# Global database instance
db = Database()

